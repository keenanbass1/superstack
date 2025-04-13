# Updated dspy_bridge.py with improved error handling and backup functionality

import dspy
import json
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('context_optimizer')

class ContextOptimizer:
    """Bridge between AI Context System and DSPy for optimization"""

    def __init__(self, context_dir, config_path=None):
        """Initialize with path to context modules directory"""
        self.context_dir = Path(context_dir)
        self.optimized_dir = self.context_dir / "_optimized"
        self._ensure_dirs_exist()
        self.config = self._load_config(config_path)
        
        # Configure DSPy with model from config
        model_config = self.config.get("models", {}).get(
            self.config.get("default_model", "claude"), 
            {"provider": "anthropic", "name": "claude-3-opus-20240229"}
        )
        
        if model_config["provider"] == "openai":
            dspy.settings.configure(lm=dspy.OpenAI(model=model_config["name"], temperature=0.2))
        elif model_config["provider"] == "anthropic":
            dspy.settings.configure(lm=dspy.Anthropic(model=model_config["name"], temperature=0.2))
        else:
            logger.warning(f"Unknown provider: {model_config['provider']}, defaulting to OpenAI")
            dspy.settings.configure(lm=dspy.OpenAI(model="gpt-4", temperature=0.2))
    
    def _ensure_dirs_exist(self):
        """Ensure all required directories exist"""
        self.optimized_dir.mkdir(exist_ok=True, parents=True)
        
    def _load_config(self, config_path=None):
        """Load optimization configuration from file or use defaults"""
        default_config = {
            "default_model": "claude",
            "models": {
                "claude": {"provider": "anthropic", "name": "claude-3-opus-20240229"},
                "gpt": {"provider": "openai", "name": "gpt-4"},
                "cursor-ai": {"provider": "openai", "name": "gpt-4-turbo"}
            },
            "optimization_goals": {
                "claude": ["coherence", "example_quality", "MCP_compliance"],
                "gpt": ["conciseness", "example_diversity", "technical_accuracy"],
                "cursor-ai": ["code_focus", "implementation_clarity"]
            },
            "backup_enabled": True,
            "max_retries": 3,
            "verbose": True
        }
        
        if not config_path:
            return default_config
            
        try:
            config_path = Path(config_path)
            if config_path.exists():
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    logger.info(f"Loaded configuration from {config_path}")
                    return {**default_config, **user_config}  # Merge with defaults
            else:
                logger.warning(f"Config file not found: {config_path}, using defaults")
        except Exception as e:
            logger.warning(f"Failed to load config from {config_path}: {e}")
        
        return default_config

    def list_available_modules(self):
        """List all available context modules"""
        modules = []
        for path in Path(self.context_dir).glob("**/*.md"):
            if "_optimized" in str(path):
                continue
            rel_path = path.relative_to(self.context_dir)
            module_name = str(rel_path.with_suffix(''))
            modules.append(module_name)
        return modules

    def load_context_module(self, module_path):
        """Load a context module file"""
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error loading module {module_path}: {e}")
            raise

    def save_context_module(self, module_path, content, replace_original=False):
        """Save optimized content back to module file or to optimized directory"""
        try:
            if replace_original:
                target_path = module_path
            else:
                rel_path = module_path.relative_to(self.context_dir)
                target_path = self.optimized_dir / rel_path
                # Ensure parent directories exist
                target_path.parent.mkdir(exist_ok=True, parents=True)
                
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            logger.info(f"Saved optimized module to {target_path}")
            return target_path
        except Exception as e:
            logger.error(f"Error saving module {module_path}: {e}")
            raise

    def create_backup(self, module_path):
        """Create a backup of the original module"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = self.context_dir / "_backups"
            backup_dir.mkdir(exist_ok=True, parents=True)
            
            rel_path = module_path.relative_to(self.context_dir)
            backup_path = backup_dir / f"{rel_path.stem}_{timestamp}{rel_path.suffix}"
            backup_path.parent.mkdir(exist_ok=True, parents=True)
            
            shutil.copy2(module_path, backup_path)
            logger.info(f"Created backup at {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Error creating backup for {module_path}: {e}")
            raise

    def create_signature(self, target_model="claude"):
        """Create DSPy signature for context optimization with model-specific goals"""
        optimization_goals = self.config.get("optimization_goals", {}).get(target_model, [])
        goals_str = ", ".join(optimization_goals) if optimization_goals else "general improvement"

        class OptimizeContext(dspy.Signature):
            """Optimize a context module for AI consumption"""
            original_content = dspy.InputField(desc="Original context module content")
            target_model = dspy.InputField(desc=f"Target AI model ({target_model})")
            optimization_goals = dspy.InputField(desc=f"Goals to focus on: {goals_str}")
            optimized_content = dspy.OutputField(desc="Optimized context module")

        return OptimizeContext

    def optimize_module(self, module_name, target_model="claude", dry_run=False, replace_original=False):
        """Optimize a specific context module with enhanced error handling"""
        try:
            # Validate inputs
            if not isinstance(module_name, str) or not module_name:
                raise ValueError("Module name must be a non-empty string")
                
            supported_models = list(self.config.get("models", {}).keys())
            if target_model not in supported_models:
                logger.warning(f"Target model '{target_model}' not in {supported_models}, defaulting to '{self.config['default_model']}'")
                target_model = self.config['default_model']
            
            # Handle module paths with or without subdirectories
            if "/" in module_name or "\\" in module_name:
                module_path = self.context_dir / f"{module_name}.md"
            else:
                # Search for the module in any subdirectory
                found = False
                for path in self.context_dir.glob(f"**/{module_name}.md"):
                    if "_optimized" not in str(path) and "_backups" not in str(path):
                        module_path = path
                        found = True
                        break
                
                if not found:
                    module_path = self.context_dir / f"{module_name}.md"
            
            if not module_path.exists():
                logger.error(f"Module not found: {module_path}")
                return {"success": False, "error": f"Module not found: {module_path}"}
            
            # Create backup if enabled
            if self.config["backup_enabled"]:
                self.create_backup(module_path)
            
            # Load content
            content = self.load_context_module(module_path)
            
            # Get optimization goals for this model
            optimization_goals = self.config.get("optimization_goals", {}).get(target_model, [])
            
            # Create DSPy chain with chain-of-thought reasoning
            OptimizeContext = self.create_signature(target_model)
            optimizer = dspy.ChainOfThought(OptimizeContext)
            
            # Run optimization
            logger.info(f"Running optimization for {module_name} targeting {target_model}...")
            result = optimizer(
                original_content=content,
                target_model=target_model,
                optimization_goals=", ".join(optimization_goals)
            )
            
            # Handle dry run mode
            if dry_run:
                logger.info("Dry run - not saving changes")
                return {
                    "success": True, 
                    "dry_run": True,
                    "original_content": content,
                    "optimized_content": result.optimized_content,
                    "module_name": module_name,
                    "target_model": target_model
                }
            
            # Save optimized content
            saved_path = self.save_context_module(module_path, result.optimized_content, replace_original)
            
            return {
                "success": True,
                "module_name": module_name,
                "target_model": target_model,
                "saved_path": str(saved_path),
                "replace_original": replace_original
            }
            
        except Exception as e:
            logger.error(f"Error optimizing module {module_name}: {str(e)}")
            return {"success": False, "error": str(e), "module_name": module_name}

    def batch_optimize(self, module_names=None, target_model="claude", dry_run=False, replace_original=False):
        """Optimize multiple modules in batch"""
        if module_names is None or module_names == ["all"]:
            module_names = self.list_available_modules()
            
        logger.info(f"Starting batch optimization of {len(module_names)} modules")
        
        results = []
        for module_name in module_names:
            result = self.optimize_module(
                module_name, 
                target_model=target_model,
                dry_run=dry_run,
                replace_original=replace_original
            )
            results.append(result)
            
        success_count = sum(1 for r in results if r["success"])
        logger.info(f"Batch optimization complete: {success_count}/{len(results)} modules successful")
        
        return {
            "success": success_count > 0,
            "total": len(results),
            "successful": success_count,
            "failed": len(results) - success_count,
            "results": results
        }

if __name__ == "__main__":
    # Command-line interface
    import argparse
    
    parser = argparse.ArgumentParser(description="Optimize context modules using DSPy")
    parser.add_argument("context_dir", help="Path to context modules directory")
    parser.add_argument("module", help="Module name to optimize or 'all' for batch mode")
    parser.add_argument("--target", "-t", default="claude", help="Target model (claude, gpt)")
    parser.add_argument("--config", "-c", help="Path to configuration file")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Preview without saving")
    parser.add_argument("--replace", "-r", action="store_true", help="Replace original files")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Set log level based on verbose flag
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    optimizer = ContextOptimizer(args.context_dir, args.config)
    
    if args.module.lower() == "all":
        # Batch mode
        result = optimizer.batch_optimize(
            target_model=args.target,
            dry_run=args.dry_run,
            replace_original=args.replace
        )
        print(json.dumps(result, indent=2))
    else:
        # Single module mode
        result = optimizer.optimize_module(
            args.module, 
            target_model=args.target,
            dry_run=args.dry_run,
            replace_original=args.replace
        )
        
        if args.dry_run and result["success"]:
            # Print a simple diff for dry run mode
            import difflib
            diff = difflib.unified_diff(
                result["original_content"].splitlines(),
                result["optimized_content"].splitlines(),
                fromfile=f"{args.module}.md (original)",
                tofile=f"{args.module}.md (optimized)",
                lineterm=''
            )
            print('\n'.join(diff))
        else:
            print(json.dumps(result, indent=2))