import os
import re
import yaml
import json
import subprocess
import sqlite3
import click
import logging
from termcolor import colored
import datetime

class ContextOptimizer:
    def __init__(self, config_path="config/dspy_config.yaml"):
        self.config = self.load_config(config_path)

    def load_config(self, config_path):
        with open(config_path, "r") as f:
            return yaml.safe_load(f)

class ContextEvaluator:
    def __init__(self, config_path="config/dspy_config.yaml"):
        self.optimizer = ContextOptimizer(config_path)
        self.config = self.optimizer.config
        self.temp_dir = os.path.join(os.getcwd(), "temp", "evaluations")
        os.makedirs(self.temp_dir, exist_ok=True)
        self.logger = setup_logger("context_evaluator")
        
    def create_evaluation_config(self, original_module_path, optimized_module_path, output_path):
        """Create PromptFoo evaluation configuration for comparing module versions"""
        # Extract module name for test case generation
        module_name = os.path.basename(original_module_path).replace(".md", "")
        
        # Generate test cases based on module content
        test_cases = self.generate_test_cases(original_module_path)
        
        # Create PromptFoo config structure
        eval_config = {
            "providers": [
                {
                    "id": "original",
                    "module": original_module_path,
                },
                {
                    "id": "optimized",
                    "module": optimized_module_path,
                }
            ],
            "tests": test_cases,
            "outputPath": output_path
        }
        
        config_path = os.path.join(self.temp_dir, f"{module_name}_eval_config.yaml")
        with open(config_path, "w") as f:
            yaml.dump(eval_config, f)
            
        return config_path
        
    def generate_test_cases(self, module_path):
        """Generate test cases based on module content using its contexts and examples"""
        test_cases = []
        
        try:
            with open(module_path, "r") as f:
                content = f.read()
                
            # Extract context blocks and use them as test scenarios
            context_blocks = re.findall(r'<context name="(.*?)".*?>(.*?)</context>', 
                                        content, re.DOTALL)
            
            # Create test cases from each context block
            for name, block_content in context_blocks:
                # Extract code examples if available
                code_examples = re.findall(r'```(?:.*?)\n(.*?)```', block_content, re.DOTALL)
                
                # Generate prompts related to this context
                prompts = [
                    f"Explain how to implement {name.replace('_', ' ')}",
                    f"What are the best practices for {name.replace('_', ' ')}?",
                    f"Generate code for {name.replace('_', ' ')}"
                ]
                
                # Add test case for each prompt
                for idx, prompt in enumerate(prompts):
                    test_case = {
                        "vars": {
                            "input": prompt,
                            "context": block_content[:500]  # Use first 500 chars as context
                        },
                        "assert": [
                            {"type": "contains_any", "value": self._extract_key_terms(block_content)},
                            {"type": "not_contains", "value": ["I don't know", "I cannot", "I don't have"]}
                        ]
                    }
                    
                    # Add example validation if code examples exist
                    if code_examples and idx == 2:  # For code generation prompt
                        test_case["assert"].append({
                            "type": "similar_code", 
                            "value": code_examples[0] if code_examples else ""
                        })
                        
                    test_cases.append(test_case)
            
            # If we couldn't extract context blocks, create generic test cases
            if not test_cases:
                module_name = os.path.basename(module_path).replace(".md", "").replace("_", " ")
                test_cases = [
                    {
                        "vars": {
                            "input": f"Explain {module_name} implementation"
                        },
                        "assert": [
                            {"type": "not_contains", "value": ["I don't know", "I cannot"]}
                        ]
                    },
                    {
                        "vars": {
                            "input": f"Generate code that implements {module_name}"
                        },
                        "assert": [
                            {"type": "contains_code", "value": True}
                        ]
                    }
                ]
                
            return test_cases
            
        except Exception as e:
            self.logger.error(f"Error generating test cases: {str(e)}")
            # Return basic test cases on failure
            return [
                {
                    "vars": {
                        "input": "Explain this module's implementation"
                    }
                }
            ]
            
    def _extract_key_terms(self, content):
        """Extract key technical terms from content for assertion validation"""
        # Remove markdown and code blocks
        clean_content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        clean_content = re.sub(r'#.*?\n', '', clean_content)
        
        # Find technical terms (camelCase, PascalCase, snake_case, etc.)
        terms = re.findall(r'\b([A-Z][a-z]+[A-Z][a-z]*\w*|\w+_\w+|[a-z]+[A-Z]\w*)\b', clean_content)
        
        # Get common technical words
        tech_words = re.findall(r'\b(function|class|method|component|interface|module|api|async|await|promise|callback|event|listener|handler|parameter|argument|return|object|array|string|number|boolean|null|undefined|import|export|default|const|let|var|if|else|switch|case|for|while|do|break|continue|try|catch|throw|new|this|super|extends|implements|static|public|private|protected)\b', 
                               clean_content, re.IGNORECASE)
        
        # Combine and return unique terms
        all_terms = set(terms + tech_words)
        return list(all_terms)[:10]  # Return top 10 terms
        
    def run_evaluation(self, config_path):
        """Run PromptFoo evaluation and return results"""
        try:
            # Build PromptFoo command
            cmd = f"promptfoo eval --config {config_path} --output json"
            
            # Run evaluation
            process = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self.logger.error(f"Evaluation failed: {stderr.decode()}")
                return None
                
            # Parse results
            results = json.loads(stdout.decode())
            
            # Calculate scores
            scores = {
                "original": {"pass": 0, "fail": 0, "total": 0},
                "optimized": {"pass": 0, "fail": 0, "total": 0}
            }
            
            for test in results.get("results", []):
                for provider_result in test.get("providerResults", []):
                    provider = provider_result.get("provider", {}).get("id")
                    if provider in scores:
                        scores[provider]["total"] += 1
                        if provider_result.get("success", False):
                            scores[provider]["pass"] += 1
                        else:
                            scores[provider]["fail"] += 1
            
            # Calculate improvement percentage
            if scores["original"]["total"] > 0 and scores["optimized"]["total"] > 0:
                original_pass_rate = scores["original"]["pass"] / scores["original"]["total"]
                optimized_pass_rate = scores["optimized"]["pass"] / scores["optimized"]["total"]
                improvement = (optimized_pass_rate - original_pass_rate) * 100
            else:
                improvement = 0
                
            return {
                "scores": scores,
                "improvement": improvement,
                "raw_results": results
            }
            
        except Exception as e:
            self.logger.error(f"Error running evaluation: {str(e)}")
            return None
            
    def evaluate_module(self, original_module_path, optimized_module_path):
        """Evaluate the performance of original vs optimized module"""
        try:
            # Verify paths exist
            if not os.path.exists(original_module_path):
                self.logger.error(f"Original module not found: {original_module_path}")
                return {"success": False, "error": "Original module not found"}
                
            if not os.path.exists(optimized_module_path):
                self.logger.error(f"Optimized module not found: {optimized_module_path}")
                return {"success": False, "error": "Optimized module not found"}
                
            module_name = os.path.basename(original_module_path).replace(".md", "")
            output_path = os.path.join(self.temp_dir, f"{module_name}_results")
            
            # Create evaluation config
            config_path = self.create_evaluation_config(
                original_module_path, optimized_module_path, output_path
            )
            
            # Run evaluation
            results = self.run_evaluation(config_path)
            
            if results is None:
                return {"success": False, "error": "Evaluation failed"}
                
            # Log results
            self.logger.info(f"Evaluation complete for {module_name}")
            self.logger.info(f"Original pass rate: {results['scores']['original']['pass']}/{results['scores']['original']['total']}")
            self.logger.info(f"Optimized pass rate: {results['scores']['optimized']['pass']}/{results['scores']['optimized']['total']}")
            self.logger.info(f"Improvement: {results['improvement']:.2f}%")
            
            return {
                "success": True,
                "module_name": module_name,
                "improvement": results["improvement"],
                "scores": results["scores"],
                "details_path": output_path
            }
            
        except Exception as e:
            self.logger.error(f"Error evaluating module: {str(e)}")
            return {"success": False, "error": str(e)}

    def batch_evaluate(self, modules_dir, optimized_dir):
        """Evaluate multiple modules and generate a summary report"""
        results = {
            "success_count": 0,
            "total": 0,
            "improved": [],
            "regressed": [],
            "unchanged": [],
            "failed": [],
            "avg_improvement": 0
        }
        
        # Get all modules
        modules = [f for f in os.listdir(modules_dir) if f.endswith(".md")]
        results["total"] = len(modules)
        
        improvement_sum = 0
        success_count = 0
        
        for module in modules:
            original_path = os.path.join(modules_dir, module)
            optimized_path = os.path.join(optimized_dir, module)
            
            # Skip if optimized version doesn't exist
            if not os.path.exists(optimized_path):
                self.logger.warning(f"No optimized version found for {module}")
                results["failed"].append({
                    "module": module,
                    "reason": "No optimized version found"
                })
                continue
                
            # Evaluate module
            eval_result = self.evaluate_module(original_path, optimized_path)
            
            if eval_result["success"]:
                success_count += 1
                improvement = eval_result["improvement"]
                improvement_sum += improvement
                
                # Categorize result
                if improvement > 1.0:  # 1% improvement threshold
                    results["improved"].append({
                        "module": module,
                        "improvement": improvement
                    })
                elif improvement < -1.0:  # 1% regression threshold 
                    results["regressed"].append({
                        "module": module,
                        "regression": -improvement
                    })
                else:
                    results["unchanged"].append({
                        "module": module,
                        "improvement": improvement
                    })
            else:
                results["failed"].append({
                    "module": module,
                    "reason": eval_result.get("error", "Unknown error")
                })
        
        # Calculate average improvement
        if success_count > 0:
            results["avg_improvement"] = improvement_sum / success_count
            
        results["success_count"] = success_count
        
        # Sort results by improvement magnitude
        results["improved"] = sorted(results["improved"], key=lambda x: x["improvement"], reverse=True)
        results["regressed"] = sorted(results["regressed"], key=lambda x: x["regression"], reverse=True)
        
        return results

