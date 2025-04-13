Comprehensive Implementation Plan for Enhanced DSPy Context Optimization
Phase 1: Core Infrastructure & Stability (Week 1)
1.1 Enhanced DSPy Bridge with Error Handling
python# Updated dspy_bridge.py with improved error handling and backup functionality

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
1.2 CLI Integration for Context Optimization
javascript// dev/commands/context.js with enhanced optimization command

const { Command } = require('commander');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');
const ora = require('ora'); // You may need to npm install ora
const chalk = require('chalk');
const { spawnSync } = require('child_process');

// Helper to get all modules
function getAllModules(contextDir) {
  const modules = [];
  
  function searchDir(dir, baseDir) {
    const items = fs.readdirSync(dir);
    
    for (const item of items) {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);
      
      // Skip special directories
      if (item.startsWith('_') || item.startsWith('.')) continue;
      
      if (stat.isDirectory()) {
        searchDir(fullPath, baseDir);
      } else if (item.endsWith('.md')) {
        // Get path relative to context directory
        const relativePath = path.relative(baseDir, fullPath);
        // Remove .md extension
        const moduleName = relativePath.replace(/\.md$/, '');
        modules.push(moduleName);
      }
    }
  }
  
  searchDir(contextDir, contextDir);
  return modules;
}

function showDiff(originalPath, optimizedPath) {
  try {
    // Use git diff for colored output if available
    try {
      const diffOutput = spawnSync('git', ['diff', '--no-index', originalPath, optimizedPath], {
        encoding: 'utf-8'
      });
      // git diff returns exit code 1 when differences are found
      if (diffOutput.status !== 0 && diffOutput.status !== 1) {
        throw new Error('Git diff failed');
      }
      console.log(diffOutput.stdout);
    } catch (e) {
      // Fallback to simple diff if git is not available
      const original = fs.readFileSync(originalPath, 'utf-8').split('\n');
      const optimized = fs.readFileSync(optimizedPath, 'utf-8').split('\n');
      
      // Simple diff output
      for (let i = 0; i < Math.max(original.length, optimized.length); i++) {
        if (i >= original.length) {
          console.log(chalk.green(`+ ${optimized[i]}`));
        } else if (i >= optimized.length) {
          console.log(chalk.red(`- ${original[i]}`));
        } else if (original[i] !== optimized[i]) {
          console.log(chalk.red(`- ${original[i]}`));
          console.log(chalk.green(`+ ${optimized[i]}`));
        }
      }
    }
  } catch (error) {
    console.error('Error displaying diff:', error.message);
  }
}

function registerCommands(program) {
  
  // Add other context-related commands here...
  
  const optimizeCommand = new Command('optimize')
    .description('Optimize context modules using DSPy')
    .argument('[module]', 'Module to optimize (omit for all modules)')
    .option('-t, --target <model>', 'Target model (claude, gpt, cursor-ai)', 'claude')
    .option('-c, --config <path>', 'Path to config file')
    .option('-d, --dry-run', 'Preview changes without saving', false)
    .option('-r, --replace', 'Replace original files instead of creating optimized copies', false)
    .option('--batch <size>', 'Batch size for processing multiple modules', 5)
    .option('-v, --verbose', 'Verbose output mode', false)
    .action(async (module, options) => {
      try {
        const contextDir = path.join(__dirname, '../../../docs/ai-context');
        const configPath = options.config ? path.resolve(options.config) : null;
        const scriptPath = path.join(__dirname, '../../context/dspy_bridge.py');
        
        // Check if script exists
        if (!fs.existsSync(scriptPath)) {
          console.error(`Optimization script not found: ${scriptPath}`);
          return;
        }
        
        // If module is omitted, process all modules
        if (!module) {
          const allModules = getAllModules(contextDir);
          console.log(`Found ${allModules.length} modules. Optimizing in batches...`);
          
          // Python takes 'all' as special keyword to process all modules
          module = 'all';
        }
        
        // Build command args
        const cmdArgs = [
          `"${contextDir}"`,
          `"${module}"`,
          `--target "${options.target}"`,
        ];
        
        if (configPath) cmdArgs.push(`--config "${configPath}"`);
        if (options.dryRun) cmdArgs.push('--dry-run');
        if (options.replace) cmdArgs.push('--replace');
        if (options.verbose) cmdArgs.push('--verbose');
        
        console.log(`Optimizing context module(s) for ${options.target}...`);
        
        // Add progress spinner
        const spinner = ora('Optimizing...').start();
        
        try {
          const result = execSync(
            `python ${scriptPath} ${cmdArgs.join(' ')}`,
            { encoding: 'utf-8' }
          );
          
          spinner.succeed('Optimization complete!');
          
          // Try to parse result as JSON
          try {
            const resultObj = JSON.parse(result);
            
            if (module === 'all') {
              // Batch results
              console.log(chalk.bold(`Optimization summary:`));
              console.log(`Total modules: ${resultObj.total}`);
              console.log(`Successful: ${chalk.green(resultObj.successful)}`);
              console.log(`Failed: ${chalk.red(resultObj.failed)}`);
              
              // List failures
              if (resultObj.failed > 0) {
                console.log('\nFailed modules:');
                for (const item of resultObj.results) {
                  if (!item.success) {
                    console.log(`- ${item.module_name}: ${item.error}`);
                  }
                }
              }
            } else {
              // Single module result
              if (resultObj.success) {
                if (options.dryRun) {
                  console.log(chalk.blue('Dry run completed. Changes were not saved.'));
                } else {
                  console.log(chalk.green(`Successfully optimized: ${resultObj.module_name}`));
                  console.log(`Saved to: ${resultObj.saved_path}`);
                  
                  // Show command to view diff
                  if (!options.replace) {
                    console.log(chalk.blue(`\nTo review changes: dev context diff ${resultObj.module_name}`));
                  }
                }
              } else {
                console.error(chalk.red(`Failed to optimize: ${resultObj.error}`));
              }
            }
          } catch (e) {
            // Not JSON, just print the result (likely a diff)
            console.log(result);
          }
        } catch (error) {
          spinner.fail('Optimization failed');
          console.error('Error output:');
          console.error(error.stderr || error.message);
        }
      } catch (error) {
        console.error('Error optimizing context module:', error.message);
      }
    });
    
  // Add a command to show diff between original and optimized versions
  const diffCommand = new Command('diff')
    .description('Show diff between original and optimized versions of a module')
    .argument('<module>', 'Module to compare')
    .action((module) => {
      try {
        const contextDir = path.join(__dirname, '../../../docs/ai-context');
        
        // Find the module path
        let modulePath;
        const directPath = path.join(contextDir, `${module}.md`);
        
        if (fs.existsSync(directPath)) {
          modulePath = directPath;
        } else {
          // Search in subdirectories
          const allModules = getAllModules(contextDir);
          const normalizedModule = module.replace(/\\/g, '/');
          
          const matchingModule = allModules.find(m => m === normalizedModule);
          if (matchingModule) {
            modulePath = path.join(contextDir, `${matchingModule}.md`);
          }
        }
        
        if (!modulePath) {
          console.error(`Module not found: ${module}`);
          return;
        }
        
        // Find optimized version
        const relPath = path.relative(contextDir, modulePath);
        const optimizedPath = path.join(contextDir, '_optimized', relPath);
        
        if (!fs.existsSync(optimizedPath)) {
          console.error(`No optimized version found for: ${module}`);
          return;
        }
        
        console.log(`Comparing original and optimized versions of ${module}:`);
        showDiff(modulePath, optimizedPath);
        
      } catch (error) {
        console.error('Error showing diff:', error.message);
      }
    });
    
  // Add a command to apply the optimized version
  const applyCommand = new Command('apply')
    .description('Apply optimized version of a module')
    .argument('<module>', 'Module to apply optimization for')
    .option('-b, --backup', 'Create a backup before applying', true)
    .action((module, options) => {
      try {
        const contextDir = path.join(__dirname, '../../../docs/ai-context');
        
        // Find the module path
        let modulePath;
        const directPath = path.join(contextDir, `${module}.md`);
        
        if (fs.existsSync(directPath)) {
          modulePath = directPath;
        } else {
          // Search in subdirectories
          const allModules = getAllModules(contextDir);
          const normalizedModule = module.replace(/\\/g, '/');
          
          const matchingModule = allModules.find(m => m === normalizedModule);
          if (matchingModule) {
            modulePath = path.join(contextDir, `${matchingModule}.md`);
          }
        }
        
        if (!modulePath) {
          console.error(`Module not found: ${module}`);
          return;
        }
        
        // Find optimized version
        const relPath = path.relative(contextDir, modulePath);
        const optimizedPath = path.join(contextDir, '_optimized', relPath);
        
        if (!fs.existsSync(optimizedPath)) {
          console.error(`No optimized version found for: ${module}`);
          return;
        }
        
        // Create backup if requested
        if (options.backup) {
          const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
          const backupDir = path.join(contextDir, '_backups');
          
          if (!fs.existsSync(backupDir)) {
            fs.mkdirSync(backupDir, { recursive: true });
          }
          
          const backupPath = path.join(
            backupDir, 
            `${path.basename(modulePath, '.md')}_${timestamp}.md`
          );
          
          fs.copyFileSync(modulePath, backupPath);
          console.log(`Backup created: ${backupPath}`);
        }
        
        // Copy optimized version to original
        fs.copyFileSync(optimizedPath, modulePath);
        console.log(`Applied optimized version of ${module}`);
        
      } catch (error) {
        console.error('Error applying optimized version:', error.message);
      }
    });
  
  program.addCommand(optimizeCommand);
  program.addCommand(diffCommand);
  program.addCommand(applyCommand);
}

