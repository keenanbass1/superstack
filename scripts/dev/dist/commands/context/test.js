import { Command } from 'commander';
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';
import chalk from 'chalk';
import { getContextModulesPath } from '../../utils/contextModules.js';

// Command for testing context modules using PromptFoo
export const testCommand = new Command('test')
  .description('Test context modules using PromptFoo')
  .option('-m, --module <moduleName>', 'Specific module to test')
  .option('-c, --config <configPath>', 'Path to a custom test configuration file')
  .option('-v, --verbose', 'Show detailed test output')
  .action(async (options) => {
    try {
      // First check if PromptFoo is installed
      if (!await isPromptFooInstalled()) {
        console.error(chalk.red('PromptFoo is not installed. Installing required packages...'));
        await installPromptFoo();
      }

      // Set up paths
      const testsDir = path.join(process.cwd(), 'tests', 'context');
      const globalConfigPath = path.join(testsDir, 'promptfoo-config.yaml');
      
      // Check if the test directory and config exist
      if (!fs.existsSync(testsDir)) {
        console.log(chalk.yellow('Creating test directory structure...'));
        fs.mkdirSync(testsDir, { recursive: true });
      }

      if (!fs.existsSync(globalConfigPath) && !options.config) {
        console.error(chalk.red('Global test configuration not found at:'), globalConfigPath);
        console.log(chalk.yellow('Please create a test configuration file or specify a custom one with --config'));
        return;
      }

      // If a specific module is provided, test just that module
      if (options.module) {
        await testModule(options.module, options.config, options.verbose);
      } else {
        // Test all modules
        await testAllModules(options.config, options.verbose);
      }
    } catch (error) {
      console.error(chalk.red('Error testing context modules:'), error instanceof Error ? error.message : String(error));
    }
  });

// Check if PromptFoo is installed
async function isPromptFooInstalled() {
  return new Promise((resolve) => {
    const promptfoo = spawn('npx', ['promptfoo', '--version']);
    
    promptfoo.on('close', (code) => {
      resolve(code === 0);
    });
    
    promptfoo.on('error', () => {
      resolve(false);
    });
  });
}

// Install PromptFoo if not present
async function installPromptFoo() {
  return new Promise((resolve, reject) => {
    console.log(chalk.yellow('Installing PromptFoo...'));
    
    const install = spawn('npm', ['install', '--save-dev', 'promptfoo']);
    
    install.stdout.on('data', (data) => {
      console.log(data.toString());
    });
    
    install.stderr.on('data', (data) => {
      console.error(data.toString());
    });
    
    install.on('close', (code) => {
      if (code === 0) {
        console.log(chalk.green('PromptFoo installed successfully!'));
        resolve();
      } else {
        reject(new Error(`Failed to install PromptFoo (exit code: ${code})`));
      }
    });
    
    install.on('error', (err) => {
      reject(new Error(`Failed to install PromptFoo: ${err.message}`));
    });
  });
}

// Find all module directories in the context modules path
async function findModulePaths() {
  const modulesPath = getContextModulesPath();
  
  if (!fs.existsSync(modulesPath)) {
    throw new Error(`Context modules directory not found: ${modulesPath}`);
  }
  
  return fs.readdirSync(modulesPath, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name);
}

// Test a specific module
async function testModule(moduleName, customConfig, verbose) {
  try {
    const modulesPath = getContextModulesPath();
    const modulePath = path.join(modulesPath, moduleName);
    
    if (!fs.existsSync(modulePath)) {
      console.error(chalk.red(`Module "${moduleName}" not found at: ${modulePath}`));
      return;
    }
    
    // Check for a module-specific test config
    const moduleConfigPath = path.join('tests', 'context', `${moduleName}.yaml`);
    const configPath = customConfig || 
                       (fs.existsSync(moduleConfigPath) ? moduleConfigPath : 
                       path.join('tests', 'context', 'promptfoo-config.yaml'));
    
    if (!fs.existsSync(configPath)) {
      console.error(chalk.red(`Test configuration not found at: ${configPath}`));
      return;
    }
    
    console.log(chalk.blue(`Testing module: ${moduleName}`));
    console.log(chalk.gray(`Using config: ${configPath}`));
    
    // Build the command args
    const args = ['promptfoo', 'eval', '--config', configPath];
    
    // Add module path as context for testing
    args.push('--vars.MODULE_PATH=' + modulePath);
    args.push('--vars.MODULE_NAME=' + moduleName);
    
    if (verbose) {
      args.push('--verbose');
    }
    
    // Execute the test
    const test = spawn('npx', args, { stdio: 'inherit' });
    
    await new Promise((resolve, reject) => {
      test.on('close', (code) => {
        if (code === 0) {
          console.log(chalk.green(`✅ Module "${moduleName}" tests completed successfully`));
          resolve(null);
        } else {
          console.error(chalk.red(`❌ Module "${moduleName}" tests failed with exit code: ${code}`));
          reject(new Error(`Tests failed with exit code: ${code}`));
        }
      });
      
      test.on('error', (err) => {
        reject(new Error(`Error running tests: ${err.message}`));
      });
    });
  } catch (error) {
    console.error(chalk.red(`Error testing module "${moduleName}":`), error instanceof Error ? error.message : String(error));
  }
}

// Test all modules in the AI context directory
async function testAllModules(customConfig, verbose) {
  try {
    const modules = await findModulePaths();
    
    if (modules.length === 0) {
      console.log(chalk.yellow('No context modules found to test.'));
      return;
    }
    
    console.log(chalk.blue(`Found ${modules.length} modules to test`));
    
    // Track results
    const results = {
      passed: 0,
      failed: 0,
      modules: {}
    };
    
    // Run tests for each module
    for (const moduleName of modules) {
      try {
        await testModule(moduleName, customConfig, verbose);
        results.passed++;
        results.modules[moduleName] = true;
      } catch (error) {
        results.failed++;
        results.modules[moduleName] = false;
      }
    }
    
    // Summary
    console.log(chalk.bold('\n==== Test Summary ===='));
    console.log(`Total modules: ${modules.length}`);
    console.log(chalk.green(`Passed: ${results.passed}`));
    console.log(chalk.red(`Failed: ${results.failed}`));
    
    // List failed modules if any
    if (results.failed > 0) {
      console.log(chalk.red('\nFailed modules:'));
      Object.entries(results.modules)
        .filter(([_, passed]) => !passed)
        .forEach(([name]) => console.log(chalk.red(`- ${name}`)));
    }
  } catch (error) {
    console.error(chalk.red('Error testing all modules:'), error instanceof Error ? error.message : String(error));
  }
} 