# CLI commands for evaluation integration
@click.group()
def evaluate():
    """Evaluate context module optimizations"""
    pass

@evaluate.command()
@click.argument("module_path", type=click.Path(exists=True))
@click.option("--optimized-path", "-o", type=click.Path(exists=True), 
              help="Path to optimized module (default: optimized/<module_name>.md)")
@click.option("--output", type=click.Path(), help="Output path for evaluation results")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed output")
def module(module_path, optimized_path=None, output=None, verbose=False):
    """Evaluate a single module optimization"""
    try:
        # Set up logger
        log_level = logging.INFO if verbose else logging.WARNING
        setup_logger("context_evaluator", level=log_level)
        
        # Resolve paths
        module_name = os.path.basename(module_path)
        if optimized_path is None:
            optimized_dir = os.path.join(os.getcwd(), "optimized")
            optimized_path = os.path.join(optimized_dir, module_name)
            
        # Create evaluator and run evaluation
        evaluator = ContextEvaluator()
        result = evaluator.evaluate_module(module_path, optimized_path)
        
        if result["success"]:
            improvement = result["improvement"]
            if improvement > 0:
                status = colored(f"+{improvement:.2f}%", "green")
            elif improvement < 0:
                status = colored(f"{improvement:.2f}%", "red")
            else:
                status = colored("0.00%", "yellow")
                
            click.echo(f"Evaluation complete for {module_name}")
            click.echo(f"Improvement: {status}")
            click.echo(f"Original: {result['scores']['original']['pass']}/{result['scores']['original']['total']} tests passed")
            click.echo(f"Optimized: {result['scores']['optimized']['pass']}/{result['scores']['optimized']['total']} tests passed")
            
            if improvement > 5:
                click.echo(colored("\nRecommendation: Apply this optimization ✓", "green"))
            elif improvement < -2:
                click.echo(colored("\nRecommendation: Keep original version ✗", "red"))
            else:
                click.echo(colored("\nRecommendation: Review manually (marginal change)", "yellow"))
                
            # Save output if specified
            if output:
                with open(output, "w") as f:
                    json.dump(result, f, indent=2)
                click.echo(f"\nDetailed results saved to {output}")
                
            # Show details path
            click.echo(f"\nFull evaluation details available at: {result['details_path']}")
            
            return 0
        else:
            click.echo(f"Evaluation failed: {result.get('error', 'Unknown error')}")
            return 1
            
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        return 1

