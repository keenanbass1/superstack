import os
import json
import yaml
import tempfile
import subprocess
import re
import shutil
import logging
from pathlib import Path
import uuid
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('context_evaluator')

class ContextEvaluator:
    """Evaluates performance of original vs optimized context modules"""
    
    def __init__(self, context_dir, config_path=None):
        """
        Initialize with path to context modules directory
        
        Args:
            context_dir: Path to context modules directory
            config_path: Optional path to configuration file
        """
        from dspy_bridge import ContextOptimizer
        
        self.context_dir = Path(context_dir)
        self.optimizer = ContextOptimizer(context_dir, config_path)
        self.config = self.optimizer.config
        self.eval_temp_dir = Path(tempfile.mkdtemp())
        logger.info(f"Created temporary evaluation directory: {self.eval_temp_dir}")
        
    def create_evaluation_config(self, original_path, optimized_path, test_cases, output_path=None):
        """
        Create a YAML configuration for PromptFoo to evaluate original vs optimized module
        
        Args:
            original_path: Path to original module
            optimized_path: Path to optimized module
            test_cases: List of test cases for evaluation
            output_path: Optional path to save YAML config
            
        Returns:
            Path to the created YAML config file
        """
        # Determine output path if not provided
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"eval_config_{Path(original_path).stem}_{timestamp}.yaml"
            output_path = self.eval_temp_dir / filename
        else:
            output_path = Path(output_path)
            
        # Create PromptFoo configuration
        config = {
            "prompts": [
                {
                    "name": "Original",
                    "provider": {
                        "id": self.config.get("default_model", "claude"),
                        "system": "You are a helpful AI assistant.",
                    },
                    "prompt": f"{{{{ includeFile('{original_path}') }}}}\\n\\n{{{{userPrompt}}}}"
                },
                {
                    "name": "Optimized",
                    "provider": {
                        "id": self.config.get("default_model", "claude"),
                        "system": "You are a helpful AI assistant.",
                    },
                    "prompt": f"{{{{ includeFile('{optimized_path}') }}}}\\n\\n{{{{userPrompt}}}}"
                }
            ],
            "tests": test_cases,
            "sharing": {
                "enabled": False
            }
        }
        
        # Write config to file
        with open(output_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
            
        logger.info(f"Created evaluation config at {output_path}")
        return output_path
        
    def generate_test_cases(self, module_content, num_tests=3):
        """
        Generate test cases based on module content
        
        Args:
            module_content: Content of the module to analyze
            num_tests: Number of test cases to generate
            
        Returns:
            List of test case objects for PromptFoo
        """
        test_cases = []
        
        try:
            # Extract context blocks from module
            context_blocks = re.findall(r'```context\n(.*?)\n```', module_content, re.DOTALL)
            
            if not context_blocks:
                # Fallback: use the whole module content
                logger.warning("No context blocks found, using whole module content")
                prompts = [
                    "What is the main purpose of this module?",
                    "Give me an example of how to use this information.",
                    "Explain the key concepts from this module."
                ]
            else:
                # Generate prompts based on context blocks
                prompts = []
                for block in context_blocks[:num_tests]:
                    # Extract key information to create relevant prompts
                    lines = block.strip().split('\n')
                    if len(lines) > 2:
                        topic = lines[0]
                        prompts.append(f"Explain {topic} in detail.")
                    
                # Fill with generic prompts if needed
                while len(prompts) < num_tests:
                    prompts.append(f"What are the key points from this context module?")
            
            # Extract technical terms for validation
            key_terms = self._extract_key_terms(module_content)
            
            # Create test cases
            for i, prompt in enumerate(prompts[:num_tests]):
                test_case = {
                    "vars": {
                        "userPrompt": prompt
                    },
                    "assert": [
                        {
                            "type": "contains-any",
                            "value": key_terms[:5],  # Use up to 5 key terms
                            "description": "Response contains key technical terms"
                        },
                        {
                            "type": "javascript",
                            "value": "outputs[0].length > 50 && outputs[0].length < 3000",
                            "description": "Response has reasonable length"
                        },
                        {
                            "type": "not-contains-any",
                            "value": ["As an AI", "I don't have", "I cannot", "I'm unable"],
                            "description": "Response avoids AI self-references"
                        }
                    ]
                }
                test_cases.append(test_case)
                
            logger.info(f"Generated {len(test_cases)} test cases for evaluation")
            return test_cases
            
        except Exception as e:
            logger.error(f"Error generating test cases: {e}")
            # Fallback to basic test cases
            return [
                {
                    "vars": {
                        "userPrompt": "What is the main purpose of this module?"
                    },
                    "assert": [
                        {
                            "type": "javascript",
                            "value": "outputs[0].length > 50",
                            "description": "Response has reasonable length"
                        }
                    ]
                }
            ]
    
    def _extract_key_terms(self, content):
        """
        Extract technical terms from content for assertion validation
        
        Args:
            content: Module content to analyze
            
        Returns:
            List of key technical terms
        """
        # Simple extraction of capitalized terms and terms in code blocks
        technical_terms = []
        
        # Extract terms from code blocks
        code_blocks = re.findall(r'```(?:(?!```).)*```', content, re.DOTALL)
        for block in code_blocks:
            # Extract words that look like functions, classes, or variables
            terms = re.findall(r'\b([A-Za-z][A-Za-z0-9_]*)\b', block)
            technical_terms.extend([t for t in terms if len(t) > 3])
        
        # Extract capitalized terms (likely to be technical concepts)
        cap_terms = re.findall(r'\b([A-Z][A-Za-z0-9_]*)\b', content)
        technical_terms.extend([t for t in cap_terms if len(t) > 3])
        
        # Extract terms in backticks (often technical references)
        backtick_terms = re.findall(r'`([^`]+)`', content)
        technical_terms.extend(backtick_terms)
        
        # Remove duplicates and limit
        unique_terms = list(set(technical_terms))
        return unique_terms[:10]  # Return up to 10 unique terms
        
    def run_evaluation(self, config_path):
        """
        Run PromptFoo evaluation and process results
        
        Args:
            config_path: Path to PromptFoo YAML config
            
        Returns:
            Dictionary with evaluation results and scores
        """
        try:
            # Ensure PromptFoo is installed
            try:
                subprocess.run(["promptfoo", "--version"], check=True, capture_output=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                logger.warning("PromptFoo not found, attempting to install...")
                subprocess.run(["npm", "install", "-g", "promptfoo"], check=True)
            
            # Run evaluation
            logger.info(f"Running evaluation with config: {config_path}")
            result_path = self.eval_temp_dir / f"results_{uuid.uuid4()}.json"
            
            # Run promptfoo eval command
            cmd = [
                "promptfoo", "eval", 
                "--config", str(config_path),
                "--output", str(result_path),
                "--format", "json"
            ]
            
            process = subprocess.run(cmd, capture_output=True, text=True)
            
            if process.returncode != 0:
                logger.error(f"Evaluation failed: {process.stderr}")
                return {
                    "success": False,
                    "error": process.stderr
                }
            
            # Parse results
            if not result_path.exists():
                logger.error(f"Result file not found: {result_path}")
                return {
                    "success": False,
                    "error": "Evaluation result file not found"
                }
                
            with open(result_path, 'r') as f:
                results = json.load(f)
                
            # Calculate scores
            total_tests = len(results.get("results", []))
            if total_tests == 0:
                return {"success": False, "error": "No test results found"}
                
            original_score = 0
            optimized_score = 0
            
            for result in results.get("results", []):
                # Get scores for each prompt variant
                for prompt_result in result.get("promptResults", []):
                    prompt_name = prompt_result.get("prompt", {}).get("name", "")
                    score = sum(1 for a in prompt_result.get("assertion", []) if a.get("passed", False))
                    total = len(prompt_result.get("assertion", []))
                    
                    if prompt_name == "Original":
                        original_score += score / total if total > 0 else 0
                    elif prompt_name == "Optimized":
                        optimized_score += score / total if total > 0 else 0
            
            # Normalize scores
            original_score = original_score / total_tests * 100 if total_tests > 0 else 0
            optimized_score = optimized_score / total_tests * 100 if total_tests > 0 else 0
            
            # Calculate improvement
            improvement = optimized_score - original_score
            improvement_percent = (improvement / original_score * 100) if original_score > 0 else 0
            
            return {
                "success": True,
                "original_score": round(original_score, 2),
                "optimized_score": round(optimized_score, 2),
                "improvement": round(improvement, 2),
                "improvement_percent": round(improvement_percent, 2),
                "total_tests": total_tests
            }
            
        except Exception as e:
            logger.error(f"Error running evaluation: {e}")
            return {"success": False, "error": str(e)}
            
    def evaluate_module(self, module_name, target_model="claude"):
        """
        Evaluate performance of original vs optimized module
        
        Args:
            module_name: Name of the module to evaluate
            target_model: Target model for evaluation
            
        Returns:
            Dictionary with evaluation results
        """
        try:
            # Find module paths
            original_path = None
            for path in self.context_dir.glob(f"**/{module_name}.md"):
                if "_optimized" not in str(path) and "_backups" not in str(path):
                    original_path = path
                    break
                    
            if not original_path:
                logger.error(f"Original module not found: {module_name}")
                return {"success": False, "error": f"Original module not found: {module_name}"}
                
            optimized_path = self.context_dir / "_optimized" / f"{module_name}.md"
            if not optimized_path.exists():
                logger.error(f"Optimized module not found: {optimized_path}")
                return {"success": False, "error": f"Optimized module not found: {optimized_path}"}
            
            # Load content
            original_content = self.optimizer.load_context_module(original_path)
            
            # Generate test cases
            test_cases = self.generate_test_cases(original_content)
            
            # Create evaluation config
            config_path = self.create_evaluation_config(original_path, optimized_path, test_cases)
            
            # Run evaluation
            evaluation = self.run_evaluation(config_path)
            
            # Add module info to results
            evaluation["module_name"] = module_name
            evaluation["target_model"] = target_model
            evaluation["original_path"] = str(original_path)
            evaluation["optimized_path"] = str(optimized_path)
            
            # Add recommendation
            if evaluation.get("success", False):
                improvement = evaluation.get("improvement", 0)
                if improvement > 5:
                    evaluation["recommendation"] = "apply_optimization"
                elif improvement > 0:
                    evaluation["recommendation"] = "consider_optimization"
                else:
                    evaluation["recommendation"] = "keep_original"
                
            logger.info(f"Evaluation for {module_name}: {evaluation}")
            return evaluation
            
        except Exception as e:
            logger.error(f"Error evaluating module {module_name}: {e}")
            return {"success": False, "error": str(e), "module_name": module_name}
            
    def batch_evaluate(self, module_names=None, target_model="claude"):
        """
        Evaluate multiple modules in batch
        
        Args:
            module_names: List of module names to evaluate or None for all
            target_model: Target model for evaluation
            
        Returns:
            Dictionary with batch evaluation results
        """
        if module_names is None or module_names == ["all"]:
            # Get all modules that have optimized versions
            optimized_modules = []
            for path in self.context_dir.glob("_optimized/**/*.md"):
                rel_path = path.relative_to(self.context_dir / "_optimized")
                module_name = str(rel_path.with_suffix(''))
                optimized_modules.append(module_name)
                
            module_names = optimized_modules
            
        logger.info(f"Starting batch evaluation of {len(module_names)} modules")
        
        results = []
        improved_modules = []
        regressed_modules = []
        unchanged_modules = []
        failed_modules = []
        
        total_improvement = 0
        evaluation_count = 0
        
        for module_name in module_names:
            result = self.evaluate_module(module_name, target_model=target_model)
            results.append(result)
            
            if not result.get("success", False):
                failed_modules.append(module_name)
                continue
                
            evaluation_count += 1
            improvement = result.get("improvement", 0)
            total_improvement += improvement
            
            if improvement > 1:
                improved_modules.append({
                    "module": module_name,
                    "improvement": improvement,
                    "score": result.get("optimized_score", 0)
                })
            elif improvement < -1:
                regressed_modules.append({
                    "module": module_name,
                    "regression": -improvement,
                    "score": result.get("optimized_score", 0)
                })
            else:
                unchanged_modules.append({
                    "module": module_name,
                    "score": result.get("optimized_score", 0)
                })
        
        # Sort results by improvement/regression
        improved_modules.sort(key=lambda x: x["improvement"], reverse=True)
        regressed_modules.sort(key=lambda x: x["regression"], reverse=True)
        
        # Calculate average improvement
        avg_improvement = total_improvement / evaluation_count if evaluation_count > 0 else 0
        
        return {
            "success": evaluation_count > 0,
            "total": len(results),
            "successful": evaluation_count,
            "failed": len(failed_modules),
            "avg_improvement": round(avg_improvement, 2),
            "improved_count": len(improved_modules),
            "regressed_count": len(regressed_modules),
            "unchanged_count": len(unchanged_modules),
            "improved_modules": improved_modules,
            "regressed_modules": regressed_modules,
            "unchanged_modules": unchanged_modules,
            "failed_modules": failed_modules
        }

if __name__ == "__main__":
    # Command-line interface
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate context module optimizations")
    parser.add_argument("context_dir", help="Path to context modules directory")
    parser.add_argument("module", help="Module name to evaluate or 'all' for batch mode")
    parser.add_argument("--target", "-t", default="claude", help="Target model (claude, gpt)")
    parser.add_argument("--config", "-c", help="Path to configuration file")
    parser.add_argument("--output", "-o", help="Path to save evaluation results")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Set log level based on verbose flag
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    evaluator = ContextEvaluator(args.context_dir, args.config)
    
    if args.module.lower() == "all":
        # Batch mode
        result = evaluator.batch_evaluate(target_model=args.target)
        
        # Print summary
        print(f"\nEvaluation Summary:")
        print(f"Total modules evaluated: {result['successful']}/{result['total']}")
        print(f"Average improvement: {result['avg_improvement']}%")
        print(f"Improved modules: {result['improved_count']}")
        print(f"Unchanged modules: {result['unchanged_count']}")
        print(f"Regressed modules: {result['regressed_count']}")
        print(f"Failed evaluations: {result['failed']}")
        
        if result["improved_count"] > 0:
            print("\nTop improved modules:")
            for module in result["improved_modules"][:5]:  # Show top 5
                print(f"  {module['module']}: +{module['improvement']}%")
                
        if result["regressed_count"] > 0:
            print("\nRegressed modules:")
            for module in result["regressed_modules"][:5]:  # Show top 5
                print(f"  {module['module']}: -{module['regression']}%")
    else:
        # Single module mode
        result = evaluator.evaluate_module(args.module, target_model=args.target)
        
        if result["success"]:
            print(f"\nEvaluation for {args.module}:")
            print(f"Original score: {result['original_score']}%")
            print(f"Optimized score: {result['optimized_score']}%")
            print(f"Improvement: {result['improvement']}% ({result['improvement_percent']}%)")
            print(f"Recommendation: {result['recommendation']}")
        else:
            print(f"Evaluation failed: {result.get('error', 'Unknown error')}")
    
    # Save results if output path provided
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nResults saved to {args.output}") 