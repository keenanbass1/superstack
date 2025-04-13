#!/usr/bin/env python3
"""
Batch Context Module Optimizer

This script optimizes multiple context modules using DSP integration.
It can be used to process all modules or a specific subset based on criteria.
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
from lib.dsp_client import DSPClient
from dsp_implementation_plan import ContextOptimizer, ContextEvaluator

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """
    Set up logging for the batch optimization process.
    
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

def get_modules_to_optimize(
    config: Dict[str, Any], 
    modules_dir: str,
    module_names: Optional[List[str]] = None,
    priority_limit: Optional[int] = None
) -> List[str]:
    """
    Get the list of module paths to optimize.
    
    Args:
        config: The configuration dictionary
        modules_dir: The directory containing context modules
        module_names: Optional list of specific module names to optimize
        priority_limit: Optional limit to the number of modules to optimize
        
    Returns:
        List of module file paths to optimize
    """
    logger = logging.getLogger(__name__)
    
    if module_names:
        # Optimize specific modules
        modules = []
        for name in module_names:
            module_path = os.path.join(modules_dir, f"{name}.md")
            if os.path.exists(module_path):
                modules.append(module_path)
            else:
                logger.warning(f"Module not found: {name}")
        return modules
    else:
        # Get all markdown files from the modules directory
        all_modules = []
        for root, _, files in os.walk(modules_dir):
            for file in files:
                if file.endswith(".md"):
                    all_modules.append(os.path.join(root, file))
        
        # If no priority limit, return all modules
        if not priority_limit:
            return all_modules
            
        # Otherwise, we should prioritize modules based on criteria
        # For example, modules with higher usage, more feedback, etc.
        # This would ideally come from ContextFeedback class
        
        # For now, we'll just return all modules up to the limit
        logger.info(f"Limiting optimization to {priority_limit} modules")
        return all_modules[:priority_limit]

