#!/usr/bin/env python3
"""
Context Module Evaluator

This script evaluates the performance of context modules, comparing
original modules against their optimized versions.
"""

import os
import sys
import json
import yaml
import logging
import argparse
from datetime import datetime
from typing import List, Dict, Any, Optional

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import project modules
from dsp_implementation_plan import ContextEvaluator

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """
    Set up logging for the evaluation process.
    
    Args:
        log_level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to a log file
        
    Returns:
        Configured logger
    """
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

def load_config(config_path: str = "config/dsp_config.yaml") -> Dict[str, Any]:
    """
    Load the configuration from the specified path.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Configuration as a dictionary
    """
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_modules_to_evaluate(
    config: Dict[str, Any], 
    modules_dir: str,
    optimized_dir: str,
    module_names: Optional[List[str]] = None
) -> List[Dict[str, str]]:
    """
    Get the list of module pairs (original and optimized) to evaluate.
    
    Args:
        config: The configuration dictionary
        modules_dir: The directory containing original context modules
        optimized_dir: The directory containing optimized modules
        module_names: Optional list of specific module names to evaluate
        
    Returns:
        List of dictionaries with original and optimized module paths
    """
    logger = logging.getLogger(__name__)
    
    modules_to_evaluate = []
    
    if module_names:
        # Evaluate specific modules
        for name in module_names:
            original_path = os.path.join(modules_dir, f"{name}.md")
            optimized_path = os.path.join(optimized_dir, f"{name}.md")
            
            if os.path.exists(original_path) and os.path.exists(optimized_path):
                modules_to_evaluate.append({
                    "name": name,
                    "original_path": original_path,
                    "optimized_path": optimized_path
                })
            else:
                if not os.path.exists(original_path):
                    logger.warning(f"Original module not found: {original_path}")
                if not os.path.exists(optimized_path):
                    logger.warning(f"Optimized module not found: {optimized_path}")
    else:
        # Find all pairs of original and optimized modules
        for root, _, files in os.walk(optimized_dir):
            for file in files:
                if file.endswith(".md"):
                    name = file[:-3]  # Remove .md extension
                    original_path = os.path.join(modules_dir, file)
                    optimized_path = os.path.join(optimized_dir, file)
                    
                    if os.path.exists(original_path):
                        modules_to_evaluate.append({
                            "name": name,
                            "original_path": original_path,
                            "optimized_path": optimized_path
                        })
                    else:
                        logger.warning(f"Original module not found for optimized module: {file}")
    
    return modules_to_evaluate

