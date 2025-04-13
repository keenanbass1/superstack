#!/usr/bin/env python3
"""
Context Module Optimization Script

This script provides a CLI for optimizing, evaluating, and managing context modules
using DSPy for optimization and PromptFoo for evaluation.
"""

import os
import sys
import glob
import logging
import argparse
import json
import yaml
import re
import difflib
import sqlite3
import tempfile
import shutil
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple, Union
import textwrap

# Add the parent directory to the path to allow importing project modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try importing DSPy
try:
    import dspy
except ImportError:
    print("Error: DSPy not found. Install with: pip install dspy-ai")
    sys.exit(1)

# Logging setup
def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """Set up logging for the script."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    level = getattr(logging, log_level)
    
    handlers = []
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        handlers.append(logging.FileHandler(log_file))
    handlers.append(logging.StreamHandler())
    
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=handlers
    )
    
    return logging.getLogger(__name__)

# Configuration loading
def load_config(config_path: str = "config/dsp_config.yaml") -> Dict[str, Any]:
    """Load DSP configuration from the specified YAML file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Failed to load configuration from {config_path}: {str(e)}")
        sys.exit(1)

class ContextOptimizer:
    """Class for optimizing context modules using DSPy."""
    
    def __init__(self, config_path: str = "config/dsp_config.yaml"):
        """Initialize the optimizer with the given configuration."""
        self.config = self._load_config(config_path)
        self.logger = logging.getLogger(__name__)
        
        # Set up directories
        self.original_dir = self.config['paths']['original_modules_dir']
        self.optimized_dir = self.config['paths']['optimized_modules_dir']
        self.backup_dir = self.config['paths']['backup_modules_dir']
        
        # Create directories if they don't exist
        for directory in [self.original_dir, self.optimized_dir, self.backup_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Configure DSPy with the default model
        self._configure_dspy()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load the configuration file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logging.error(f"Failed to load configuration from {config_path}: {str(e)}")
            sys.exit(1)
    
    def _configure_dspy(self):
        """Configure DSPy with the model from config."""
        default_model = self.config["models"]["default"]
        
        # Find the model configuration
        model_config = None
        for model in self.config["models"]["options"]:
            if model["name"] == default_model:
                model_config = model
                break
        
        if not model_config:
            self.logger.error(f"Model {default_model} not found in configuration")
            sys.exit(1)
        
        # Configure DSPy based on the provider
        provider = model_config.get("provider", "openai")
        if provider == "openai":
            dspy.settings.configure(
                lm=dspy.OpenAI(
                    model=model_config["name"],
                    api_key=os.environ.get("OPENAI_API_KEY"),
                    temperature=model_config.get("temperature", 0.2),
                    max_tokens=model_config.get("max_tokens", 4096)
                )
            )
        elif provider == "anthropic":
            dspy.settings.configure(
                lm=dspy.Anthropic(
                    model=model_config["name"],
                    api_key=os.environ.get("ANTHROPIC_API_KEY"),
                    temperature=model_config.get("temperature", 0.2),
                    max_tokens=model_config.get("max_tokens", 4096)
                )
            )
        else:
            self.logger.error(f"Unsupported provider: {provider}")
            sys.exit(1)
        
        self.logger.info(f"Configured DSPy with model: {model_config['name']}")
    
    def list_modules(self) -> List[str]:
        """List all available context modules."""
        modules = []
        module_files = glob.glob(os.path.join(self.original_dir, "*.md"))
        
        for file_path in module_files:
            modules.append(os.path.basename(file_path))
        
        return sorted(modules)
    
    def _create_backup(self, module_path: str) -> str:
        """Create a backup of the module before optimization."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = os.path.basename(module_path)
        backup_filename = f"{os.path.splitext(filename)[0]}_{timestamp}{os.path.splitext(filename)[1]}"
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        # Create directory if it doesn't exist
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Copy the file
        shutil.copy2(module_path, backup_path)
        self.logger.info(f"Created backup at {backup_path}")
        
        return backup_path
    
    def _extract_module_content(self, module_path: str) -> str:
        """Extract the content of a module from file."""
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.logger.error(f"Failed to read module {module_path}: {str(e)}")
            raise
    
    def _extract_context_blocks(self, content: str) -> List[Dict[str, Any]]:
        """Extract context blocks and their priorities from the module content."""
        blocks = []
        
        # Get the patterns from config
        separator = self.config['dsp']['module_settings']['context_separator']
        priority_pattern = self.config['dsp']['module_settings']['priority_pattern']
        context_pattern = self.config['dsp']['module_settings']['context_pattern']
        
        # Split the content by separator if present
        if separator in content:
            sections = content.split(separator)
        else:
            sections = [content]
        
        for section in sections:
            # Extract priority if present
            priority_match = re.search(priority_pattern, section)
            priority = priority_match.group(1) if priority_match else "medium"
            
            # Extract context if present
            context_match = re.search(context_pattern, section, re.DOTALL)
            context = context_match.group(1).strip() if context_match else section.strip()
            
            blocks.append({
                "priority": priority,
                "content": context
            })
        
        return blocks
    
    def optimize_module(self, module_name: str, target_model: Optional[str] = None) -> Dict[str, Any]:
        """
        Optimize a single context module using DSPy.
        
        Args:
            module_name: Name of the module to optimize
            target_model: Optional model to use for optimization (overrides config default)
            
        Returns:
            Dictionary with optimization results
        """
        # Ensure .md extension
        if not module_name.endswith('.md'):
            module_name = f"{module_name}.md"
        
        # Construct paths
        original_path = os.path.join(self.original_dir, module_name)
        optimized_path = os.path.join(self.optimized_dir, module_name)
        
        # Check if module exists
        if not os.path.exists(original_path):
            error_msg = f"Module {module_name} not found in {self.original_dir}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
        
        # Prepare result dictionary
        result = {
            "module_name": module_name,
            "success": False,
            "original_path": original_path,
            "optimized_path": optimized_path,
            "backup_path": None,
            "error": None
        }
        
        try:
            self.logger.info(f"Optimizing module: {module_name}")
            
            # Create a backup
            result["backup_path"] = self._create_backup(original_path)
            
            # Extract content
            content = self._extract_module_content(original_path)
            result["original_content"] = content
            result["original_tokens"] = len(content.split())
            
            # Extract context blocks
            blocks = self._extract_context_blocks(content)
            result["context_blocks"] = len(blocks)
            
            # Configure DSPy with the target model if specified
            if target_model:
                # Save current model
                current_model = self.config["models"]["default"]
                # Temporarily update the model
                self._configure_dspy_with_model(target_model)
                result["model"] = target_model
            else:
                result["model"] = self.config["models"]["default"]
            
            # Define the DSPy optimization module
            class ModuleOptimizer(dspy.Module):
                def __init__(self):
                    super().__init__()
                    self.optimizer = dspy.ChainOfThought(
                        dspy.Predict("optimized_content")
                    )
                
                def forward(self, content, guidelines):
                    return self.optimizer(
                        content=content,
                        guidelines=guidelines
                    )
            
            # Create optimization guidelines
            optimization_guidelines = """
            Please optimize the provided AI context module content. Your task is to:
            1. Maintain all essential technical information
            2. Improve clarity and conciseness
            3. Preserve the original structure and formatting
            4. Ensure the module remains accurate and aligned with its original purpose
            5. Format important technical terms in code formatting using backticks (`) where appropriate
            6. Preserve any existing code examples and format them properly
            7. Provide detailed and complete information, as this will be used by an AI to answer questions
            8. Structure the content to make it easy to understand and navigate
            """
            
            # Initialize the optimizer
            module_optimizer = ModuleOptimizer()
            
            # Process each block with DSPy
            optimized_blocks = []
            
            for i, block in enumerate(blocks):
                self.logger.info(f"Optimizing block {i+1}/{len(blocks)}")
                
                response = module_optimizer(
                    content=block["content"],
                    guidelines=optimization_guidelines
                )
                
                optimized_blocks.append({
                    "priority": block["priority"],
                    "content": response.optimized_content
                })
            
            # Reconstruct the optimized content
            optimized_content = ""
            for i, block in enumerate(optimized_blocks):
                if i > 0:
                    optimized_content += f"\n{separator}\n"
                
                # Add priority if it was in the original
                if "priority" in block and block["priority"] != "medium":
                    optimized_content += f"#priority: {block['priority']}\n\n"
                
                optimized_content += block["content"]
            
            result["optimized_content"] = optimized_content
            result["optimized_tokens"] = len(optimized_content.split())
            
            # Calculate token reduction
            original_tokens = result["original_tokens"]
            optimized_tokens = result["optimized_tokens"]
            token_reduction = ((original_tokens - optimized_tokens) / original_tokens) * 100 if original_tokens > 0 else 0
            result["token_reduction"] = round(token_reduction, 2)
            
            # Save optimized content
            os.makedirs(os.path.dirname(optimized_path), exist_ok=True)
            with open(optimized_path, 'w', encoding='utf-8') as f:
                f.write(optimized_content)
            
            # Generate diff
            result["diff"] = self.generate_diff(original_path, optimized_path)
            
            # Run PromptFoo tests if enabled
            if self.config.get("evaluation", {}).get("run_tests_after_optimize", False):
                self.logger.info(f"Running PromptFoo tests for module {module_name}")
                try:
                    # Use the new CLI command for running tests
                    module_base = os.path.splitext(module_name)[0]
                    import subprocess
                    
                    # Run the test command using the new CLI integration
                    cmd = ["dev", "context", "test", module_base]
                    
                    # Run the test
                    process = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        check=False
                    )
                    
                    # Store test results
                    result["test_results"] = {
                        "success": process.returncode == 0,
                        "output": process.stdout,
                        "error": process.stderr if process.returncode != 0 else None
                    }
                    
                    if process.returncode == 0:
                        self.logger.info(f"PromptFoo tests passed for module {module_name}")
                    else:
                        self.logger.warning(f"PromptFoo tests failed for module {module_name}")
                except Exception as e:
                    self.logger.warning(f"Error running PromptFoo tests: {str(e)}")
                    result["test_results"] = {
                        "success": False,
                        "error": str(e)
                    }
            
            result["success"] = True
            self.logger.info(f"Successfully optimized module {module_name}")
            self.logger.info(f"Token reduction: {token_reduction:.2f}%")
            
            # Reset DSPy to use the original model if changed
            if target_model:
                self._configure_dspy_with_model(current_model)
            
        except Exception as e:
            error_msg = f"Error optimizing module {module_name}: {str(e)}"
            self.logger.error(error_msg)
            result["error"] = error_msg
        
        return result
    
    def _configure_dspy_with_model(self, model_name: str):
        """Temporarily configure DSPy with a different model."""
        # Find the model configuration
        model_config = None
        for model in self.config["models"]["options"]:
            if model["name"] == model_name:
                model_config = model
                break
        
        if not model_config:
            self.logger.warning(f"Model {model_name} not found in configuration, using default")
            return
        
        # Configure DSPy based on the provider
        provider = model_config.get("provider", "openai")
        if provider == "openai":
            dspy.settings.configure(
                lm=dspy.OpenAI(
                    model=model_config["name"],
                    api_key=os.environ.get("OPENAI_API_KEY"),
                    temperature=model_config.get("temperature", 0.2),
                    max_tokens=model_config.get("max_tokens", 4096)
                )
            )
        elif provider == "anthropic":
            dspy.settings.configure(
                lm=dspy.Anthropic(
                    model=model_config["name"],
                    api_key=os.environ.get("ANTHROPIC_API_KEY"),
                    temperature=model_config.get("temperature", 0.2),
                    max_tokens=model_config.get("max_tokens", 4096)
                )
            )
        
        self.logger.info(f"Reconfigured DSPy with model: {model_config['name']}")
    
    def generate_diff(self, original_path: str, optimized_path: str) -> str:
        """Generate a unified diff between original and optimized files."""
        with open(original_path, 'r', encoding='utf-8') as f:
            original_lines = f.readlines()
        
        with open(optimized_path, 'r', encoding='utf-8') as f:
            optimized_lines = f.readlines()
        
        diff = difflib.unified_diff(
            original_lines,
            optimized_lines,
            fromfile=f"Original: {os.path.basename(original_path)}",
            tofile=f"Optimized: {os.path.basename(optimized_path)}",
            lineterm=''
        )
        
        return '\n'.join(diff)

    def batch_optimize(self, modules: Optional[List[str]] = None, 
                     max_modules: int = 10, 
                     target_model: Optional[str] = None) -> Dict[str, Any]:
        """
        Optimize multiple modules in batch mode.
        
        Args:
            modules: List of module names to optimize (if None, all modules are considered)
            max_modules: Maximum number of modules to optimize
            target_model: Optional model to use for optimization
            
        Returns:
            Dictionary with batch optimization results
        """
        if modules is None:
            # Get all available modules
            all_modules = self.list_modules()
            modules = all_modules[:max_modules]
        else:
            # Ensure all modules have .md extension
            modules = [m if m.endswith('.md') else f"{m}.md" for m in modules]
            # Limit to max_modules
            modules = modules[:max_modules]
        
        self.logger.info(f"Starting batch optimization of {len(modules)} modules")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "target_model": target_model or self.config["models"]["default"],
            "total_modules": len(modules),
            "successful": 0,
            "failed": 0,
            "modules": []
        }
        
        for module_name in modules:
            self.logger.info(f"Processing module: {module_name}")
            
            result = self.optimize_module(module_name, target_model)
            results["modules"].append(result)
            
            if result["success"]:
                results["successful"] += 1
            else:
                results["failed"] += 1
        
        # Calculate average token reduction for successful optimizations
        successful_modules = [m for m in results["modules"] if m["success"]]
        if successful_modules:
            total_reduction = sum(m["token_reduction"] for m in successful_modules)
            avg_reduction = total_reduction / len(successful_modules)
            results["average_token_reduction"] = round(avg_reduction, 2)
        else:
            results["average_token_reduction"] = 0
        
        self.logger.info(f"Batch optimization completed: {results['successful']} successful, {results['failed']} failed")
        if results["successful"] > 0:
            self.logger.info(f"Average token reduction: {results.get('average_token_reduction', 0):.2f}%")
        
        return results

class ContextEvaluator:
    """Class for evaluating the quality of optimized context modules."""
    
    def __init__(self, config_path: str = "config/dsp_config.yaml"):
        """Initialize the evaluator with the given configuration."""
        self.optimizer = ContextOptimizer(config_path)
        self.config = self.optimizer.config
        self.logger = logging.getLogger(__name__)
        
        # Set up temporary directory for evaluations
        self.temp_dir = tempfile.mkdtemp(prefix="context_eval_")
        self.logger.info(f"Created temporary directory for evaluations: {self.temp_dir}")
    
    def __del__(self):
        """Clean up temporary files when done."""
        if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            self.logger.info(f"Removed temporary directory: {self.temp_dir}")
    
    def create_evaluation_config(self, 
                                original_path: str, 
                                optimized_path: str, 
                                test_cases: List[Dict[str, str]],
                                output_path: str) -> str:
        """
        Create a PromptFoo evaluation configuration.
        
        Args:
            original_path: Path to the original module
            optimized_path: Path to the optimized module
            test_cases: List of test cases for evaluation
            output_path: Path to save evaluation results
            
        Returns:
            Path to the created configuration file
        """
        module_name = os.path.basename(original_path)
        config_path = os.path.join(self.temp_dir, f"{os.path.splitext(module_name)[0]}_eval_config.yaml")
        
        # Read the module contents
        with open(original_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        with open(optimized_path, 'r', encoding='utf-8') as f:
            optimized_content = f.read()
        
        # Create PromptFoo configuration
        config = {
            "prompts": [
                {
                    "name": "Original Module",
                    "prompt": "{{prompt}}\n\nContext:\n{{context_original}}",
                    "models": ["openai:gpt-4"]
                },
                {
                    "name": "Optimized Module",
                    "prompt": "{{prompt}}\n\nContext:\n{{context_optimized}}",
                    "models": ["openai:gpt-4"]
                }
            ],
            "providers": [
                {
                    "id": "openai",
                    "config": {
                        "apiKey": "env:OPENAI_API_KEY"
                    }
                }
            ],
            "tests": test_cases,
            "outputPath": output_path,
            "vars": {
                "context_original": original_content,
                "context_optimized": optimized_content
            }
        }
        
        # Write config to file
        with open(config_path, 'w') as f:
            yaml.dump(config, f)
        
        return config_path
    
    def generate_test_cases(self, module_content: str, max_cases: int = 5) -> List[Dict[str, str]]:
        """
        Generate test cases based on module content.
        
        Args:
            module_content: Content of the module
            max_cases: Maximum number of test cases to generate
            
        Returns:
            List of test cases
        """
        # Extract key technical terms from content
        key_terms = self._extract_key_terms(module_content)
        
        # Get test prompts from config
        test_prompts = self.config["evaluation"]["test_prompts"]
        
        # Create test cases
        test_cases = []
        
        # If we have key terms, create test cases for each
        if key_terms:
            for term in key_terms[:max_cases]:
                prompt_template = test_prompts[len(test_cases) % len(test_prompts)]
                prompt = prompt_template.replace("{subject}", term)
                
                test_case = {
                    "vars": {
                        "prompt": prompt
                    },
                    "assert": [
                        {
                            "type": "contains",
                            "value": term
                        },
                        {
                            "type": "similar",
                            "threshold": 0.7
                        }
                    ]
                }
                test_cases.append(test_case)
                
                if len(test_cases) >= max_cases:
                    break
        
        # If we couldn't create enough test cases, add generic ones
        while len(test_cases) < max_cases:
            idx = len(test_cases) % len(test_prompts)
            generic_prompt = test_prompts[idx].replace("{subject}", "this topic")
            
            test_case = {
                "vars": {
                    "prompt": generic_prompt
                },
                "assert": [
                    {
                        "type": "similar",
                        "threshold": 0.7
                    }
                ]
            }
            test_cases.append(test_case)
        
        return test_cases
    
    def _extract_key_terms(self, content: str) -> List[str]:
        """Extract key technical terms from the module content."""
        # Use a simple heuristic: look for terms in headings and code blocks
        terms = []
        
        # Extract headings (###, ##)
        heading_pattern = r'(?:^|\n)#{2,3}\s+([A-Za-z0-9\s_\-]+)'
        headings = re.findall(heading_pattern, content)
        terms.extend([h.strip() for h in headings if len(h.strip()) > 3])
        
        # Extract terms from code blocks (terms in backticks)
        code_pattern = r'`([^`]+)`'
        code_terms = re.findall(code_pattern, content)
        terms.extend([t.strip() for t in code_terms if len(t.strip()) > 3])
        
        # Extract capitalized multi-word terms (likely technical terms)
        cap_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b'
        cap_terms = re.findall(cap_pattern, content)
        terms.extend([t.strip() for t in cap_terms if len(t.strip()) > 3])
        
        # Remove duplicates and limit to reasonable terms
        unique_terms = list(set(terms))
        return [t for t in unique_terms if 3 < len(t) < 30]
    
    def run_evaluation(self, config_path: str) -> Dict[str, Any]:
        """
        Run evaluation using PromptFoo.
        
        Args:
            config_path: Path to PromptFoo configuration
            
        Returns:
            Dictionary with evaluation results
        """
        import subprocess
        import json
        
        output_path = os.path.join(self.temp_dir, "evaluation_results.json")
        
        # Prepare the command
        cmd = [
            "npx", 
            "promptfoo", 
            "eval", 
            "-c", config_path,
            "--output", output_path,
            "--format", "json"
        ]
        
        self.logger.info("Running evaluation with promptfoo")
        
        try:
            # Run the command
            subprocess.run(
                cmd, 
                check=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            
            # Read the results
            with open(output_path, 'r') as f:
                results = json.load(f)
            
            # Process the results to calculate scores
            original_scores = []
            optimized_scores = []
            
            for test in results.get("results", []):
                for output in test.get("outputs", []):
                    # Check if this is from the original or optimized prompt
                    prompt_name = output.get("prompt", {}).get("name", "")
                    
                    # Calculate score based on passing assertions
                    total_assertions = len(output.get("assertions", []))
                    passed_assertions = sum(1 for a in output.get("assertions", []) if a.get("passed", False))
                    score = passed_assertions / total_assertions if total_assertions > 0 else 0
                    
                    if "Original" in prompt_name:
                        original_scores.append(score)
                    elif "Optimized" in prompt_name:
                        optimized_scores.append(score)
            
            # Calculate average scores
            avg_original = sum(original_scores) / len(original_scores) if original_scores else 0
            avg_optimized = sum(optimized_scores) / len(optimized_scores) if optimized_scores else 0
            
            # Calculate improvement percentage
            improvement = ((avg_optimized - avg_original) / avg_original) * 100 if avg_original > 0 else 0
            
            return {
                "original_score": round(avg_original, 2),
                "optimized_score": round(avg_optimized, 2),
                "improvement": round(improvement, 2),
                "raw_results": results
            }
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error running evaluation: {e}")
            return {
                "error": f"Evaluation failed: {str(e)}",
                "original_score": 0,
                "optimized_score": 0,
                "improvement": 0
            }
        except Exception as e:
            self.logger.error(f"Error processing evaluation results: {e}")
            return {
                "error": f"Error processing evaluation: {str(e)}",
                "original_score": 0,
                "optimized_score": 0,
                "improvement": 0
            }
    
    def evaluate_module(self, module_name: str) -> Dict[str, Any]:
        """
        Evaluate a single module's optimization quality.
        
        Args:
            module_name: Name of the module to evaluate
            
        Returns:
            Dictionary with evaluation results
        """
        # Ensure .md extension
        if not module_name.endswith('.md'):
            module_name = f"{module_name}.md"
        
        # Construct paths
        original_path = os.path.join(self.optimizer.original_dir, module_name)
        optimized_path = os.path.join(self.optimizer.optimized_dir, module_name)
        
        # Check if files exist
        if not os.path.exists(original_path):
            error_msg = f"Original module {module_name} not found"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg, "module_name": module_name}
        
        if not os.path.exists(optimized_path):
            error_msg = f"Optimized module {module_name} not found"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg, "module_name": module_name}
        
        result = {
            "module_name": module_name,
            "success": False,
            "original_path": original_path,
            "optimized_path": optimized_path,
            "error": None
        }
        
        try:
            self.logger.info(f"Evaluating module: {module_name}")
            
            # Read module content
            with open(original_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Generate test cases
            max_cases = self.config["evaluation"]["promptfoo"]["vars"]["max_test_cases"]
            test_cases = self.generate_test_cases(original_content, max_cases)
            
            # Create evaluation configuration
            output_path = os.path.join(self.temp_dir, f"{os.path.splitext(module_name)[0]}_results.json")
            config_path = self.create_evaluation_config(
                original_path,
                optimized_path,
                test_cases,
                output_path
            )
            
            # Run evaluation
            eval_results = self.run_evaluation(config_path)
            
            # Merge results
            result.update(eval_results)
            
            # Set success flag
            result["success"] = "error" not in eval_results
            
            if result["success"]:
                self.logger.info(f"Evaluation completed: original score={result['original_score']}, " + 
                                f"optimized score={result['optimized_score']}, " + 
                                f"improvement={result['improvement']}%")
            
        except Exception as e:
            error_msg = f"Error evaluating module {module_name}: {str(e)}"
            self.logger.error(error_msg)
            result["error"] = error_msg
        
        return result
    
    def batch_evaluate(self, modules: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Evaluate multiple modules in batch mode.
        
        Args:
            modules: List of module names to evaluate (if None, all optimized modules are considered)
            
        Returns:
            Dictionary with batch evaluation results
        """
        # If no modules specified, find all modules that have both original and optimized versions
        if modules is None:
            optimized_modules = [os.path.basename(f) for f in 
                                glob.glob(os.path.join(self.optimizer.optimized_dir, "*.md"))]
            
            modules = []
            for module in optimized_modules:
                original_path = os.path.join(self.optimizer.original_dir, module)
                if os.path.exists(original_path):
                    modules.append(module)
        else:
            # Ensure all modules have .md extension
            modules = [m if m.endswith('.md') else f"{m}.md" for m in modules]
        
        self.logger.info(f"Starting batch evaluation of {len(modules)} modules")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_evaluations": len(modules),
            "successful_evaluations": 0,
            "failed_evaluations": 0,
            "improved_count": 0,
            "regressed_count": 0,
            "unchanged_count": 0,
            "average_improvement": 0,
            "improved_modules": [],
            "regressed_modules": [],
            "unchanged_modules": [],
            "failed_modules": []
        }
        
        for module_name in modules:
            self.logger.info(f"Evaluating module: {module_name}")
            
            result = self.evaluate_module(module_name)
            
            if result["success"]:
                results["successful_evaluations"] += 1
                
                # Categorize based on improvement
                improvement = result.get("improvement", 0)
                if improvement > 1:  # More than 1% improvement
                    results["improved_count"] += 1
                    results["improved_modules"].append(result)
                elif improvement < -1:  # More than 1% regression
                    results["regressed_count"] += 1
                    results["regressed_modules"].append(result)
                else:  # Roughly the same
                    results["unchanged_count"] += 1
                    results["unchanged_modules"].append(result)
            else:
                results["failed_evaluations"] += 1
                results["failed_modules"].append(result)
        
        # Calculate average improvement for successful evaluations
        successful_modules = results["improved_modules"] + results["regressed_modules"] + results["unchanged_modules"]
        if successful_modules:
            total_improvement = sum(m.get("improvement", 0) for m in successful_modules)
            avg_improvement = total_improvement / len(successful_modules)
            results["average_improvement"] = round(avg_improvement, 2)
        
        self.logger.info(f"Batch evaluation completed:")
        self.logger.info(f"  - Total: {results['total_evaluations']}")
        self.logger.info(f"  - Successful: {results['successful_evaluations']}")
        self.logger.info(f"  - Improved: {results['improved_count']}")
        self.logger.info(f"  - Regressed: {results['regressed_count']}")
        self.logger.info(f"  - Unchanged: {results['unchanged_count']}")
        self.logger.info(f"  - Average improvement: {results['average_improvement']:.2f}%")
        
        return results

class ContextFeedback:
    """Class for collecting and managing feedback on context modules."""
    
    def __init__(self, config_path: str = "config/dsp_config.yaml"):
        """Initialize with the given configuration."""
        self.config = load_config(config_path)
        self.db_path = self.config.get('paths', {}).get('database', 'data/feedback.db')
        self.logger = logging.getLogger(__name__)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_name TEXT,
            feedback_type TEXT,
            score REAL,
            comments TEXT,
            timestamp TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS optimization_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_name TEXT,
            target_model TEXT,
            original_score REAL,
            optimized_score REAL,
            improvement REAL,
            token_reduction REAL,
            timestamp TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_feedback(self, module_name: str, feedback_type: str, score: float, comments: str = ""):
        """
        Add feedback for a module.
        
        Args:
            module_name: Name of the module
            feedback_type: Type of feedback (positive/negative)
            score: Numeric score (0-10)
            comments: Optional feedback comments
        """
        # Ensure proper extension
        if not module_name.endswith('.md'):
            module_name = f"{module_name}.md"
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO feedback (module_name, feedback_type, score, comments, timestamp) VALUES (?, ?, ?, ?, ?)",
            (module_name, feedback_type, score, comments, datetime.now().isoformat())
        )
        
        conn.commit()
        conn.close()
        
        self.logger.info(f"Added {feedback_type} feedback for {module_name} with score {score}")
    
    def add_optimization_result(self, result: Dict[str, Any]):
        """
        Add optimization result to the database.
        
        Args:
            result: Optimization result dict
        """
        if not result.get("success", False):
            self.logger.warning(f"Skipping failed optimization for {result.get('module_name', 'unknown')}")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO optimization_results 
            (module_name, target_model, original_score, optimized_score, improvement, token_reduction, timestamp) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                result.get("module_name", ""),
                result.get("target_model", ""),
                result.get("original_score", 0),
                result.get("optimized_score", 0),
                result.get("improvement", 0),
                result.get("token_reduction", 0),
                datetime.now().isoformat()
            )
        )
        
        conn.commit()
        conn.close()
        
        self.logger.info(f"Added optimization result for {result.get('module_name', 'unknown')}")
    
    def get_feedback(self, module_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get feedback for a module or all modules.
        
        Args:
            module_name: Optional module name to filter by
            
        Returns:
            List of feedback entries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if module_name:
            if not module_name.endswith('.md'):
                module_name = f"{module_name}.md"
                
            cursor.execute(
                "SELECT * FROM feedback WHERE module_name = ? ORDER BY timestamp DESC",
                (module_name,)
            )
        else:
            cursor.execute("SELECT * FROM feedback ORDER BY module_name, timestamp DESC")
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_optimization_results(self, module_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get optimization results for a module or all modules.
        
        Args:
            module_name: Optional module name to filter by
            
        Returns:
            List of optimization result entries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if module_name:
            if not module_name.endswith('.md'):
                module_name = f"{module_name}.md"
                
            cursor.execute(
                "SELECT * FROM optimization_results WHERE module_name = ? ORDER BY timestamp DESC",
                (module_name,)
            )
        else:
            cursor.execute("SELECT * FROM optimization_results ORDER BY module_name, timestamp DESC")
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def identify_modules_for_optimization(self, min_feedback_count: int = 3, 
                                         negative_threshold: float = 6.0) -> List[str]:
        """
        Identify modules that need optimization based on feedback.
        
        Args:
            min_feedback_count: Minimum number of feedback entries to consider
            negative_threshold: Score below which a module is considered for optimization
            
        Returns:
            List of module names that need optimization
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all module names
        cursor.execute("SELECT DISTINCT module_name FROM feedback")
        all_modules = [row[0] for row in cursor.fetchall()]
        
        need_optimization = []
        
        for module in all_modules:
            # Get feedback count
            cursor.execute("SELECT COUNT(*) FROM feedback WHERE module_name = ?", (module,))
            count = cursor.fetchone()[0]
            
            if count >= min_feedback_count:
                # Calculate average score
                cursor.execute("SELECT AVG(score) FROM feedback WHERE module_name = ?", (module,))
                avg_score = cursor.fetchone()[0]
                
                if avg_score < negative_threshold:
                    need_optimization.append(module)
                    self.logger.info(f"Module {module} needs optimization: avg score {avg_score:.2f} from {count} feedbacks")
        
        conn.close()
        return need_optimization
    
    def export_data(self, output_path: str = "data/feedback_export.json") -> str:
        """
        Export all data to a JSON file.
        
        Args:
            output_path: Path to save the export
            
        Returns:
            Path to the exported file
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        data = {
            "feedback": self.get_feedback(),
            "optimization_results": self.get_optimization_results(),
            "modules_needing_optimization": self.identify_modules_for_optimization(),
            "export_time": datetime.now().isoformat()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        self.logger.info(f"Exported feedback data to {output_path}")
        return output_path


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="DSPy Context Module Optimizer CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
        Examples:
          # List available modules
          python optimize_context.py list
          
          # Optimize a single module
          python optimize_context.py optimize --module introduction.md
          
          # Batch optimize modules
          python optimize_context.py batch-optimize --max 5
          
          # Evaluate an optimized module
          python optimize_context.py evaluate --module introduction.md
          
          # Record feedback for a module
          python optimize_context.py feedback --module introduction.md --type positive --score 8
          
          # Identify modules that need optimization based on feedback
          python optimize_context.py identify
        ''')
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available modules')
    list_parser.add_argument('--config', default='config/dsp_config.yaml', help='Path to config file')
    
    # Optimize command
    optimize_parser = subparsers.add_parser('optimize', help='Optimize a single module')
    optimize_parser.add_argument('--module', required=True, help='Module name to optimize')
    optimize_parser.add_argument('--model', help='Model to use for optimization')
    optimize_parser.add_argument('--config', default='config/dsp_config.yaml', help='Path to config file')
    optimize_parser.add_argument('--output', help='Path to save optimization results JSON')
    
    # Batch optimize command
    batch_parser = subparsers.add_parser('batch-optimize', help='Optimize multiple modules')
    batch_parser.add_argument('--modules', nargs='+', help='List of module names to optimize')
    batch_parser.add_argument('--max', type=int, default=5, help='Maximum number of modules to optimize')
    batch_parser.add_argument('--model', help='Model to use for optimization')
    batch_parser.add_argument('--config', default='config/dsp_config.yaml', help='Path to config file')
    batch_parser.add_argument('--output', help='Path to save batch optimization results JSON')
    
    # Evaluate command
    evaluate_parser = subparsers.add_parser('evaluate', help='Evaluate an optimized module')
    evaluate_parser.add_argument('--module', required=True, help='Module name to evaluate')
    evaluate_parser.add_argument('--config', default='config/dsp_config.yaml', help='Path to config file')
    evaluate_parser.add_argument('--output', help='Path to save evaluation results JSON')
    
    # Batch evaluate command
    batch_eval_parser = subparsers.add_parser('batch-evaluate', help='Evaluate multiple optimized modules')
    batch_eval_parser.add_argument('--modules', nargs='+', help='List of module names to evaluate')
    batch_eval_parser.add_argument('--config', default='config/dsp_config.yaml', help='Path to config file')
    batch_eval_parser.add_argument('--output', help='Path to save batch evaluation results JSON')
    
    # Feedback command
    feedback_parser = subparsers.add_parser('feedback', help='Record feedback for a module')
    feedback_parser.add_argument('--module', required=True, help='Module name')
    feedback_parser.add_argument('--type', required=True, choices=['positive', 'negative'], help='Feedback type')
    feedback_parser.add_argument('--score', required=True, type=float, help='Score (0-10)')
    feedback_parser.add_argument('--comments', default='', help='Optional feedback comments')
    feedback_parser.add_argument('--config', default='config/dsp_config.yaml', help='Path to config file')
    
    # Identify command
    identify_parser = subparsers.add_parser('identify', help='Identify modules that need optimization')
    identify_parser.add_argument('--min-feedback', type=int, default=3, help='Minimum number of feedback entries')
    identify_parser.add_argument('--threshold', type=float, default=6.0, help='Score threshold')
    identify_parser.add_argument('--config', default='config/dsp_config.yaml', help='Path to config file')
    identify_parser.add_argument('--output', help='Path to save identification results JSON')
    
    # Export feedback data command
    export_parser = subparsers.add_parser('export', help='Export feedback and optimization data')
    export_parser.add_argument('--output', default='data/feedback_export.json', help='Path to save export JSON')
    export_parser.add_argument('--config', default='config/dsp_config.yaml', help='Path to config file')
    
    # Global options
    parser.add_argument('--log-level', default='info', 
                       choices=['debug', 'info', 'warning', 'error'], 
                       help='Logging level')
    parser.add_argument('--log-file', help='Log to file instead of console')
    
    return parser.parse_args()


def main():
    """Main entry point for the script."""
    args = parse_arguments()
    
    # Setup logging
    log_level = getattr(logging, args.log_level.upper())
    setup_logging(log_level, args.log_file)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Starting command: {args.command}")
    
    try:
        if args.command == 'list':
            # List available modules
            optimizer = ContextOptimizer(args.config)
            modules = optimizer.list_modules()
            
            print(f"Found {len(modules)} modules:")
            for module in modules:
                print(f"  - {module}")
            
        elif args.command == 'optimize':
            # Optimize a single module
            optimizer = ContextOptimizer(args.config)
            result = optimizer.optimize_module(args.module, args.model)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2)
                logger.info(f"Saved optimization results to {args.output}")
            
            if result['success']:
                print(f"Module {args.module} optimized successfully")
                print(f"Token reduction: {result['token_reduction']:.2f}%")
                print(f"Optimized file saved to: {result['optimized_path']}")
            else:
                print(f"Failed to optimize module {args.module}")
                print(f"Error: {result.get('error', 'Unknown error')}")
            
        elif args.command == 'batch-optimize':
            # Batch optimize modules
            optimizer = ContextOptimizer(args.config)
            results = optimizer.batch_optimize(args.modules, args.max, args.model)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2)
                logger.info(f"Saved batch optimization results to {args.output}")
            
            print(f"Batch optimization completed:")
            print(f"  - Total: {results['total_modules']}")
            print(f"  - Successful: {results['successful']}")
            print(f"  - Failed: {results['failed']}")
            if results['successful'] > 0:
                print(f"  - Average token reduction: {results['average_token_reduction']:.2f}%")
            
        elif args.command == 'evaluate':
            # Evaluate a single module
            evaluator = ContextEvaluator(args.config)
            result = evaluator.evaluate_module(args.module)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2)
                logger.info(f"Saved evaluation results to {args.output}")
            
            if result['success']:
                print(f"Module {args.module} evaluated successfully")
                print(f"Original score: {result['original_score']:.2f}")
                print(f"Optimized score: {result['optimized_score']:.2f}")
                print(f"Improvement: {result['improvement']:.2f}%")
            else:
                print(f"Failed to evaluate module {args.module}")
                print(f"Error: {result.get('error', 'Unknown error')}")
            
        elif args.command == 'batch-evaluate':
            # Batch evaluate modules
            evaluator = ContextEvaluator(args.config)
            results = evaluator.batch_evaluate(args.modules)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2)
                logger.info(f"Saved batch evaluation results to {args.output}")
            
            print(f"Batch evaluation completed:")
            print(f"  - Total: {results['total_evaluations']}")
            print(f"  - Successful: {results['successful_evaluations']}")
            print(f"  - Improved: {results['improved_count']}")
            print(f"  - Regressed: {results['regressed_count']}")
            print(f"  - Unchanged: {results['unchanged_count']}")
            print(f"  - Average improvement: {results['average_improvement']:.2f}%")
            
        elif args.command == 'feedback':
            # Record feedback
            feedback_manager = ContextFeedback(args.config)
            feedback_manager.add_feedback(args.module, args.type, args.score, args.comments)
            
            print(f"Recorded {args.type} feedback for {args.module} with score {args.score}")
            
        elif args.command == 'identify':
            # Identify modules that need optimization
            feedback_manager = ContextFeedback(args.config)
            modules = feedback_manager.identify_modules_for_optimization(
                args.min_feedback, args.threshold
            )
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump({'modules_for_optimization': modules}, f, indent=2)
                logger.info(f"Saved identification results to {args.output}")
            
            print(f"Found {len(modules)} modules that need optimization:")
            for module in modules:
                print(f"  - {module}")
            
        elif args.command == 'export':
            # Export feedback data
            feedback_manager = ContextFeedback(args.config)
            output_path = feedback_manager.export_data(args.output)
            
            print(f"Exported feedback data to {output_path}")
            
        else:
            # No command or unknown command
            print("No command specified. Use --help for usage information.")
    
    except Exception as e:
        logger.error(f"Error in command {args.command}: {str(e)}")
        print(f"Error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 