def batch_optimize(
    config_path: str = "config/dsp_config.yaml",
    modules_dir: Optional[str] = None,
    optimized_dir: Optional[str] = None,
    module_names: Optional[List[str]] = None,
    model_name: Optional[str] = None,
    strategy_name: Optional[str] = None,
    priority_limit: Optional[int] = None,
    auto_apply: bool = False,
    evaluate: bool = False,
    output_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Optimize multiple context modules in batch.
    
    Args:
        config_path: Path to the configuration file
        modules_dir: Directory containing the modules
        optimized_dir: Directory to store optimized modules
        module_names: Optional list of specific module names to optimize
        model_name: Name of the model to use for optimization
        strategy_name: Name of the optimization strategy to use
        priority_limit: Maximum number of modules to optimize
        auto_apply: Whether to automatically apply optimizations
        evaluate: Whether to evaluate optimizations
        output_file: Path to save the optimization results
        
    Returns:
        Dictionary containing optimization results
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
    
    # Ensure output directory exists
    os.makedirs(optimized_dir, exist_ok=True)
    
    # Initialize DSP client
    dsp_client = DSPClient(config_path)
    
    # Create context optimizer
    context_optimizer = ContextOptimizer(config_path)
    
    # Initialize evaluator if needed
    context_evaluator = None
    if evaluate:
        logger.info("Initializing context evaluator")
        context_evaluator = ContextEvaluator(config_path)
    
    # Get modules to optimize
    modules = get_modules_to_optimize(config, modules_dir, module_names, priority_limit)
    
    if not modules:
        logger.warning("No modules found to optimize")
        return {
            "success": True,
            "optimized_count": 0,
            "failed_count": 0,
            "modules": [],
            "timestamp": datetime.now().isoformat()
        }
    
    logger.info(f"Found {len(modules)} modules to optimize")
    
    # Optimize each module
    results = {
        "success": True,
        "optimized_count": 0,
        "failed_count": 0,
        "modules": [],
        "timestamp": datetime.now().isoformat()
    }
    
    for module_path in modules:
        module_name = os.path.basename(module_path).replace(".md", "")
        logger.info(f"Optimizing module: {module_name}")
        
        try:
            # Optimize the module
            optimization_result = context_optimizer.optimize_module(
                module_path,
                model_name=model_name,
                strategy=strategy_name
            )
            
            if optimization_result["success"]:
                results["optimized_count"] += 1
                
                # Evaluate if requested
                evaluation_result = None
                if evaluate and context_evaluator:
                    try:
                        evaluation_result = context_evaluator.evaluate_module(
                            module_path,
                            optimization_result["optimized_path"]
                        )
                        optimization_result["evaluation"] = evaluation_result
                        
                        # Auto-apply based on evaluation score
                        if auto_apply and evaluation_result["success"]:
                            improvement_threshold = config['evaluation']['auto_apply_threshold']
                            if evaluation_result["improvement"] >= improvement_threshold:
                                logger.info(f"Auto-applying optimization for {module_name} (improvement: {evaluation_result['improvement']:.2f}%)")
                                context_optimizer.apply_optimization(module_name)
                            else:
                                logger.info(f"Not auto-applying optimization for {module_name} (improvement: {evaluation_result['improvement']:.2f}% < threshold: {improvement_threshold}%)")
                    except Exception as e:
                        logger.error(f"Error evaluating module {module_name}: {str(e)}")
                        evaluation_result = {"success": False, "error": str(e)}
                        optimization_result["evaluation"] = evaluation_result
                
                # Auto-apply without evaluation if requested
                if auto_apply and not evaluate:
                    logger.info(f"Auto-applying optimization for {module_name} (no evaluation)")
                    context_optimizer.apply_optimization(module_name)
            else:
                results["failed_count"] += 1
            
            # Add result to output
            results["modules"].append({
                "module_name": module_name,
                "module_path": module_path,
                "success": optimization_result["success"],
                "result": optimization_result
            })
            
        except Exception as e:
            logger.error(f"Error optimizing module {module_name}: {str(e)}")
            results["failed_count"] += 1
            results["modules"].append({
                "module_name": module_name,
                "module_path": module_path,
                "success": False,
                "error": str(e)
            })
    
    # Save results to file if requested
    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Saved optimization results to {output_file}")
    
    # Log summary
    logger.info(f"Batch optimization completed: {results['optimized_count']} succeeded, {results['failed_count']} failed")
    
    return results

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Batch optimize context modules with DSP")
    
    parser.add_argument("--config", type=str, default="config/dsp_config.yaml",
                        help="Path to the configuration file")
    parser.add_argument("--modules-dir", type=str,
                        help="Directory containing context modules")
    parser.add_argument("--optimized-dir", type=str,
                        help="Directory to store optimized modules")
    parser.add_argument("--module", type=str, action="append", dest="modules",
                        help="Specific module name(s) to optimize (can be used multiple times)")
    parser.add_argument("--model", type=str,
                        help="Model to use for optimization")
    parser.add_argument("--strategy", type=str,
                        help="Optimization strategy to use")
    parser.add_argument("--limit", type=int,
                        help="Maximum number of modules to optimize")
    parser.add_argument("--output", type=str,
                        help="Path to save optimization results")
    parser.add_argument("--auto-apply", action="store_true",
                        help="Automatically apply optimizations")
    parser.add_argument("--evaluate", action="store_true",
                        help="Evaluate optimizations")
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
    
    # Run batch optimization
    results = batch_optimize(
        config_path=args.config,
        modules_dir=args.modules_dir,
        optimized_dir=args.optimized_dir,
        module_names=args.modules,
        model_name=args.model,
        strategy_name=args.strategy,
        priority_limit=args.limit,
        auto_apply=args.auto_apply,
        evaluate=args.evaluate,
        output_file=args.output
    )
    
    # Output summary
    print(f"\nBatch Optimization Summary:")
    print(f"- Total modules: {len(results['modules'])}")
    print(f"- Successfully optimized: {results['optimized_count']}")
    print(f"- Failed: {results['failed_count']}")
    
    if args.output:
        print(f"\nDetailed results saved to: {args.output}") 