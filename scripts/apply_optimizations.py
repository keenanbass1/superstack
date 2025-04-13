#!/usr/bin/env python3
"""
Context Module Optimization Applier

This script handles the process of applying optimized context modules
to the production environment after they have been reviewed and approved.
"""

import os
import sys
import glob
import shutil
import logging
import argparse
import yaml
import json
import re
import difflib
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """
    Set up logging for the optimization application process.
    
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

def get_modules_to_apply(optimized_dir: str, original_dir: str) -> List[Dict[str, str]]:
    """
    Get a list of optimized modules that can be applied.
    
    Args:
        optimized_dir: Directory containing optimized modules
        original_dir: Directory containing original modules
        
    Returns:
        List of dictionaries with module info
    """
    modules = []
    
    # Get all optimized module files
    optimized_files = glob.glob(os.path.join(optimized_dir, "*.md"))
    
    for opt_file in optimized_files:
        module_name = os.path.basename(opt_file)
        original_file = os.path.join(original_dir, module_name)
        
        # Check if the original module exists
        if os.path.exists(original_file):
            modules.append({
                "name": module_name,
                "optimized_path": opt_file,
                "original_path": original_file
            })
    
    return modules

def generate_diff(original_path: str, optimized_path: str) -> str:
    """
    Generate a diff between the original and optimized module.
    
    Args:
        original_path: Path to the original module
        optimized_path: Path to the optimized module
        
    Returns:
        Diff as a string
    """
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

def create_backup(file_path: str, backup_dir: str) -> str:
    """
    Create a backup of a file before applying changes.
    
    Args:
        file_path: Path to the file to back up
        backup_dir: Directory to store backups
        
    Returns:
        Path to the backup file
    """
    # Create backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)
    
    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = os.path.basename(file_path)
    backup_filename = f"{os.path.splitext(filename)[0]}_{timestamp}{os.path.splitext(filename)[1]}"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    # Copy the file
    shutil.copy2(file_path, backup_path)
    
    return backup_path

def apply_optimization(
    module_info: Dict[str, str], 
    backup_dir: str,
    logger: logging.Logger
) -> Dict[str, Any]:
    """
    Apply an optimized module to replace the original.
    
    Args:
        module_info: Dictionary with module info
        backup_dir: Directory to store backups
        logger: Logger instance
        
    Returns:
        Dictionary with result info
    """
    result = {
        "module_name": module_info["name"],
        "success": False,
        "error": None,
        "backup_path": None
    }
    
    try:
        # Create backup
        backup_path = create_backup(module_info["original_path"], backup_dir)
        result["backup_path"] = backup_path
        logger.info(f"Created backup of {module_info['name']} at {backup_path}")
        
        # Copy optimized file to original location
        shutil.copy2(module_info["optimized_path"], module_info["original_path"])
        
        result["success"] = True
        logger.info(f"Successfully applied optimization for {module_info['name']}")
    
    except Exception as e:
        error_msg = f"Error applying optimization for {module_info['name']}: {str(e)}"
        result["error"] = error_msg
        logger.error(error_msg)
        
        # Try to restore from backup if we have one
        if result["backup_path"] and os.path.exists(result["backup_path"]):
            try:
                shutil.copy2(result["backup_path"], module_info["original_path"])
                logger.info(f"Restored {module_info['name']} from backup")
            except Exception as restore_error:
                logger.error(f"Failed to restore from backup: {str(restore_error)}")
    
    return result

def apply_all_optimizations(
    modules: List[Dict[str, str]],
    backup_dir: str,
    logger: logging.Logger
) -> Dict[str, Any]:
    """
    Apply all optimized modules.
    
    Args:
        modules: List of module info dictionaries
        backup_dir: Directory to store backups
        logger: Logger instance
        
    Returns:
        Dictionary with results info
    """
    results = {
        "total": len(modules),
        "successful": 0,
        "failed": 0,
        "modules": []
    }
    
    for module_info in modules:
        result = apply_optimization(module_info, backup_dir, logger)
        results["modules"].append(result)
        
        if result["success"]:
            results["successful"] += 1
        else:
            results["failed"] += 1
    
    return results

def save_results(results: Dict[str, Any], output_path: str) -> bool:
    """
    Save application results to a JSON file.
    
    Args:
        results: Results dictionary
        output_path: Path to save results
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Add timestamp to results
        results["timestamp"] = datetime.now().isoformat()
        
        # Write to file
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        return True
    except Exception as e:
        logging.getLogger(__name__).error(f"Error saving results: {str(e)}")
        return False

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Apply optimized context modules")
    
    parser.add_argument("--config", type=str, default="config/dsp_config.yaml",
                        help="Path to the configuration file")
    
    parser.add_argument("--original-dir", type=str,
                        help="Directory containing original modules")
    
    parser.add_argument("--optimized-dir", type=str,
                        help="Directory containing optimized modules")
    
    parser.add_argument("--backup-dir", type=str,
                        help="Directory to store backups (defaults to config value)")
    
    parser.add_argument("--module", type=str,
                        help="Apply a specific module (default: apply all available)")
    
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be done without making changes")
    
    parser.add_argument("--output", type=str,
                        help="Path to save results as JSON")
    
    parser.add_argument("--log-level", type=str, default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Logging level")
    
    parser.add_argument("--log-file", type=str,
                        help="Path to log file")
    
    return parser.parse_args()

if __name__ == "__main__":
    # Parse arguments
    args = parse_arguments()
    
    # Set up logging
    logger = setup_logging(args.log_level, args.log_file)
    
    # Load configuration
    config = load_config(args.config)
    
    # Get directories from args or config
    original_dir = args.original_dir or config.get('paths', {}).get('original_modules_dir', 'context/ai-context/modules')
    optimized_dir = args.optimized_dir or config.get('paths', {}).get('optimized_modules_dir', 'context/ai-context/optimized')
    backup_dir = args.backup_dir or config.get('paths', {}).get('backup_modules_dir', 'context/ai-context/backups')
    
    # Get modules to apply
    all_modules = get_modules_to_apply(optimized_dir, original_dir)
    
    if args.module:
        # Filter for specific module
        modules = [m for m in all_modules if m["name"] == args.module or m["name"] == f"{args.module}.md"]
        if not modules:
            logger.error(f"Module '{args.module}' not found or has no optimized version")
            sys.exit(1)
    else:
        modules = all_modules
    
    logger.info(f"Found {len(modules)} optimized modules that can be applied")
    
    # In dry-run mode, just show what would be done
    if args.dry_run:
        print(f"Dry run: would apply {len(modules)} optimized modules:")
        for module in modules:
            print(f"- {module['name']}")
            diff = generate_diff(module["original_path"], module["optimized_path"])
            print("\nDiff:")
            print(diff)
            print("\n" + "-" * 60 + "\n")
        sys.exit(0)
    
    # Apply optimizations
    results = apply_all_optimizations(modules, backup_dir, logger)
    
    # Print summary
    print(f"\nApplied {results['successful']}/{results['total']} optimized modules")
    if results['failed'] > 0:
        print(f"Failed to apply {results['failed']} modules")
        for module in results['modules']:
            if not module['success']:
                print(f"- {module['module_name']}: {module['error']}")
    
    # Save results if output path provided
    if args.output:
        if save_results(results, args.output):
            print(f"Results saved to {args.output}")
        else:
            print("Failed to save results") 