module.exports = { registerCommands };
Phase 2: Evaluation Framework (Week 2)
2.1 Evaluation Module with PromptFoo Integration
python# scripts/context/evaluation.py

import os
import json
import yaml
import subprocess
import tempfile
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('context_evaluator')

class ContextEvaluator:
    """Evaluates the effectiveness of context modules using PromptFoo"""
    
    def __init__(self, context_dir, evaluation_dir=None):
        """Initialize with paths to context modules and evaluation configs"""
        self.context_dir = Path(context_dir)
        self.evaluation_dir = Path(evaluation_dir or self.context_dir / '_evaluation')
        self.evaluation_dir.mkdir(exist_ok=True, parents=True)
        
    def create_evaluation_config(self, module_name, original_path, optimized_path):
        """Create a PromptFoo evaluation config for comparing module versions"""
        # Ensure the module exists
        if not original_path.exists():
            raise FileNotFoundError(f"Original module not found: {original_path}")
            
        if not optimized_path.exists():
            raise FileNotFoundError(f"Optimized module not found: {optimized_path}")
        
        # Create a temp directory for the config
        eval_id = f"{module_name.replace('/', '_')}_{os.urandom(4).hex()}"
        eval_dir = self.evaluation_dir / eval_id
        eval_dir.mkdir(exist_ok=True, parents=True)
        
        # Read module content to extract key sections for testing
        with open(original_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Generate test cases based on the module content
        test_cases = self._generate_test_cases(original_content, module_name)
        
        # Create PromptFoo config
        config = {
            "prompts": {
                "original": {
                    "provider": "anthropic",
                    "system": f"You are a helpful assistant with expertise in {module_name}. Use the following context to answer questions accurately:\n\n{{{{context}}}}",
                    "prompt": "{{question}}",
                    "contextFiles": [str(original_path)]
                },
                "optimized": {
                    "provider": "anthropic",
                    "system": f"You are a helpful assistant with expertise in {module_name}. Use the following context to answer questions accurately:\n\n{{{{context}}}}",
                    "prompt": "{{question}}",
                    "contextFiles": [str(optimized_path)]
                }
            },
            "tests": test_cases,
            "providers": {
                "anthropic": {
                    "anthropic_api_key": "$ANTHROPIC_API_KEY",
                    "model": "claude-3-opus-20240229"
                }
            },
            "output": {
                "path": str(eval_dir / "results.json")
            }
        }
        
        # Write config to file
        config_path = eval_dir / "config.yaml"
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f)
            
        return {
            "eval_id": eval_id,
            "config_path": str(config_path),
            "results_path": str(eval_dir / "results.json"),
            "module_name": module_name
        }
    
    def _generate_test_cases(self, content, module_name):
        """Generate test cases based on module content"""
        # This is a simplified version - in practice, you would use LLM to generate
        # better test cases based on the module content
        
        # Extract headers to create questions
        import re
        headers = re.findall(r'#{2,4}\s+(.+)', content)
        
        test_cases = []
        for i, header in enumerate(headers[:5]):  # Limit to first 5 headers
            test_cases.append({
                "name": f"Test {i+1}: Understanding of {header}",
                "vars": {
                    "question": f"Explain the concept of {header} as described in the context. Be specific and include key details."
                },
                "assert": [
                    {
                        "type": "llm-rubric",
                        "value": "Response should be comprehensive, technically accurate, and directly address the concept in the question."
                    },
                    {
                        "type": "similar-to-reference-implementation",
                        "threshold": 0.7
                    }
                ]
            })
            
        # Add a general test
        test_cases.append({
            "name": f"Overall module understanding",
            "vars": {
                "question": f"What are the most important concepts covered in this module on {module_name}? Outline the key principles."
            },
            "assert": [
                {
                    "type": "llm-rubric",
                    "value": "Response should identify the main concepts and principles covered in the module, demonstrating comprehensive understanding."
                }
            ]
        })
        
        return test_cases
    
    def run_evaluation(self, config_path):
        """Run PromptFoo evaluation using the generated config"""
        try:
            # Check if promptfoo is installed
            subprocess.run(["promptfoo", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("PromptFoo not found. Please install it with: npm install -g promptfoo")
            return {"success": False, "error": "PromptFoo not installed"}
        
        # Run evaluation
        logger.info(f"Running evaluation with config: {config_path}")
        try:
            result = subprocess.run(
                ["promptfoo", "eval", "--config", config_path],
                check=True,
                capture_output=True,
                text=True
            )
            
            # Read results file
            results_dir = Path(config_path).parent
            results_path = results_dir / "results.json"
            
            if results_path.exists():
                with open(results_path, 'r', encoding='utf-8') as f:
                    results = json.load(f)
                
                # Calculate overall scores
                original_score = 0
                optimized_score = 0
                total_tests = 0
                
                for test in results.get("results", []):
                    total_testsRetryClaude hit the max length for a message and has paused its response. You can write Continue to keep the chat going.KBcontinueEditI'll continue with the implementation plan for the enhanced DSPy context optimization system:
Phase 2: Evaluation Framework (Week 2) (continued)
2.1 Evaluation Module with PromptFoo Integration (continued)
python# scripts/context/evaluation.py (continued)

                for test in results.get("results", []):
                    total_tests += 1
                    
                    # Get scores for each prompt
                    prompt_results = test.get("promptResults", {})
                    
                    for prompt_name, result in prompt_results.items():
                        score = sum(1 for assertion in result.get("assertions", []) if assertion.get("pass"))
                        total_assertions = len(result.get("assertions", []))
                        
                        if total_assertions > 0:
                            normalized_score = score / total_assertions
                            
                            if prompt_name == "original":
                                original_score += normalized_score
                            elif prompt_name == "optimized":
                                optimized_score += normalized_score
                
                # Calculate average scores
                if total_tests > 0:
                    original_score /= total_tests
                    optimized_score /= total_tests
                    
                    improvement = optimized_score - original_score
                    percentage_improvement = (improvement / max(original_score, 0.001)) * 100
                
                return {
                    "success": True,
                    "original_score": original_score,
                    "optimized_score": optimized_score,
                    "improvement": improvement,
                    "percentage_improvement": percentage_improvement,
                    "total_tests": total_tests,
                    "results_path": str(results_path)
                }
            else:
                return {"success": False, "error": "Results file not found after evaluation"}
                
        except subprocess.CalledProcessError as e:
            logger.error(f"PromptFoo evaluation failed: {e}")
            logger.error(f"Output: {e.stdout}")
            logger.error(f"Error: {e.stderr}")
            return {"success": False, "error": str(e)}
    
    def evaluate_module(self, module_name):
        """Evaluate a module by comparing original and optimized versions"""
        try:
            # Find original module path
            original_path = None
            for path in self.context_dir.glob(f"**/{module_name}.md"):
                if "_optimized" not in str(path) and "_backups" not in str(path):
                    original_path = path
                    break
                    
            if not original_path:
                return {"success": False, "error": f"Original module not found: {module_name}"}
                
            # Find optimized version
            rel_path = original_path.relative_to(self.context_dir)
            optimized_path = self.context_dir / "_optimized" / rel_path
            
            if not optimized_path.exists():
                return {"success": False, "error": f"Optimized version not found for: {module_name}"}
            
            # Create evaluation config
            config = self.create_evaluation_config(module_name, original_path, optimized_path)
            
            # Run evaluation
            result = self.run_evaluation(config["config_path"])
            
            # Add module info to result
            result["module_name"] = module_name
            result["original_path"] = str(original_path)
            result["optimized_path"] = str(optimized_path)
            result["eval_id"] = config["eval_id"]
            
            return result
            
        except Exception as e:
            logger.error(f"Error evaluating module {module_name}: {e}")
            return {"success": False, "error": str(e), "module_name": module_name}
            
    def batch_evaluate(self, module_names=None):
        """Evaluate multiple modules in batch"""
        if not module_names:
            # Find all modules that have optimized versions
            optimized_dir = self.context_dir / "_optimized"
            if not optimized_dir.exists():
                return {"success": False, "error": "No optimized modules found"}
                
            module_names = []
            for path in optimized_dir.glob("**/*.md"):
                rel_path = path.relative_to(optimized_dir)
                module_name = str(rel_path.with_suffix(''))
                module_names.append(module_name)
                
        logger.info(f"Starting batch evaluation of {len(module_names)} modules")
        
        results = []
        for module_name in module_names:
            result = self.evaluate_module(module_name)
            results.append(result)
            
        success_count = sum(1 for r in results if r["success"])
        
        # Calculate average improvement
        total_improvement = 0
        improved_modules = []
        regression_modules = []
        
        for result in results:
            if result["success"]:
                improvement = result.get("improvement", 0)
                total_improvement += improvement
                
                if improvement > 0:
                    improved_modules.append({
                        "module": result["module_name"],
                        "improvement": improvement,
                        "percentage": result.get("percentage_improvement", 0)
                    })
                elif improvement < 0:
                    regression_modules.append({
                        "module": result["module_name"],
                        "regression": -improvement,
                        "percentage": -result.get("percentage_improvement", 0)
                    })
        
        avg_improvement = total_improvement / max(success_count, 1)
        
        return {
            "success": success_count > 0,
            "total": len(results),
            "successful": success_count,
            "failed": len(results) - success_count,
            "average_improvement": avg_improvement,
            "improved_modules": sorted(improved_modules, key=lambda x: x["improvement"], reverse=True),
            "regression_modules": sorted(regression_modules, key=lambda x: x["regression"], reverse=True),
            "results": results
        }

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate context modules effectiveness")
    parser.add_argument("context_dir", help="Path to context modules directory")
    parser.add_argument("module", help="Module name to evaluate or 'all' for batch mode")
    parser.add_argument("--output", "-o", help="Path to save evaluation results")
    
    args = parser.parse_args()
    
    evaluator = ContextEvaluator(args.context_dir)
    
    if args.module.lower() == "all":
        # Batch mode
        result = evaluator.batch_evaluate()
    else:
        # Single module mode
        result = evaluator.evaluate_module(args.module)
    
    # Print results to console
    print(json.dumps(result, indent=2))
    
    # Save results if output path specified
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
2.2 CLI Integration for Evaluation
javascript// Add this to dev/commands/context.js

// Add command for evaluating module changes
const evalCommand = new Command('evaluate')
  .description('Evaluate effectiveness of context module optimizations')
  .argument('[module]', 'Module to evaluate (omit for all optimized modules)')
  .option('-o, --output <path>', 'Save results to file')
  .option('-v, --verbose', 'Verbose output')
  .action(async (module, options) => {
    try {
      const contextDir = path.join(__dirname, '../../../docs/ai-context');
      const scriptPath = path.join(__dirname, '../../context/evaluation.py');
      
      // Check if script exists
      if (!fs.existsSync(scriptPath)) {
        console.error(`Evaluation script not found: ${scriptPath}`);
        return;
      }
      
      // Default to 'all' if no module specified
      module = module || 'all';
      
      // Build command
      const cmdArgs = [
        `"${contextDir}"`,
        `"${module}"`
      ];
      
      if (options.output) cmdArgs.push(`--output "${options.output}"`);
      
      console.log(`Evaluating module optimizations for ${module === 'all' ? 'all modules' : module}...`);
      
      // Add progress spinner
      const spinner = ora('Evaluating...').start();
      
      try {
        const result = execSync(
          `python ${scriptPath} ${cmdArgs.join(' ')}`,
          { encoding: 'utf-8' }
        );
        
        spinner.succeed('Evaluation complete!');
        
        // Parse and display results
        try {
          const resultObj = JSON.parse(result);
          
          if (module === 'all') {
            // Batch results
            console.log(chalk.bold(`Evaluation summary:`));
            console.log(`Total modules: ${resultObj.total}`);
            console.log(`Successful: ${chalk.green(resultObj.successful)}`);
            console.log(`Failed: ${chalk.red(resultObj.failed)}`);
            console.log(`Average improvement: ${resultObj.average_improvement >= 0 ? 
              chalk.green(`+${resultObj.average_improvement.toFixed(2)}`) : 
              chalk.red(resultObj.average_improvement.toFixed(2))}`);
            
            // Show top improvements
            if (resultObj.improved_modules.length > 0) {
              console.log('\nTop improvements:');
              resultObj.improved_modules.slice(0, 5).forEach(item => {
                console.log(`- ${item.module}: ${chalk.green(`+${item.improvement.toFixed(2)} (${item.percentage.toFixed(1)}%)`)}`);
              });
            }
            
            // Show regressions
            if (resultObj.regression_modules.length > 0) {
              console.log('\nRegressions:');
              resultObj.regression_modules.forEach(item => {
                console.log(`- ${item.module}: ${chalk.red(`-${item.regression.toFixed(2)} (${item.percentage.toFixed(1)}%)`)}`);
              });
            }
          } else {
            // Single module result
            if (resultObj.success) {
              console.log('Module evaluation:', chalk.bold(resultObj.module_name));
              console.log(`Original score: ${resultObj.original_score.toFixed(2)}`);
              console.log(`Optimized score: ${resultObj.optimized_score.toFixed(2)}`);
              
              const improvement = resultObj.improvement;
              const sign = improvement >= 0 ? '+' : '';
              const color = improvement >= 0 ? chalk.green : chalk.red;
              
              console.log(`Improvement: ${color(`${sign}${improvement.toFixed(2)} (${resultObj.percentage_improvement.toFixed(1)}%)`)}`);
              
              // Recommendation
              if (improvement > 0.05) {
                console.log(chalk.green('\nRecommendation: Apply the optimized version'));
                console.log(`Command: dev context apply ${resultObj.module_name}`);
              } else if (improvement >= -0.05) {
                console.log(chalk.yellow('\nRecommendation: Marginal difference, compare details before applying'));
                console.log(`Command: dev context diff ${resultObj.module_name}`);
              } else {
                console.log(chalk.red('\nRecommendation: Keep the original version'));
              }
            } else {
              console.error(chalk.red(`Evaluation failed: ${resultObj.error}`));
            }
          }
        } catch (e) {
          // Not valid JSON, just print the result
          console.log(result);
        }
      } catch (error) {
        spinner.fail('Evaluation failed');
        console.error('Error output:');
        console.error(error.stderr || error.message);
      }
    } catch (error) {
      console.error('Error evaluating context module:', error.message);
    }
  });

program.addCommand(evalCommand);
Phase 3: Batch Processing & Automation (Week 3)
3.1 Configuration File for Optimization Settings
yaml# config/context-optimization.yaml

# General settings
default_model: "claude"
backup_enabled: true
verbose: false
max_retries: 3

# Model configurations
models:
  claude:
    provider: "anthropic"
    name: "claude-3-opus-20240229"
    temperature: 0.2
  
  gpt:
    provider: "openai"
    name: "gpt-4"
    temperature: 0.1
  
  cursor-ai:
    provider: "openai"
    name: "gpt-4-turbo"
    temperature: 0.3

# Optimization goals by target model
optimization_goals:
  claude:
    - "coherence"
    - "example_quality"
    - "MCP_compliance"
    - "accessibility"
  
  gpt:
    - "conciseness"
    - "example_diversity"
    - "technical_accuracy"
    - "schema_compatibility"
  
  cursor-ai:
    - "code_focus"
    - "implementation_clarity"
    - "IDE_integration"

# Performance thresholds for automatic acceptance
auto_accept:
  enabled: false
  min_improvement: 0.05
  max_regression: -0.02

# Batch processing settings
batch:
  size: 5
  parallel: false
  timeout_per_module: 600

# Evaluation settings
evaluation:
  tests_per_module: 5
  model: "claude-3-opus-20240229"
  min_similarity_threshold: 0.7
3.2 Feedback Loop System
python# scripts/context/feedback_loop.py

import sqlite3
import os
import json
import time
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('feedback_loop')

class FeedbackSystem:
    """Tracks and utilizes feedback on context module performance"""
    
    def __init__(self, db_path):
        """Initialize with database path"""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True, parents=True)
        self.db = self._initialize_db()
    
    def _initialize_db(self):
        """Set up the database for tracking module feedback"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS module_feedback (
            id INTEGER PRIMARY KEY,
            module_name TEXT,
            target_model TEXT,
            effectiveness REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS optimization_results (
            id INTEGER PRIMARY KEY,
            module_name TEXT,
            target_model TEXT,
            original_score REAL,
            optimized_score REAL,
            improvement REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            applied BOOLEAN DEFAULT FALSE
        )
        ''')
        
        conn.commit()
        return conn
    
    def record_feedback(self, module_name, target_model, effectiveness, notes=""):
        """Record effectiveness of a module based on user feedback or testing"""
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO module_feedback (module_name, target_model, effectiveness, notes) VALUES (?, ?, ?, ?)",
            (module_name, target_model, effectiveness, notes)
        )
        self.db.commit()
        logger.info(f"Recorded feedback for {module_name}: {effectiveness}")
        return cursor.lastrowid
    
    def record_optimization(self, module_name, target_model, original_score, optimized_score, improvement, applied=False):
        """Record results of an optimization run"""
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO optimization_results (module_name, target_model, original_score, optimized_score, improvement, applied) VALUES (?, ?, ?, ?, ?, ?)",
            (module_name, target_model, original_score, optimized_score, improvement, applied)
        )
        self.db.commit()
        logger.info(f"Recorded optimization for {module_name}: improvement={improvement}")
        return cursor.lastrowid
    
    def update_optimization_applied(self, optimization_id, applied=True):
        """Update whether an optimization was applied"""
        cursor = self.db.cursor()
        cursor.execute(
            "UPDATE optimization_results SET applied = ? WHERE id = ?",
            (applied, optimization_id)
        )
        self.db.commit()
        return cursor.rowcount > 0
    
    def get_module_feedback(self, module_name, target_model=None, limit=10):
        """Get recent feedback for a specific module"""
        cursor = self.db.cursor()
        if target_model:
            cursor.execute(
                "SELECT * FROM module_feedback WHERE module_name = ? AND target_model = ? ORDER BY timestamp DESC LIMIT ?",
                (module_name, target_model, limit)
            )
        else:
            cursor.execute(
                "SELECT * FROM module_feedback WHERE module_name = ? ORDER BY timestamp DESC LIMIT ?",
                (module_name, limit)
            )
        return cursor.fetchall()
    
    def get_optimization_history(self, module_name, target_model=None, limit=10):
        """Get optimization history for a module"""
        cursor = self.db.cursor()
        if target_model:
            cursor.execute(
                "SELECT * FROM optimization_results WHERE module_name = ? AND target_model = ? ORDER BY timestamp DESC LIMIT ?",
                (module_name, target_model, limit)
            )
        else:
            cursor.execute(
                "SELECT * FROM optimization_results WHERE module_name = ? ORDER BY timestamp DESC LIMIT ?",
                (module_name, limit)
            )
        return cursor.fetchall()
    
    def get_module_effectiveness(self, module_name, target_model=None):
        """Calculate average effectiveness for a module"""
        cursor = self.db.cursor()
        if target_model:
            cursor.execute(
                "SELECT AVG(effectiveness) FROM module_feedback WHERE module_name = ? AND target_model = ?",
                (module_name, target_model)
            )
        else:
            cursor.execute(
                "SELECT AVG(effectiveness) FROM module_feedback WHERE module_name = ?",
                (module_name,)
            )
        result = cursor.fetchone()
        return result[0] if result[0] is not None else 0.0
    
    def identify_modules_for_improvement(self, threshold=0.7, min_feedback_count=3):
        """Identify modules that could benefit from optimization"""
        cursor = self.db.cursor()
        cursor.execute(
            """
            SELECT module_name, target_model, AVG(effectiveness) as avg_effectiveness, COUNT(*) as feedback_count 
            FROM module_feedback 
            GROUP BY module_name, target_model 
            HAVING avg_effectiveness < ? AND feedback_count >= ?
            ORDER BY avg_effectiveness ASC
            """,
            (threshold, min_feedback_count)
        )
        return cursor.fetchall()
    
    def get_optimization_success_rate(self, target_model=None, min_improvement=0.05):
        """Calculate success rate of optimizations"""
        cursor = self.db.cursor()
        if target_model:
            cursor.execute(
                """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN improvement >= ? THEN 1 ELSE 0 END) as successful
                FROM optimization_results
                WHERE target_model = ?
                """,
                (min_improvement, target_model)
            )
        else:
            cursor.execute(
                """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN improvement >= ? THEN 1 ELSE 0 END) as successful
                FROM optimization_results
                """,
                (min_improvement,)
            )
        
        result = cursor.fetchone()
        if not result or result[0] == 0:
            return 0.0
        
        return (result[1] / result[0]) * 100.0
    
    def export_data(self, output_path):
        """Export all data to JSON file"""
        cursor = self.db.cursor()
        
        # Get feedback data
        cursor.execute("SELECT * FROM module_feedback")
        feedback_rows = cursor.fetchall()
        feedback_data = []
        for row in feedback_rows:
            feedback_data.append({
                "id": row[0],
                "module_name": row[1],
                "target_model": row[2],
                "effectiveness": row[3],
                "timestamp": row[4],
                "notes": row[5]
            })
        
        # Get optimization data
        cursor.execute("SELECT * FROM optimization_results")
        optimization_rows = cursor.fetchall()
        optimization_data = []
        for row in optimization_rows:
            optimization_data.append({
                "id": row[0],
                "module_name": row[1],
                "target_model": row[2],
                "original_score": row[3],
                "optimized_score": row[4],
                "improvement": row[5],
                "timestamp": row[6],
                "applied": bool(row[7])
            })
        
        # Compile export data
        export_data = {
            "feedback": feedback_data,
            "optimizations": optimization_data,
            "export_date": datetime.now().isoformat(),
            "summary": {
                "total_feedback": len(feedback_data),
                "total_optimizations": len(optimization_data),
                "average_improvement": sum(opt["improvement"] for opt in optimization_data) / max(len(optimization_data), 1)
            }
        }
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)
        
        return export_data["summary"]

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Context Module Feedback System")
    parser.add_argument("command", choices=["record", "query", "identify", "export"], help="Command to execute")
    parser.add_argument("--db", default="context_feedback.db", help="Path to database file")
    parser.add_argument("--module", help="Module name for record/query commands")
    parser.add_argument("--model", help="Target model name")
    parser.add_argument("--score", type=float, help="Effectiveness score (0-1)")
    parser.add_argument("--notes", help="Additional notes")
    parser.add_argument("--threshold", type=float, default=0.7, help="Threshold for identifying modules needing improvement")
    parser.add_argument("--output", help="Output file path for export command")
    
    args = parser.parse_args()
    
    feedback_system = FeedbackSystem(args.db)
    
    if args.command == "record":
        if not args.module or args.score is None:
            print("Error: --module and --score are required for 'record' command")
            sys.exit(1)
        
        feedback_system.record_feedback(args.module, args.model, args.score, args.notes or "")
        print(f"Recorded feedback for {args.module}")
        
    elif args.command == "query":
        if not args.module:
            print("Error: --module is required for 'query' command")
            sys.exit(1)
        
        feedback = feedback_system.get_module_feedback(args.module, args.model)
        print(f"Recent feedback for {args.module}:")
        for item in feedback:
            print(f"- {item[4]} | Score: {item[3]} | Notes: {item[5]}")
        
    elif args.command == "identify":
        modules = feedback_system.identify_modules_for_improvement(args.threshold)
        print(f"Modules needing improvement (below {args.threshold}):")
        for module, model, score, count in modules:
            print(f"- {module} ({model}): {score:.2f} [Based on {count} feedback items]")
        
    elif args.command == "export":
        if not args.output:
            args.output = f"context_feedback_export_{int(time.time())}.json"
        
        summary = feedback_system.export_data(args.output)
        print(f"Exported data to {args.output}")
        print(f"Summary: {summary['total_feedback']} feedback records, {summary['total_optimizations']} optimizations")
        print(f"Average improvement: {summary['average_improvement']:.2f}")
Phase 4: Continuous Improvement & Integration (Week 4)
4.1 GitHub Actions Workflow for Optimization
yaml# .github/workflows/context-optimization.yml

name: Context Module Optimization

on:
  workflow_dispatch:
    inputs:
      module:
        description: 'Context module to optimize (leave empty for batch)'
        required: false
      target_model:
        description: 'Target model for optimization'
        default: 'claude'
        required: true
        type: choice
        options:
          - claude
          - gpt
          - cursor-ai
      dry_run:
        description: 'Preview changes without applying'
        default: true
        type: boolean
      auto_apply:
        description: 'Automatically apply improvements above threshold'
        default: false
        type: boolean
  
  # Optional: Schedule regular optimization of poorly performing modules
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday

jobs:
  optimize:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install dspy-ai pyyaml
          npm install -g promptfoo
      
      - name: Set up API keys
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          echo "OPENAI_API_KEY=$OPENAI_API_KEY" >> $GITHUB_ENV
          echo "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY" >> $GITHUB_ENV
      
      - name: Optimize modules
        id: optimize
        env:
          MODULE: ${{ github.event.inputs.module }}
          TARGET_MODEL: ${{ github.event.inputs.target_model }}
          DRY_RUN: ${{ github.event.inputs.dry_run }}
        run: |
          # Run optimization script
          mkdir -p ./results
          
          if [ -z "$MODULE" ]; then
            echo "Running batch optimization..."
            MODULES_TO_OPTIMIZE=$(python ./scripts/context/feedback_loop.py identify --threshold 0.7 | grep -oP '- \K[^ ]+' | head -5)
            echo "Modules identified for optimization: $MODULES_TO_OPTIMIZE"
            
            for module in $MODULES_TO_OPTIMIZE; do
              echo "Optimizing $module..."
              python ./scripts/context/dspy_bridge.py ./docs/ai-context "$module" --target "$TARGET_MODEL" $([[ "$DRY_RUN" == "true" ]] && echo "--dry-run") > "./results/${module}_optimization.json"
            done
          else
            echo "Optimizing single module: $MODULE"
            python ./scripts/context/dspy_bridge.py ./docs/ai-context "$MODULE" --target "$TARGET_MODEL" $([[ "$DRY_RUN" == "true" ]] && echo "--dry-run") > "./results/${MODULE}_optimization.json"
          fi
      
      - name: Evaluate optimizations
        id: evaluate
        if: ${{ !github.event.inputs.dry_run }}
        env:
          MODULE: ${{ github.event.inputs.module }}
          AUTO_APPLY: ${{ github.event.inputs.auto_apply }}
        run: |
          if [ -z "$MODULE" ]; then
            # Batch evaluation
            modules=$(ls ./results/*_optimization.json | sed 's/\.\/results\///' | sed 's/_optimization\.json//')
            
            for module in $modules; do
              echo "Evaluating $module..."
              python ./scripts/context/evaluation.py ./docs/ai-context "$module" --output "./results/${module}_evaluation.json"
              
              # Apply if meets threshold and auto-apply is enabled
              if [[ "$AUTO_APPLY" == "true" ]]; then
                improvement=$(jq -r '.improvement' "./results/${module}_evaluation.json")
                threshold=0.05
                
                if (( $(echo "$improvement > $threshold" | bc -l) )); then
                  echo "Auto-applying optimization for $module (improvement: $improvement)"
                  cp ./docs/ai-context/_optimized/${module}.md ./docs/ai-context/${module}.md
                fi
              fi
            done
          else
            # Single module evaluation
            python ./scripts/context/evaluation.py ./docs/ai-context "$MODULE" --output "./results/${MODULE}_evaluation.json"
            
            # Apply if meets threshold and auto-apply is enabled
            if [[ "$AUTO_APPLY" == "true" ]]; then
              improvement=$(jq -r '.improvement' "./results/${MODULE}_evaluation.json")
              threshold=0.05
              
              if (( $(echo "$improvement > $threshold" | bc -l) )); then
                echo "Auto-applying optimization for $MODULE (improvement: $improvement)"
                cp ./docs/ai-context/_optimized/${MODULE}.md ./docs/ai-context/${MODULE}.md
              fi
            fi
          fi
      
      - name: Create optimization report
        run: |
          echo "# Context Module Optimization Report" > report.md
          echo "Generated on $(date)" >> report.md
          echo "" >> report.md
          
          # Add optimization results
          echo "## Optimization Results" >> report.md
          for result in ./results/*_optimization.json; do
            module=$(basename $result _optimization.json)
            echo "### $module" >> report.md
            
            if jq -e '.success' $result > /dev/null; then
              echo "✅ Optimization successful" >> report.md
            else
              echo "❌ Optimization failed: $(jq -r '.error' $result)" >> report.md
              continue
            fi
            
            # Add evaluation results if available
            eval_file="./results/${module}_evaluation.json"
            if [ -f "$eval_file" ]; then
              improvement=$(jq -r '.improvement' $eval_file)
              orig_score=$(jq -r '.original_score' $eval_file)
              opt_score=$(jq -r '.optimized_score' $eval_file)
              
              echo "- Original score: $orig_score" >> report.md
              echo "- Optimized score: $opt_score" >> report.md
              echo "- Improvement: $improvement" >> report.md
              
              if (( $(echo "$improvement > 0.05" | bc -l) )); then
                echo "- Recommendation: **Apply optimization**" >> report.md
              elif (( $(echo "$improvement > -0.05" | bc -l) )); then
                echo "- Recommendation: **Review changes manually**" >> report.md
              else
                echo "- Recommendation: **Keep original version**" >> report.md
              fi
            fi
            
            echo "" >> report.md
          done
      
      - name: Upload results
        uses: actions/upload-artifact@v3
        withRetryClaude hit the max length for a message and has paused its response. You can write Continue to keep the chat going.KBcontinueEditI'll continue with the comprehensive implementation plan:
Phase 4: Continuous Improvement & Integration (Week 4) (continued)
4.1 GitHub Actions Workflow for Optimization (continued)
yaml# .github/workflows/context-optimization.yml (continued)

      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: optimization-results
          path: |
            ./results/*.json
            report.md
      
      - name: Create PR for approved optimizations
        if: ${{ github.event.inputs.auto_apply == 'true' && !github.event.inputs.dry_run }}
        uses: peter-evans/create-pull-request@v4
        with:
          commit-message: "Automatically apply context module optimizations"
          title: "Context Module Optimization: Auto-approved improvements"
          body: |
            This PR contains automatically approved context module optimizations.
            
            The following modules were optimized and met the improvement threshold:
            ${{ steps.evaluate.outputs.applied_modules }}
            
            See the attached optimization report for details.
          branch: auto-context-optimization
          add-paths: |
            docs/ai-context/*.md
          delete-branch: true
4.2 Integration with Project Build Process
javascript// scripts/dev/commands/build.js

// Add context optimization check to build process
program
  .command('build')
  .option('--optimize-context', 'Optimize context modules before building', false)
  .option('--target-model <model>', 'Target model for optimization', 'claude')
  .option('--auto-apply', 'Automatically apply good optimizations', false)
  .action(async (options) => {
    try {
      // If context optimization is requested, run it before building
      if (options.optimizeContext) {
        console.log('Optimizing context modules before build...');
        
        // Get list of modules that need improvement
        const { execSync } = require('child_process');
        const contextDir = path.join(__dirname, '../../../docs/ai-context');
        const feedbackPath = path.join(__dirname, '../../../data/context_feedback.db');
        
        // Identify modules that need improvement
        const identifyResult = execSync(
          `python ${path.join(__dirname, '../../context/feedback_loop.py')} identify --db "${feedbackPath}" --threshold 0.7`,
          { encoding: 'utf-8' }
        );
        
        // Extract module names from the output
        const moduleRegex = /- ([^\s]+) \([^\)]+\):/g;
        const modulesToOptimize = [];
        let match;
        
        while ((match = moduleRegex.exec(identifyResult)) !== null) {
          modulesToOptimize.push(match[1]);
        }
        
        // Limit to top 5 modules
        const modulesToProcess = modulesToOptimize.slice(0, 5);
        
        if (modulesToProcess.length > 0) {
          console.log(`Found ${modulesToProcess.length} modules to optimize: ${modulesToProcess.join(', ')}`);
          
          for (const module of modulesToProcess) {
            try {
              console.log(`Optimizing ${module}...`);
              
              // Run optimization
              const optimizeResult = JSON.parse(execSync(
                `python ${path.join(__dirname, '../../context/dspy_bridge.py')} "${contextDir}" "${module}" --target "${options.targetModel}"`,
                { encoding: 'utf-8' }
              ));
              
              if (optimizeResult.success) {
                console.log(`Successfully optimized ${module}`);
                
                // If auto-apply is enabled, evaluate and potentially apply
                if (options.autoApply) {
                  console.log(`Evaluating optimization for ${module}...`);
                  
                  const evalResult = JSON.parse(execSync(
                    `python ${path.join(__dirname, '../../context/evaluation.py')} "${contextDir}" "${module}"`,
                    { encoding: 'utf-8' }
                  ));
                  
                  if (evalResult.success && evalResult.improvement > 0.05) {
                    console.log(`Applying optimization for ${module} (improvement: ${evalResult.improvement.toFixed(2)})`);
                    
                    // Apply the optimization
                    execSync(
                      `node ${path.join(__dirname, '../index.js')} context apply "${module}"`,
                      { stdio: 'inherit' }
                    );
                  } else {
                    console.log(`Not applying optimization for ${module} (improvement: ${evalResult.improvement?.toFixed(2) || 'N/A'})`);
                  }
                }
              } else {
                console.log(`Failed to optimize ${module}: ${optimizeResult.error}`);
              }
            } catch (error) {
              console.error(`Error processing ${module}:`, error.message);
            }
          }
        } else {
          console.log('No modules identified for optimization');
        }
      }
      
      // Continue with regular build process
      console.log('Building project...');
      // ... existing build logic ...
      
    } catch (error) {
      console.error('Build process failed:', error.message);
      process.exit(1);
    }
  });
4.3 Dashboard for Optimization Insights
javascript// scripts/dev/commands/dashboard.js

const { Command } = require('commander');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');
const open = require('open');
const express = require('express');
const sqlite3 = require('sqlite3').verbose();

function registerCommands(program) {
  // Add dashboard command
  program
    .command('dashboard')
    .description('Launch dashboard for context module insights')
    .option('-p, --port <port>', 'Port to run the dashboard on', 3000)
    .action(async (options) => {
      try {
        // Paths
        const contextDir = path.join(__dirname, '../../../docs/ai-context');
        const dataDir = path.join(__dirname, '../../../data');
        const dbPath = path.join(dataDir, 'context_feedback.db');
        
        // Ensure data directory exists
        if (!fs.existsSync(dataDir)) {
          fs.mkdirSync(dataDir, { recursive: true });
        }
        
        // Generate stats if they don't exist
        const statsPath = path.join(dataDir, 'context_stats.json');
        if (!fs.existsSync(statsPath) || isStatsStale(statsPath)) {
          console.log('Generating context module statistics...');
          generateStats(contextDir, dbPath, statsPath);
        }
        
        // Launch dashboard server
        const app = express();
        
        // Serve static files
        app.use(express.static(path.join(__dirname, '../../../templates/dashboard')));
        
        // API endpoints
        app.get('/api/stats', (req, res) => {
          try {
            const stats = JSON.parse(fs.readFileSync(statsPath, 'utf-8'));
            res.json(stats);
          } catch (error) {
            res.status(500).json({ error: error.message });
          }
        });
        
        app.get('/api/modules', (req, res) => {
          try {
            const modules = getAllModules(contextDir);
            res.json(modules);
          } catch (error) {
            res.status(500).json({ error: error.message });
          }
        });
        
        app.get('/api/feedback/:module', (req, res) => {
          try {
            const { module } = req.params;
            const feedback = getModuleFeedback(dbPath, module);
            res.json(feedback);
          } catch (error) {
            res.status(500).json({ error: error.message });
          }
        });
        
        app.get('/api/optimizations/:module', (req, res) => {
          try {
            const { module } = req.params;
            const optimizations = getModuleOptimizations(dbPath, module);
            res.json(optimizations);
          } catch (error) {
            res.status(500).json({ error: error.message });
          }
        });
        
        app.get('/api/recommendations', (req, res) => {
          try {
            const recommendations = getOptimizationRecommendations(dbPath);
            res.json(recommendations);
          } catch (error) {
            res.status(500).json({ error: error.message });
          }
        });
        
        // Start server
        const server = app.listen(options.port, () => {
          console.log(`Dashboard running at http://localhost:${options.port}`);
          open(`http://localhost:${options.port}`);
          
          console.log('Press Ctrl+C to stop');
        });
        
        // Handle graceful shutdown
        process.on('SIGINT', () => {
          console.log('Stopping dashboard...');
          server.close(() => {
            console.log('Dashboard stopped');
            process.exit(0);
          });
        });
        
      } catch (error) {
        console.error('Error launching dashboard:', error.message);
      }
    });
}

// Helper functions
function isStatsStale(statsPath) {
  try {
    const stats = fs.statSync(statsPath);
    const now = new Date();
    const fileTime = new Date(stats.mtime);
    const diffHours = (now - fileTime) / (1000 * 60 * 60);
    
    // Consider stats stale if older than 24 hours
    return diffHours > 24;
  } catch (e) {
    return true;
  }
}

function generateStats(contextDir, dbPath, outputPath) {
  try {
    // Get all modules
    const modules = getAllModules(contextDir);
    
    // Connect to feedback database
    const db = new sqlite3.Database(dbPath);
    
    // Collect stats
    const stats = {
      total_modules: modules.length,
      optimization_stats: null,
      feedback_stats: null,
      top_performing: [],
      needs_improvement: [],
      most_optimized: [],
      recent_optimizations: [],
      generated: new Date().toISOString()
    };
    
    // Get optimization stats
    db.get(
      `SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN improvement > 0 THEN 1 ELSE 0 END) as improved,
        AVG(improvement) as avg_improvement
      FROM optimization_results`,
      (err, row) => {
        if (!err && row) {
          stats.optimization_stats = {
            total: row.total,
            improved: row.improved,
            improvement_rate: row.total > 0 ? (row.improved / row.total) * 100 : 0,
            avg_improvement: row.avg_improvement || 0
          };
        }
      }
    );
    
    // Get feedback stats
    db.get(
      `SELECT 
        COUNT(*) as total,
        AVG(effectiveness) as avg_effectiveness
      FROM module_feedback`,
      (err, row) => {
        if (!err && row) {
          stats.feedback_stats = {
            total: row.total,
            avg_effectiveness: row.avg_effectiveness || 0
          };
        }
      }
    );
    
    // Get top performing modules
    db.all(
      `SELECT 
        module_name, 
        AVG(effectiveness) as avg_effectiveness,
        COUNT(*) as feedback_count
      FROM module_feedback
      GROUP BY module_name
      HAVING feedback_count >= 3
      ORDER BY avg_effectiveness DESC
      LIMIT 5`,
      (err, rows) => {
        if (!err && rows) {
          stats.top_performing = rows;
        }
      }
    );
    
    // Get modules needing improvement
    db.all(
      `SELECT 
        module_name, 
        AVG(effectiveness) as avg_effectiveness,
        COUNT(*) as feedback_count
      FROM module_feedback
      GROUP BY module_name
      HAVING feedback_count >= 3
      ORDER BY avg_effectiveness ASC
      LIMIT 5`,
      (err, rows) => {
        if (!err && rows) {
          stats.needs_improvement = rows;
        }
      }
    );
    
    // Get most optimized modules
    db.all(
      `SELECT 
        module_name, 
        COUNT(*) as optimization_count,
        AVG(improvement) as avg_improvement
      FROM optimization_results
      GROUP BY module_name
      ORDER BY optimization_count DESC
      LIMIT 5`,
      (err, rows) => {
        if (!err && rows) {
          stats.most_optimized = rows;
        }
      }
    );
    
    // Get recent optimizations
    db.all(
      `SELECT 
        module_name, 
        target_model,
        improvement,
        timestamp,
        applied
      FROM optimization_results
      ORDER BY timestamp DESC
      LIMIT 10`,
      (err, rows) => {
        if (!err && rows) {
          stats.recent_optimizations = rows;
        }
      }
    );
    
    // Write stats to file after all queries complete
    db.close(() => {
      fs.writeFileSync(outputPath, JSON.stringify(stats, null, 2));
      console.log(`Statistics written to ${outputPath}`);
    });
    
  } catch (error) {
    console.error('Error generating stats:', error.message);
  }
}

// Other helper functions (getAllModules, getModuleFeedback, etc.)
// ...

module.exports = { registerCommands };