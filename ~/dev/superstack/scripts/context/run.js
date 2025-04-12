#!/usr/bin/env node

/**
 * Runner script for AI Context System
 * This script initializes the context command and executes it
 */

const contextCommand = require('./cli-command');

// Install required dependencies if not already installed
const checkDependencies = () => {
  const requiredDeps = ['commander', 'chalk', 'handlebars', 'inquirer'];
  let missingDeps = [];
  
  for (const dep of requiredDeps) {
    try {
      require.resolve(dep);
    } catch (e) {
      missingDeps.push(dep);
    }
  }
  
  if (missingDeps.length > 0) {
    console.log(`Installing required dependencies: ${missingDeps.join(', ')}...`);
    const { execSync } = require('child_process');
    try {
      execSync(`npm install ${missingDeps.join(' ')} --no-save`, { stdio: 'inherit' });
    } catch (err) {
      console.error(`Failed to install dependencies: ${err.message}`);
      process.exit(1);
    }
  }
};

// Main function
const main = async () => {
  try {
    // Check dependencies first
    checkDependencies();
    
    // Parse command-line arguments and execute
    contextCommand.parse(process.argv);

    // If no arguments were provided, display help
    if (process.argv.length <= 2) {
      contextCommand.help();
    }
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
};

// Run the script
main(); 