@evaluate.command()
@click.argument("modules_dir", type=click.Path(exists=True))
@click.option("--optimized-dir", "-o", type=click.Path(exists=True), 
              help="Directory containing optimized modules (default: optimized/)")
@click.option("--output", type=click.Path(), help="Output JSON file for evaluation results")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed output")
def batch(modules_dir, optimized_dir=None, output=None, verbose=False):
    """Evaluate multiple module optimizations in batch"""
    try:
        # Set up logger
        log_level = logging.INFO if verbose else logging.WARNING
        setup_logger("context_evaluator", level=log_level)
        
        # Resolve paths
        if optimized_dir is None:
            optimized_dir = os.path.join(os.getcwd(), "optimized")
            
        # Create evaluator and run batch evaluation
        evaluator = ContextEvaluator()
        results = evaluator.batch_evaluate(modules_dir, optimized_dir)
        
        # Display results summary
        click.echo(f"\nEvaluation Summary ({results['success_count']}/{results['total']} modules evaluated)")
        click.echo(f"Average improvement: {results['avg_improvement']:.2f}%")
        click.echo(f"Improved modules: {len(results['improved'])}")
        click.echo(f"Regressed modules: {len(results['regressed'])}")
        click.echo(f"Unchanged modules: {len(results['unchanged'])}")
        click.echo(f"Failed evaluations: {len(results['failed'])}")
        
        # Display top improvements
        if results['improved']:
            click.echo("\nTop Improvements:")
            for item in results['improved'][:5]:  # Show top 5
                module = item['module']
                improvement = item['improvement']
                click.echo(f"  {module}: {colored(f'+{improvement:.2f}%', 'green')}")
                
        # Display top regressions
        if results['regressed']:
            click.echo("\nTop Regressions:")
            for item in results['regressed'][:5]:  # Show top 5
                module = item['module']
                regression = item['regression']
                click.echo(f"  {module}: {colored(f'-{regression:.2f}%', 'red')}")
                
        # Save output if specified
        if output:
            with open(output, "w") as f:
                json.dump(results, f, indent=2)
            click.echo(f"\nDetailed results saved to {output}")
            
        return 0
            
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        return 1

