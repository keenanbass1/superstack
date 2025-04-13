import os
import json
import yaml
import shutil
import logging
import tempfile
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any

from .utils import (
    setup_logger, 
    ensure_dir, 
    extract_module_name, 
    read_file_content,
    write_json,
    read_json
)

class ContextEvaluator:
    """
    A class to evaluate the effectiveness of AI context modules.
    Uses PromptFoo for evaluation.
    """
    
    def __init__(self, config_path: str):
        """
        Initialize the ContextEvaluator.
        
        Args:
            config_path: Path to the configuration file
        """
        self.logger = setup_logger('context_evaluator')
        
        # Create a temporary directory for evaluation files
        self.temp_dir = tempfile.mkdtemp(prefix="context_eval_")
        self.logger.info(f"Created temporary directory for evaluation: {self.temp_dir}")
        
        # Import optimizer for convenience
        from .optimizer import ContextOptimizer
        self.optimizer = ContextOptimizer(config_path)
        
        self.logger.info("ContextEvaluator initialized")
        
    def __del__(self):
        """
        Clean up temporary files on deletion.
        """
        try:
            if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                self.logger.info(f"Cleaned up temporary directory: {self.temp_dir}")
        except Exception as e:
            self.logger.error(f"Error cleaning up temporary directory: {str(e)}")
    
    def create_evaluation_config(
        self, 
        original_path: str, 
        optimized_path: str, 
        test_cases: List[Dict],
        output_path: Optional[str] = None
    ) -> str:
        """
        Create a PromptFoo configuration for evaluating original vs. optimized modules.
        
        Args:
            original_path: Path to the original module
            optimized_path: Path to the optimized module
            test_cases: List of test case dictionaries
            output_path: Path to save the output (default: a temporary file)
            
        Returns:
            str: Path to the created configuration file
        """
        if not output_path:
            output_path = os.path.join(self.temp_dir, "eval_config.yaml")
        
        # Basic PromptFoo configuration
        config = {
            "prompts": [
                {
                    "name": "original",
                    "path": original_path
                },
                {
                    "name": "optimized",
                    "path": optimized_path
                }
            ],
            "providers": [
                {
                    "id": "openai:gpt-4-turbo",
                    "config": {
                        "model": "gpt-4-turbo"
                    }
                }
            ],
            "testCases": test_cases,
            "evaluators": [
                {
                    "id": "factuality",
                    "config": {
                        "threshold": 0.7
                    }
                },
                {
                    "id": "relevance",
                    "config": {
                        "threshold": 0.7
                    }
                },
                {
                    "id": "coherence"
                }
            ],
            "options": {
                "showProgressBar": True,
                "cache": True
            }
        }
        
        # Write the configuration
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        self.logger.info(f"Created evaluation configuration at {output_path}")
        return output_path
    
    def generate_test_cases(self, module_content: str, num_cases: int = 5) -> List[Dict]:
        """
        Generate test cases based on module content.
        
        Args:
            module_content: The content of the module
            num_cases: Number of test cases to generate
            
        Returns:
            list: List of test case dictionaries
        """
        test_cases = []
        
        try:
            # Extract context blocks from the module content
            context_blocks = self._extract_context_blocks(module_content)
            
            if not context_blocks:
                self.logger.warning("No context blocks found in module content")
                # Create generic test cases if no context blocks found
                test_cases = [
                    {
                        "vars": {
                            "query": "Explain the main concepts in this document"
                        },
                        "assert": [
                            {
                                "type": "javascript",
                                "value": "output.length > 50"
                            }
                        ]
                    },
                    {
                        "vars": {
                            "query": "What are the key features described in this module?"
                        },
                        "assert": [
                            {
                                "type": "javascript",
                                "value": "output.length > 50"
                            }
                        ]
                    }
                ]
                return test_cases
            
            # Extract key terms for assertions
            key_terms = self._extract_key_terms(module_content)
            
            # Create test cases based on context blocks
            for name, block in list(context_blocks.items())[:num_cases]:
                # Create a prompt based on the context
                prompt = f"What is the purpose of {name}? Explain it in detail."
                
                # Create assertions for this test case
                assertions = [
                    {
                        "type": "javascript",
                        "value": "output.length > 100"  # Ensure substantive response
                    }
                ]
                
                # Add assertions to check for key terms
                for term in key_terms[:3]:  # Use up to 3 key terms per test case
                    # Check if the term is related to this context
                    if term.lower() in block.lower() or term.lower() in name.lower():
                        assertions.append({
                            "type": "contains",
                            "value": term
                        })
                
                test_cases.append({
                    "vars": {
                        "query": prompt
                    },
                    "assert": assertions
                })
            
            # If we don't have enough test cases, add some generic ones
            while len(test_cases) < num_cases:
                test_cases.append({
                    "vars": {
                        "query": f"How would you implement the functionality described in this module?"
                    },
                    "assert": [
                        {
                            "type": "javascript",
                            "value": "output.length > 50"
                        }
                    ]
                })
            
        except Exception as e:
            self.logger.error(f"Error generating test cases: {str(e)}")
            # Return some fallback test cases
            test_cases = [
                {
                    "vars": {
                        "query": "Summarize the key points in this module"
                    },
                    "assert": [
                        {
                            "type": "javascript",
                            "value": "output.length > 50"
                        }
                    ]
                }
            ]
        
        return test_cases
    
    def _extract_context_blocks(self, content: str) -> Dict[str, str]:
        """
        Extract context blocks from module content.
        
        Args:
            content: Module content
            
        Returns:
            dict: Mapping of context names to content
        """
        context_blocks = {}
        try:
            # Find all <context> tags
            context_pattern = re.compile(r'<context\s+name="([^"]+)"[^>]*>(.*?)</context>', re.DOTALL)
            
            for match in context_pattern.finditer(content):
                name = match.group(1)
                block_content = match.group(2).strip()
                context_blocks[name] = block_content
                
        except Exception as e:
            self.logger.error(f"Error extracting context blocks: {str(e)}")
            
        return context_blocks
    
    def _extract_key_terms(self, content: str, max_terms: int = 10) -> List[str]:
        """
        Extract key technical terms from the content for assertion validation.
        
        Args:
            content: Module content
            max_terms: Maximum number of terms to extract
            
        Returns:
            list: List of key terms
        """
        try:
            # Simple approach: look for capitalized words and phrases
            # This could be enhanced with NLP approaches in a real implementation
            term_pattern = re.compile(r'\b([A-Z][a-zA-Z0-9]*(?:\s+[A-Z][a-zA-Z0-9]*)*)\b')
            matches = term_pattern.findall(content)
            
            # Filter short terms and duplicates
            key_terms = []
            seen = set()
            
            for term in matches:
                if len(term) > 3 and term not in seen and not term.lower() in ['this', 'that', 'the', 'and', 'for']:
                    key_terms.append(term)
                    seen.add(term)
                    
                    if len(key_terms) >= max_terms:
                        break
            
            return key_terms
            
        except Exception as e:
            self.logger.error(f"Error extracting key terms: {str(e)}")
            return []
    
    def run_evaluation(self, config_path: str) -> Dict:
        """
        Run the evaluation using PromptFoo.
        
        Args:
            config_path: Path to the evaluation configuration file
            
        Returns:
            dict: Evaluation results with scores
        """
        try:
            # Command to run PromptFoo evaluation
            cmd = [
                "npx", "promptfoo", "eval",
                "--config", config_path,
                "--output", "json",
                "--no-table"
            ]
            
            self.logger.info(f"Running evaluation command: {' '.join(cmd)}")
            
            # Run the evaluation process
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse the output
            try:
                output = json.loads(result.stdout)
                
                # Calculate scores for original and optimized versions
                scores = {
                    "original": {
                        "total": 0,
                        "passed": 0,
                        "score": 0.0
                    },
                    "optimized": {
                        "total": 0,
                        "passed": 0,
                        "score": 0.0
                    }
                }
                
                # Process evaluation results
                if "results" in output:
                    for test_result in output["results"]:
                        for prompt_result in test_result.get("promptResults", []):
                            prompt_name = prompt_result.get("prompt", {}).get("name", "")
                            
                            if prompt_name in ["original", "optimized"]:
                                scores[prompt_name]["total"] += 1
                                
                                # Check if assertion passed
                                if prompt_result.get("success", False):
                                    scores[prompt_name]["passed"] += 1
                
                # Calculate percentage scores
                for version in ["original", "optimized"]:
                    if scores[version]["total"] > 0:
                        scores[version]["score"] = (scores[version]["passed"] / scores[version]["total"]) * 100
                
                # Calculate improvement
                improvement = 0
                if scores["original"]["score"] > 0:
                    improvement = ((scores["optimized"]["score"] - scores["original"]["score"]) 
                                  / scores["original"]["score"]) * 100
                
                return {
                    "success": True,
                    "scores": scores,
                    "improvement": improvement,
                    "raw_results": output
                }
                
            except json.JSONDecodeError as e:
                error_msg = f"Error parsing evaluation output: {str(e)}"
                self.logger.error(error_msg)
                self.logger.debug(f"Evaluation stdout: {result.stdout}")
                return {"success": False, "error": error_msg}
                
        except subprocess.CalledProcessError as e:
            error_msg = f"Evaluation process failed: {str(e)}"
            self.logger.error(error_msg)
            self.logger.debug(f"Evaluation stdout: {e.stdout}")
            self.logger.debug(f"Evaluation stderr: {e.stderr}")
            return {"success": False, "error": error_msg}
            
        except Exception as e:
            error_msg = f"Error running evaluation: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def evaluate_module(self, original_path: str, optimized_path: Optional[str] = None) -> Dict:
        """
        Evaluate a module by comparing original and optimized versions.
        
        Args:
            original_path: Path to the original module
            optimized_path: Path to the optimized module (if None, will look in default location)
            
        Returns:
            dict: Evaluation results
        """
        try:
            # Check if original module exists
            original_path = Path(original_path)
            if not original_path.exists():
                error_msg = f"Original module not found: {original_path}"
                self.logger.error(error_msg)
                return {"success": False, "error": error_msg}
            
            # Resolve optimized path if not provided
            if not optimized_path:
                optimized_dir = self.optimizer.config.get('optimized_dir', 'optimized')
                optimized_path = Path(optimized_dir) / original_path.name
            else:
                optimized_path = Path(optimized_path)
            
            # Check if optimized module exists
            if not optimized_path.exists():
                error_msg = f"Optimized module not found: {optimized_path}"
                self.logger.error(error_msg)
                return {"success": False, "error": error_msg}
            
            # Read module content
            original_content = read_file_content(original_path)
            
            # Generate test cases
            test_cases = self.generate_test_cases(original_content)
            
            # Create evaluation configuration
            config_path = self.create_evaluation_config(
                str(original_path),
                str(optimized_path),
                test_cases
            )
            
            # Run the evaluation
            eval_results = self.run_evaluation(config_path)
            
            if not eval_results.get("success", False):
                return eval_results
            
            # Extract module name for reporting
            module_name = extract_module_name(original_path)
            
            # Prepare the final results
            results = {
                "success": True,
                "module_name": module_name,
                "original_path": str(original_path),
                "optimized_path": str(optimized_path),
                "scores": eval_results.get("scores", {}),
                "improvement": eval_results.get("improvement", 0),
                "recommendation": "neutral"
            }
            
            # Add recommendation based on improvement
            if results["improvement"] > 10:
                results["recommendation"] = "apply"
                self.logger.info(f"Module '{module_name}' shows significant improvement: {results['improvement']:.2f}%")
            elif results["improvement"] < -5:
                results["recommendation"] = "reject"
                self.logger.info(f"Module '{module_name}' shows regression: {results['improvement']:.2f}%")
            else:
                self.logger.info(f"Module '{module_name}' shows neutral results: {results['improvement']:.2f}%")
            
            return results
            
        except Exception as e:
            error_msg = f"Error evaluating module: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def batch_evaluate(self, module_paths: Optional[List[str]] = None, output_path: Optional[str] = None) -> Dict:
        """
        Evaluate multiple modules and summarize results.
        
        Args:
            module_paths: List of module paths to evaluate (None for all modules)
            output_path: Path to save the evaluation results
            
        Returns:
            dict: Batch evaluation results
        """
        # If no module paths provided, get all modules
        if not module_paths:
            module_paths = self.optimizer.list_modules()
            
        if not module_paths:
            error_msg = "No modules found to evaluate"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
        
        results = {
            "success": True,
            "total": len(module_paths),
            "evaluated": 0,
            "improved": [],
            "regressed": [],
            "neutral": [],
            "failed": [],
            "average_improvement": 0.0,
            "modules": []
        }
        
        total_improvement = 0.0
        
        for module_path in module_paths:
            self.logger.info(f"Evaluating module: {module_path}")
            
            eval_result = self.evaluate_module(module_path)
            results["modules"].append(eval_result)
            
            if eval_result.get("success", False):
                results["evaluated"] += 1
                
                improvement = eval_result.get("improvement", 0)
                total_improvement += improvement
                
                module_info = {
                    "module_name": eval_result.get("module_name", ""),
                    "path": module_path,
                    "improvement": improvement
                }
                
                # Categorize based on improvement
                if improvement > 10:
                    results["improved"].append(module_info)
                elif improvement < -5:
                    results["regressed"].append(module_info)
                else:
                    results["neutral"].append(module_info)
            else:
                results["failed"].append({
                    "module_name": extract_module_name(module_path),
                    "path": module_path,
                    "error": eval_result.get("error", "Unknown error")
                })
        
        # Calculate average improvement
        if results["evaluated"] > 0:
            results["average_improvement"] = total_improvement / results["evaluated"]
        
        # Save results if output path is provided
        if output_path:
            write_json(results, output_path)
            self.logger.info(f"Evaluation results saved to {output_path}")
        
        self.logger.info(f"Batch evaluation complete. "
                      f"Evaluated: {results['evaluated']}/{results['total']}, "
                      f"Average improvement: {results['average_improvement']:.2f}%")
        
        return results 