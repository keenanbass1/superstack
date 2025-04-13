import os
import json
import tempfile
import logging
import difflib
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any

import dspy
from .utils import (
    setup_logger, 
    load_yaml_config, 
    ensure_dir, 
    backup_file, 
    extract_module_name, 
    read_file_content,
    write_file_content
)

class ContextOptimizer:
    """
    A class to optimize AI context modules using DSPy.
    """
    
    def __init__(self, config_path: str):
        """
        Initialize the ContextOptimizer with the given configuration.
        
        Args:
            config_path: Path to the configuration file
        """
        self.logger = setup_logger('context_optimizer')
        self.config = self._load_config(config_path)
        self.backup_dir = self.config.get('backup_dir', 'backups/context_modules')
        
        # Ensure required directories exist
        ensure_dir(self.backup_dir)
        ensure_dir(self.config.get('optimized_dir', 'optimized'))
        
        # Configure DSPy
        self._configure_dspy()
        
        self.logger.info("ContextOptimizer initialized")
    
    def _load_config(self, config_path: str) -> Dict:
        """
        Load configuration from the given path.
        
        Args:
            config_path: Path to the configuration file
            
        Returns:
            dict: Configuration dictionary
        """
        try:
            config = load_yaml_config(config_path)
            self.logger.info(f"Configuration loaded from {config_path}")
            return config
        except Exception as e:
            self.logger.error(f"Error loading configuration: {str(e)}")
            raise
    
    def _configure_dspy(self) -> None:
        """
        Configure DSPy with the appropriate model based on configuration.
        """
        try:
            model_config = self.config.get('dspy', {})
            model_name = model_config.get('model', 'gpt-3.5-turbo')
            
            if 'openai' in model_name.lower():
                api_key = os.environ.get('OPENAI_API_KEY')
                if not api_key:
                    self.logger.warning("OpenAI API key not found in environment variables")
                
                dspy.configure(lm=model_name)
                self.logger.info(f"DSPy configured with OpenAI model: {model_name}")
            
            elif 'claude' in model_name.lower():
                api_key = os.environ.get('ANTHROPIC_API_KEY')
                if not api_key:
                    self.logger.warning("Anthropic API key not found in environment variables")
                
                dspy.configure(lm=model_name)
                self.logger.info(f"DSPy configured with Anthropic model: {model_name}")
            
            else:
                # Default configuration
                dspy.configure(lm=model_name)
                self.logger.info(f"DSPy configured with model: {model_name}")
                
        except Exception as e:
            self.logger.error(f"Error configuring DSPy: {str(e)}")
            raise
    
    def list_modules(self, module_dir: Optional[str] = None) -> List[str]:
        """
        List all available context modules.
        
        Args:
            module_dir: Directory containing the modules (overrides configuration)
            
        Returns:
            list: List of module paths
        """
        if not module_dir:
            module_dir = self.config.get('module_dir', 'modules')
        
        module_dir = Path(module_dir)
        if not module_dir.exists():
            self.logger.error(f"Module directory does not exist: {module_dir}")
            return []
        
        # Find all markdown files recursively
        modules = list(module_dir.glob('**/*.md'))
        self.logger.info(f"Found {len(modules)} modules in {module_dir}")
        
        return [str(module) for module in modules]
    
    def optimize_module(self, module_path: str, output_dir: Optional[str] = None) -> Dict:
        """
        Optimize a single context module.
        
        Args:
            module_path: Path to the module to optimize
            output_dir: Directory to save the optimized module (overrides configuration)
            
        Returns:
            dict: Results of the optimization process
        """
        # Resolve paths
        module_path = Path(module_path)
        if not module_path.exists():
            error_msg = f"Module file not found: {module_path}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
        
        if not output_dir:
            output_dir = self.config.get('optimized_dir', 'optimized')
        
        output_dir = Path(output_dir)
        output_path = output_dir / module_path.name
        
        try:
            # Create a backup
            backup_path = backup_file(module_path, self.backup_dir)
            self.logger.info(f"Created backup at {backup_path}")
            
            # Read the module content
            content = read_file_content(module_path)
            if not content:
                error_msg = f"Module file is empty: {module_path}"
                self.logger.error(error_msg)
                return {"success": False, "error": error_msg}
            
            # Extract module name for logging
            module_name = extract_module_name(module_path)
            
            # Run optimization with DSPy
            self.logger.info(f"Optimizing module: {module_name}")
            result = self._run_dspy_optimization(content, module_name)
            
            if not result.get("success", False):
                return result
            
            optimized_content = result.get("optimized_content", "")
            if not optimized_content:
                error_msg = "DSPy returned empty optimized content"
                self.logger.error(error_msg)
                return {"success": False, "error": error_msg}
            
            # Save the optimized content
            ensure_dir(output_dir)
            write_file_content(optimized_content, output_path)
            
            # Generate diff
            diff = self._generate_diff(content, optimized_content, module_name)
            diff_path = output_dir / f"{module_path.stem}_diff.txt"
            write_file_content(diff, diff_path)
            
            self.logger.info(f"Optimization complete: {module_name}")
            return {
                "success": True,
                "original_path": str(module_path),
                "optimized_path": str(output_path),
                "diff_path": str(diff_path),
                "module_name": module_name
            }
            
        except Exception as e:
            error_msg = f"Error optimizing module {module_path}: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def _run_dspy_optimization(self, content: str, module_name: str) -> Dict:
        """
        Run DSPy optimization on the given content.
        
        Args:
            content: Module content to optimize
            module_name: Name of the module for logging
            
        Returns:
            dict: Results of the optimization process
        """
        try:
            # Create a temporary file for the DSPy optimization input
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as temp_file:
                temp_path = temp_file.name
                
                # Prepare the optimization input
                optimization_input = {
                    "module_name": module_name,
                    "content": content,
                    "optimization_goals": self.config.get("optimization_goals", [
                        "Clarity and readability",
                        "Compatibility with MCP format",
                        "Efficiency in retrieval",
                        "Accuracy of context"
                    ]),
                    "model": self.config.get("dspy", {}).get("model", "gpt-3.5-turbo")
                }
                
                # Write the input to the temporary file
                json.dump(optimization_input, temp_file)
            
            # Execute the DSPy optimization script
            script_path = self.config.get("dspy_script", "scripts/dspy_optimize.py")
            
            command = [
                "python", script_path,
                "--input", temp_path,
                "--model", optimization_input["model"]
            ]
            
            self.logger.info(f"Running DSPy optimization command: {' '.join(command)}")
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse the output
            try:
                output = json.loads(result.stdout)
                os.unlink(temp_path)  # Clean up temp file
                
                if not output.get("success", False):
                    error_msg = output.get("error", "Unknown error during DSPy optimization")
                    self.logger.error(error_msg)
                    return {"success": False, "error": error_msg}
                
                return {
                    "success": True,
                    "optimized_content": output.get("optimized_content", ""),
                    "metadata": output.get("metadata", {})
                }
                
            except json.JSONDecodeError as e:
                error_msg = f"Error parsing DSPy optimization output: {str(e)}"
                self.logger.error(error_msg)
                self.logger.debug(f"DSPy stdout: {result.stdout}")
                self.logger.debug(f"DSPy stderr: {result.stderr}")
                return {"success": False, "error": error_msg}
                
        except subprocess.CalledProcessError as e:
            error_msg = f"DSPy optimization process failed: {str(e)}"
            self.logger.error(error_msg)
            self.logger.debug(f"DSPy stdout: {e.stdout}")
            self.logger.debug(f"DSPy stderr: {e.stderr}")
            return {"success": False, "error": error_msg}
            
        except Exception as e:
            error_msg = f"Error during DSPy optimization: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def _generate_diff(self, original: str, optimized: str, module_name: str) -> str:
        """
        Generate a diff between original and optimized content.
        
        Args:
            original: Original content
            optimized: Optimized content
            module_name: Name of the module
            
        Returns:
            str: Diff output as string
        """
        original_lines = original.splitlines()
        optimized_lines = optimized.splitlines()
        
        diff = difflib.unified_diff(
            original_lines,
            optimized_lines,
            fromfile=f"{module_name}.original",
            tofile=f"{module_name}.optimized",
            lineterm=""
        )
        
        return "\n".join(diff)
    
    def batch_optimize(self, module_paths: Optional[List[str]] = None, output_dir: Optional[str] = None) -> Dict:
        """
        Optimize multiple modules in batch.
        
        Args:
            module_paths: List of module paths to optimize (None for all modules)
            output_dir: Directory to save optimized modules (overrides configuration)
            
        Returns:
            dict: Results of the batch optimization process
        """
        if not module_paths:
            module_paths = self.list_modules()
            
        if not module_paths:
            error_msg = "No modules found to optimize"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
        
        results = {
            "success": True,
            "total": len(module_paths),
            "succeeded": 0,
            "failed": 0,
            "modules": []
        }
        
        for module_path in module_paths:
            self.logger.info(f"Processing module: {module_path}")
            result = self.optimize_module(module_path, output_dir)
            
            if result.get("success", False):
                results["succeeded"] += 1
            else:
                results["failed"] += 1
                
            results["modules"].append(result)
        
        self.logger.info(f"Batch optimization complete. "
                         f"Success: {results['succeeded']}/{results['total']}")
        
        return results
    
    def compare_modules(self, original_path: str, optimized_path: str) -> str:
        """
        Compare original and optimized modules and return the diff.
        
        Args:
            original_path: Path to the original module
            optimized_path: Path to the optimized module
            
        Returns:
            str: Diff output as string
        """
        try:
            original_content = read_file_content(original_path)
            optimized_content = read_file_content(optimized_path)
            
            module_name = extract_module_name(original_path)
            return self._generate_diff(original_content, optimized_content, module_name)
            
        except Exception as e:
            error_msg = f"Error comparing modules: {str(e)}"
            self.logger.error(error_msg)
            return f"Error: {error_msg}"
    
    def apply_optimization(self, original_path: str, optimized_path: str) -> Dict:
        """
        Apply the optimized version by copying it over the original.
        
        Args:
            original_path: Path to the original module
            optimized_path: Path to the optimized module
            
        Returns:
            dict: Result of the operation
        """
        try:
            # Create another backup before applying
            backup_path = backup_file(original_path, self.backup_dir)
            
            # Read optimized content
            optimized_content = read_file_content(optimized_path)
            
            # Write to original path
            write_file_content(optimized_content, original_path)
            
            module_name = extract_module_name(original_path)
            self.logger.info(f"Applied optimization to {module_name}")
            
            return {
                "success": True,
                "module_name": module_name,
                "path": str(original_path),
                "backup_path": backup_path
            }
            
        except Exception as e:
            error_msg = f"Error applying optimization: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg} 