class ContextFeedback:
    def __init__(self, db_path="data/feedback.db"):
        """Initialize feedback collection and storage system"""
        self.db_path = db_path
        self.logger = setup_logger("context_feedback")
        
        # Ensure database directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database
        self._init_db()
        
    def _init_db(self):
        """Initialize SQLite database for feedback storage"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create feedback table if it doesn't exist
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS module_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_name TEXT NOT NULL,
                feedback_text TEXT NOT NULL,
                sentiment REAL,
                model_used TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                processed INTEGER DEFAULT 0
            )
            ''')
            
            # Create optimization results table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS optimization_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_name TEXT NOT NULL,
                target_model TEXT NOT NULL,
                improvement REAL,
                success INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                applied INTEGER DEFAULT 0
            )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Error initializing database: {str(e)}")
            raise
            
    def record_feedback(self, module_name, feedback_text, model_used=None):
        """Record feedback for a specific module"""
        try:
            # Perform sentiment analysis on feedback
            sentiment = self._analyze_sentiment(feedback_text)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO module_feedback (module_name, feedback_text, sentiment, model_used) VALUES (?, ?, ?, ?)",
                (module_name, feedback_text, sentiment, model_used)
            )
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Recorded feedback for module: {module_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error recording feedback: {str(e)}")
            return False
            
    def _analyze_sentiment(self, text):
        """Basic sentiment analysis for feedback classification"""
        # Simple keyword-based sentiment analysis
        positive_words = set([
            "good", "great", "excellent", "helpful", "useful", "clear", 
            "effective", "improved", "better", "best", "perfect"
        ])
        
        negative_words = set([
            "bad", "poor", "unclear", "confusing", "unhelpful", "worse",
            "wrong", "incorrect", "error", "issue", "problem", "bug"
        ])
        
        # Clean and tokenize text
        clean_text = re.sub(r'[^\w\s]', '', text.lower())
        words = clean_text.split()
        
        # Count positive and negative words
        pos_count = sum(1 for word in words if word in positive_words)
        neg_count = sum(1 for word in words if word in negative_words)
        
        # Calculate sentiment score (-1 to 1)
        total = pos_count + neg_count
        if total == 0:
            return 0
        return (pos_count - neg_count) / total
        
    def record_optimization_result(self, module_name, target_model, improvement, success):
        """Record the result of a module optimization attempt"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO optimization_results (module_name, target_model, improvement, success) VALUES (?, ?, ?, ?)",
                (module_name, target_model, improvement, 1 if success else 0)
            )
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Recorded optimization result for module: {module_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error recording optimization result: {str(e)}")
            return False
    
    def mark_optimization_applied(self, module_name, target_model):
        """Mark an optimization as applied in production"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE optimization_results SET applied = 1 WHERE module_name = ? AND target_model = ? ORDER BY timestamp DESC LIMIT 1",
                (module_name, target_model)
            )
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Marked optimization as applied for module: {module_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error marking optimization as applied: {str(e)}")
            return False
            
    def get_module_effectiveness(self, module_name=None):
        """Calculate module effectiveness based on feedback sentiment"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if module_name:
                cursor.execute(
                    "SELECT AVG(sentiment) FROM module_feedback WHERE module_name = ?",
                    (module_name,)
                )
            else:
                cursor.execute("SELECT module_name, AVG(sentiment) FROM module_feedback GROUP BY module_name")
                
            results = cursor.fetchall()
            conn.close()
            
            if module_name:
                return results[0][0] if results and results[0][0] is not None else 0
            else:
                return {row[0]: row[1] for row in results if row[1] is not None}
                
        except Exception as e:
            self.logger.error(f"Error calculating module effectiveness: {str(e)}")
            return {} if module_name is None else 0
            
    def get_modules_for_optimization(self, threshold=-0.2, min_feedback=3):
        """Identify modules that need optimization based on feedback"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT module_name, AVG(sentiment) as avg_sentiment, COUNT(*) as feedback_count
                FROM module_feedback 
                GROUP BY module_name
                HAVING avg_sentiment < ? AND feedback_count >= ?
                ORDER BY avg_sentiment ASC
            """, (threshold, min_feedback))
            
            results = cursor.fetchall()
            conn.close()
            
            return [
                {"module": row[0], "sentiment": row[1], "feedback_count": row[2]}
                for row in results
            ]
            
        except Exception as e:
            self.logger.error(f"Error identifying modules for optimization: {str(e)}")
            return []
            
    def get_optimization_success_rate(self, module_name=None, target_model=None):
        """Calculate success rate of optimizations"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT COUNT(*), SUM(success) FROM optimization_results WHERE 1=1"
            params = []
            
            if module_name:
                query += " AND module_name = ?"
                params.append(module_name)
                
            if target_model:
                query += " AND target_model = ?"
                params.append(target_model)
                
            cursor.execute(query, params)
            total, successes = cursor.fetchone()
            conn.close()
            
            if total and total > 0:
                return (successes or 0) / total
            return 0
            
        except Exception as e:
            self.logger.error(f"Error calculating optimization success rate: {str(e)}")
            return 0
            
    def export_data(self, output_path):
        """Export feedback and optimization data to JSON"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get all feedback records
            cursor.execute("SELECT * FROM module_feedback ORDER BY timestamp DESC")
            feedback_records = [dict(row) for row in cursor.fetchall()]
            
            # Get all optimization results
            cursor.execute("SELECT * FROM optimization_results ORDER BY timestamp DESC")
            optimization_results = [dict(row) for row in cursor.fetchall()]
            
            # Create summary data
            summary = {
                "total_feedback": len(feedback_records),
                "total_optimizations": len(optimization_results),
                "avg_sentiment": sum(r["sentiment"] for r in feedback_records if r["sentiment"]) / len(feedback_records) if feedback_records else 0,
                "avg_improvement": sum(r["improvement"] for r in optimization_results if r["improvement"]) / len(optimization_results) if optimization_results else 0,
                "applied_optimizations": sum(1 for r in optimization_results if r["applied"])
            }
            
            # Combine all data
            export_data = {
                "feedback": feedback_records,
                "optimizations": optimization_results,
                "summary": summary
            }
            
            # Write to file
            with open(output_path, "w") as f:
                json.dump(export_data, f, indent=2)
                
            conn.close()
            self.logger.info(f"Data exported to {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting data: {str(e)}")
            return False 