def batch_evaluate(
    config_path: str = "config/dsp_config.yaml",
    modules_dir: Optional[str] = None,
    optimized_dir: Optional[str] = None,
    module_names: Optional[List[str]] = None,
    output_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Evaluate multiple pairs of original and optimized context modules.
    
    Args:
        config_path: Path to the configuration file
        modules_dir: Directory containing original modules
        optimized_dir: Directory containing optimized modules
        module_names: Optional list of specific module names to evaluate
        output_file: Path to save the evaluation results
        
    Returns:
        Dictionary containing evaluation results
    """
    # Set up logging
    logger = setup_logging()
    
    # Load configuration
    config = load_config(config_path)
    
    # Set default directories if not specified
    if not modules_dir:
        modules_dir = config['general']['modules_path']
    if not optimized_dir:
        optimized_dir = config['general']['optimized_modules_path']
    
    # Initialize evaluator
    evaluator = ContextEvaluator(config_path)
    
    # Get modules to evaluate
    modules = get_modules_to_evaluate(config, modules_dir, optimized_dir, module_names)
    
    if not modules:
        logger.warning("No module pairs found to evaluate")
        return {
            "success": True,
            "total_evaluated": 0,
            "improved_count": 0,
            "regressed_count": 0,
            "unchanged_count": 0,
            "failed_count": 0,
            "modules": [],
            "timestamp": datetime.now().isoformat()
        }
    
    logger.info(f"Found {len(modules)} module pairs to evaluate")
    
    # Use the evaluator's batch_evaluate method
    try:
        pairs = [(module["original_path"], module["optimized_path"]) for module in modules]
        evaluation_results = evaluator.batch_evaluate(pairs)
        
        # Save results to file if requested
        if output_file:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(evaluation_results, f, indent=2)
            logger.info(f"Saved evaluation results to {output_file}")
        
        return evaluation_results
        
    except Exception as e:
        logger.error(f"Error in batch evaluation: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def evaluate_single_module(
    module_name: str,
    config_path: str = "config/dsp_config.yaml",
    modules_dir: Optional[str] = None,
    optimized_dir: Optional[str] = None,
    output_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Evaluate a single pair of original and optimized context modules.
    
    Args:
        module_name: Name of the module to evaluate
        config_path: Path to the configuration file
        modules_dir: Directory containing original modules
        optimized_dir: Directory containing optimized modules
        output_file: Path to save the evaluation results
        
    Returns:
        Dictionary containing evaluation results
    """
    # Set up logging
    logger = setup_logging()
    
    # Load configuration
    config = load_config(config_path)
    
    # Set default directories if not specified
    if not modules_dir:
        modules_dir = config['general']['modules_path']
    if not optimized_dir:
        optimized_dir = config['general']['optimized_modules_path']
    
    # Construct module paths
    original_path = os.path.join(modules_dir, f"{module_name}.md")
    optimized_path = os.path.join(optimized_dir, f"{module_name}.md")
    
    # Check if both files exist
    if not os.path.exists(original_path):
        logger.error(f"Original module not found: {original_path}")
        return {
            "success": False,
            "error": f"Original module not found: {original_path}",
            "timestamp": datetime.now().isoformat()
        }
    
    if not os.path.exists(optimized_path):
        logger.error(f"Optimized module not found: {optimized_path}")
        return {
            "success": False,
            "error": f"Optimized module not found: {optimized_path}",
            "timestamp": datetime.now().isoformat()
        }
    
    # Initialize evaluator
    evaluator = ContextEvaluator(config_path)
    
    # Evaluate the module
    try:
        evaluation_result = evaluator.evaluate_module(original_path, optimized_path)
        
        # Save results to file if requested
        if output_file:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(evaluation_result, f, indent=2)
            logger.info(f"Saved evaluation results to {output_file}")
        
        return evaluation_result
        
    except Exception as e:
        logger.error(f"Error evaluating module {module_name}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Evaluate context modules")
    
    parser.add_argument("--config", type=str, default="config/dsp_config.yaml",
                        help="Path to the configuration file")
    parser.add_argument("--modules-dir", type=str,
                        help="Directory containing original context modules")
    parser.add_argument("--optimized-dir", type=str,
                        help="Directory containing optimized modules")
    parser.add_argument("--module", type=str,
                        help="Single module name to evaluate")
    parser.add_argument("--batch", action="store_true",
                        help="Evaluate multiple modules in batch")
    parser.add_argument("--modules", type=str, nargs="+",
                        help="List of module names to evaluate in batch")
    parser.add_argument("--output", type=str,
                        help="Path to save evaluation results")
    parser.add_argument("--log-level", type=str, default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Logging level")
    parser.add_argument("--log-file", type=str,
                        help="Path to log file")
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    # Set up logging
    logger = setup_logging(args.log_level, args.log_file)
    
    # Determine evaluation mode
    if args.module:
        # Single module evaluation
        results = evaluate_single_module(
            module_name=args.module,
            config_path=args.config,
            modules_dir=args.modules_dir,
            optimized_dir=args.optimized_dir,
            output_file=args.output
        )
        
        # Output summary
        if results["success"]:
            improvement = results.get("improvement", 0)
            print(f"\nEvaluation results for module '{args.module}':")
            print(f"- Original score: {results.get('original_score', 'N/A')}")
            print(f"- Optimized score: {results.get('optimized_score', 'N/A')}")
            print(f"- Improvement: {improvement:.2f}%")
            
            if improvement > 0:
                print(f"- Recommendation: ✅ APPLY - The optimized version shows improvement")
            elif improvement < 0:
                print(f"- Recommendation: ❌ REJECT - The optimized version performs worse")
            else:
                print(f"- Recommendation: ⚠️ NEUTRAL - No significant change in performance")
        else:
            print(f"\nEvaluation failed for module '{args.module}':")
            print(f"- Error: {results.get('error', 'Unknown error')}")
            
    elif args.batch or args.modules:
        # Batch evaluation
        results = batch_evaluate(
            config_path=args.config,
            modules_dir=args.modules_dir,
            optimized_dir=args.optimized_dir,
            module_names=args.modules,
            output_file=args.output
        )
        
        # Output summary
        if results["success"]:
            avg_improvement = results.get("average_improvement", 0)
            print(f"\nBatch Evaluation Summary:")
            print(f"- Total modules evaluated: {results.get('total_evaluated', 0)}")
            print(f"- Improved modules: {results.get('improved_count', 0)}")
            print(f"- Regressed modules: {results.get('regressed_count', 0)}")
            print(f"- Unchanged modules: {results.get('unchanged_count', 0)}")
            print(f"- Failed evaluations: {results.get('failed_count', 0)}")
            print(f"- Average improvement: {avg_improvement:.2f}%")
            
            if results.get("improved", []):
                print("\nTop improved modules:")
                for module in sorted(results.get("improved", []), 
                                     key=lambda x: x.get("improvement", 0), 
                                     reverse=True)[:5]:
                    print(f"  - {module.get('name', 'Unknown')}: {module.get('improvement', 0):.2f}%")
            
            if results.get("regressed", []):
                print("\nRegressed modules:")
                for module in sorted(results.get("regressed", []), 
                                     key=lambda x: x.get("improvement", 0)):
                    print(f"  - {module.get('name', 'Unknown')}: {module.get('improvement', 0):.2f}%")
        else:
            print(f"\nBatch evaluation failed:")
            print(f"- Error: {results.get('error', 'Unknown error')}")
    else:
        logger.error("No evaluation mode specified. Use --module for single module or --batch for batch evaluation.")
        sys.exit(1)
    
    if args.output:
        print(f"\nDetailed results saved to: {args.output}") 