def setup_logger(name, level=logging.INFO):
    """Configure logger with consistent formatting"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

class BatchProcessor:
    """Handles batch processing of module optimization and tracking"""
    
    def __init__(self, config_path="config/dspy_config.yaml"):
        self.config_path = config_path
        self.optimizer = ContextOptimizer(config_path)
        self.evaluator = ContextEvaluator(config_path)
        self.feedback = ContextFeedback()
        self.logger = setup_logger("batch_processor")
        
    def process_config(self, batch_config_path):
        """Process a batch configuration file for module optimization"""
        try:
            with open(batch_config_path, "r") as f:
                batch_config = yaml.safe_load(f)
                
            results = {
                "total": 0,
                "succeeded": 0,
                "failed": 0,
                "modules": []
            }
            
            # Get module paths
            modules_dir = batch_config.get("modules_dir", "modules")
            optimized_dir = batch_config.get("optimized_dir", "optimized")
            target_model = batch_config.get("target_model", "gpt-4")
            
            # Get modules list (either from config or directory)
            if "modules" in batch_config:
                modules = batch_config["modules"]
                # Convert to full paths
                module_paths = [os.path.join(modules_dir, module) for module in modules]
            else:
                # Get all markdown files from modules directory
                module_paths = [
                    os.path.join(modules_dir, f) 
                    for f in os.listdir(modules_dir) 
                    if f.endswith(".md")
                ]
                modules = [os.path.basename(path) for path in module_paths]
            
            # Process each module
            results["total"] = len(modules)
            
            for module_path, module_name in zip(module_paths, modules):
                self.logger.info(f"Processing module: {module_name}")
                
                # Skip if module doesn't exist
                if not os.path.exists(module_path):
                    self.logger.warning(f"Module not found: {module_path}")
                    results["failed"] += 1
                    results["modules"].append({
                        "name": module_name,
                        "status": "failed",
                        "error": "Module file not found"
                    })
                    continue
                
                # Create optimized path
                optimized_path = os.path.join(optimized_dir, module_name)
                
                # Optimize module
                optimize_result = self.optimizer.optimize_module(
                    module_path, 
                    output_path=optimized_path,
                    model=target_model
                )
                
                if optimize_result["success"]:
                    # Evaluate the optimization
                    eval_result = self.evaluator.evaluate_module(
                        module_path, 
                        optimized_path
                    )
                    
                    # Record optimization result in feedback system
                    improvement = eval_result.get("improvement", 0) if eval_result["success"] else 0
                    self.feedback.record_optimization_result(
                        module_name, 
                        target_model, 
                        improvement, 
                        eval_result["success"]
                    )
                    
                    # Add to results
                    results["succeeded"] += 1
                    results["modules"].append({
                        "name": module_name,
                        "status": "success",
                        "improvement": improvement,
                        "eval_success": eval_result["success"]
                    })
                else:
                    # Record failed optimization
                    self.feedback.record_optimization_result(
                        module_name, 
                        target_model, 
                        0, 
                        False
                    )
                    
                    results["failed"] += 1
                    results["modules"].append({
                        "name": module_name,
                        "status": "failed",
                        "error": optimize_result.get("error", "Unknown error")
                    })
            
            # Save results
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            results_path = f"reports/batch_results_{timestamp}.json"
            os.makedirs(os.path.dirname(results_path), exist_ok=True)
            
            with open(results_path, "w") as f:
                json.dump(results, f, indent=2)
                
            self.logger.info(f"Batch processing complete. Results saved to {results_path}")
            return results
            
        except Exception as e:
            self.logger.error(f"Error processing batch: {str(e)}")
            return {"total": 0, "succeeded": 0, "failed": 0, "error": str(e)}
            
    def auto_optimize_priority_modules(self, limit=5):
        """Automatically optimize modules with poor feedback"""
        try:
            # Get modules that need optimization
            priority_modules = self.feedback.get_modules_for_optimization()
            
            # Limit the number of modules to process
            priority_modules = priority_modules[:limit]
            
            if not priority_modules:
                self.logger.info("No modules identified for optimization")
                return {"total": 0, "succeeded": 0, "failed": 0, "modules": []}
                
            self.logger.info(f"Auto-optimizing {len(priority_modules)} priority modules")
            
            # Create batch config
            batch_config = {
                "modules": [module["module"] for module in priority_modules],
                "target_model": self.optimizer.config.get("default_model", "gpt-4")
            }
            
            # Save temporary batch config
            temp_config_path = "temp/auto_optimize_config.yaml"
            os.makedirs(os.path.dirname(temp_config_path), exist_ok=True)
            
            with open(temp_config_path, "w") as f:
                yaml.dump(batch_config, f)
                
            # Process the batch
            return self.process_config(temp_config_path)
            
        except Exception as e:
            self.logger.error(f"Error auto-optimizing modules: {str(e)}")
            return {"total": 0, "succeeded": 0, "failed": 0, "error": str(e)}
            
    def analyze_optimization_performance(self):
        """Analyze optimization performance across modules and models"""
        try:
            # Get all optimization results
            conn = sqlite3.connect(self.feedback.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get model-specific performance
            cursor.execute("""
                SELECT target_model, 
                       AVG(improvement) as avg_improvement, 
                       SUM(success) as successes,
                       COUNT(*) as total
                FROM optimization_results
                GROUP BY target_model
            """)
            
            model_performance = [dict(row) for row in cursor.fetchall()]
            
            # Get module-specific performance
            cursor.execute("""
                SELECT module_name, 
                       AVG(improvement) as avg_improvement, 
                       SUM(success) as successes,
                       COUNT(*) as total
                FROM optimization_results
                GROUP BY module_name
                ORDER BY avg_improvement DESC
            """)
            
            module_performance = [dict(row) for row in cursor.fetchall()]
            
            # Get overall stats
            cursor.execute("""
                SELECT AVG(improvement) as avg_improvement, 
                       SUM(success) as successes,
                       COUNT(*) as total,
                       SUM(applied) as applied
                FROM optimization_results
            """)
            
            overall = dict(cursor.fetchone())
            
            conn.close()
            
            # Generate report
            report = {
                "timestamp": datetime.datetime.now().isoformat(),
                "overall": overall,
                "models": model_performance,
                "modules": module_performance,
                "top_modules": module_performance[:5] if len(module_performance) > 5 else module_performance,
                "bottom_modules": module_performance[-5:] if len(module_performance) > 5 else []
            }
            
            # Save report
            report_path = "reports/optimization_analysis.json"
            os.makedirs(os.path.dirname(report_path), exist_ok=True)
            
            with open(report_path, "w") as f:
                json.dump(report, f, indent=2)
                
            self.logger.info(f"Optimization performance analysis complete. Report saved to {report_path}")
            return report
            
        except Exception as e:
            self.logger.error(f"Error analyzing optimization performance: {str(e)}")
            return {"error": str(e)}

# CLI commands for batch processing
@click.group()
def batch():
    """Batch processing of module optimizations"""
    pass

@batch.command()
@click.argument("config_path", type=click.Path(exists=True))
@click.option("--verbose", "-v", is_flag=True, help="Show detailed output")
def process(config_path, verbose=False):
    """Process a batch of modules using a configuration file"""
    try:
        # Set up logger
        log_level = logging.INFO if verbose else logging.WARNING
        setup_logger("batch_processor", level=log_level)
        
        # Process batch
        processor = BatchProcessor()
        results = processor.process_config(config_path)
        
        # Display results
        click.echo(f"\nBatch Processing Results ({results['succeeded']}/{results['total']} succeeded)")
        
        if "error" in results:
            click.echo(f"Error: {results['error']}")
            return 1
            
        # Display module results
        for module in results["modules"]:
            if module["status"] == "success":
                improvement = module.get("improvement", 0)
                if improvement > 0:
                    status = colored(f"+{improvement:.2f}%", "green")
                elif improvement < 0:
                    status = colored(f"{improvement:.2f}%", "red")
                else:
                    status = colored("0.00%", "yellow")
                    
                click.echo(f"  {module['name']}: {status}")
            else:
                click.echo(f"  {module['name']}: {colored('Failed', 'red')} - {module.get('error', 'Unknown error')}")
                
        return 0
            
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        return 1

@batch.command()
@click.option("--limit", "-l", type=int, default=5, help="Maximum number of modules to optimize")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed output")
def auto_optimize(limit, verbose=False):
    """Automatically optimize modules with poor feedback"""
    try:
        # Set up logger
        log_level = logging.INFO if verbose else logging.WARNING
        setup_logger("batch_processor", level=log_level)
        
        # Auto-optimize modules
        processor = BatchProcessor()
        results = processor.auto_optimize_priority_modules(limit)
        
        if "error" in results:
            click.echo(f"Error: {results['error']}")
            return 1
            
        # Display results
        if results["total"] == 0:
            click.echo("No modules identified for optimization")
            return 0
            
        click.echo(f"\nAuto-Optimization Results ({results['succeeded']}/{results['total']} succeeded)")
        
        # Display module results
        for module in results["modules"]:
            if module["status"] == "success":
                improvement = module.get("improvement", 0)
                if improvement > 0:
                    status = colored(f"+{improvement:.2f}%", "green")
                elif improvement < 0:
                    status = colored(f"{improvement:.2f}%", "red")
                else:
                    status = colored("0.00%", "yellow")
                    
                click.echo(f"  {module['name']}: {status}")
            else:
                click.echo(f"  {module['name']}: {colored('Failed', 'red')} - {module.get('error', 'Unknown error')}")
                
        return 0
            
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        return 1

@batch.command()
@click.option("--output", "-o", type=click.Path(), help="Output JSON file for analysis report")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed output")
def analyze(output=None, verbose=False):
    """Analyze optimization performance across modules and models"""
    try:
        # Set up logger
        log_level = logging.INFO if verbose else logging.WARNING
        setup_logger("batch_processor", level=log_level)
        
        # Analyze performance
        processor = BatchProcessor()
        report = processor.analyze_optimization_performance()
        
        if "error" in report:
            click.echo(f"Error: {report['error']}")
            return 1
            
        # Display report summary
        click.echo("\nOptimization Performance Analysis")
        click.echo(f"Total optimizations: {report['overall']['total']}")
        click.echo(f"Success rate: {report['overall']['successes'] / report['overall']['total'] * 100:.2f}%")
        click.echo(f"Average improvement: {report['overall']['avg_improvement']:.2f}%")
        click.echo(f"Optimizations applied: {report['overall']['applied']}")
        
        # Display model performance
        click.echo("\nModel Performance:")
        for model in report['models']:
            success_rate = model['successes'] / model['total'] * 100
            click.echo(f"  {model['target_model']}: {model['avg_improvement']:.2f}% avg improvement, {success_rate:.2f}% success rate")
            
        # Display top modules
        click.echo("\nTop Performing Modules:")
        for module in report['top_modules']:
            click.echo(f"  {module['module_name']}: {module['avg_improvement']:.2f}% avg improvement")
            
        # Save output if specified
        if output:
            with open(output, "w") as f:
                json.dump(report, f, indent=2)
            click.echo(f"\nDetailed report saved to {output}")
            
        return 0
            
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        return 1 