import { Command } from 'commander';
import chalk from 'chalk';
import inquirer from 'inquirer';
import fs from 'fs-extra';
import path from 'path';
import ora from 'ora';
import { contextUtils } from '../utils/context.js';
import { logger } from '../utils/logger.js';

// Import our new commands
import { listCommand } from './context/list.js';
import { addCommand } from './context/add.js';
import { removeCommand } from './context/remove.js';
import { clearCommand } from './context/clear.js';
import { showCommand } from './context/show.js';
import { pushCommand } from './context/push.js';
import { groupListCommand } from './context/group-list.js';
import { groupCreateCommand } from './context/group-create.js';
import { groupAddCommand } from './context/group-add.js';
import { groupDeleteCommand } from './context/group-delete.js';

/**
 * Initialize a new project context
 */
async function initContext() {
  const spinner = ora('Initializing project context').start();
  
  try {
    // Check if we're in a project directory
    const currentDir = process.cwd();
    const projectName = path.basename(currentDir);
    
    // Check if context already exists
    if (await contextUtils.contextExists()) {
      spinner.warn('Context file already exists');
      
      const { overwrite } = await inquirer.prompt([{
        type: 'confirm',
        name: 'overwrite',
        message: 'Context file already exists. Overwrite?',
        default: false
      }]);
      
      if (!overwrite) {
        logger.info('Context initialization canceled');
        return;
      }
      
      // Initialize with overwrite
      spinner.start('Creating new context file...');
      await contextUtils.initContext(currentDir, projectName, true);
    } else {
      // Initialize new context
      spinner.text = 'Creating context file...';
      await contextUtils.initContext(currentDir, projectName);
    }
    
    spinner.succeed(`Project context initialized for ${chalk.green(projectName)}`);
    logger.info(`Edit ${chalk.blue('project-context.md')} to add your project details`);
    logger.command('dev context push', 'Update your AI assistants with this context');
  } catch (error) {
    spinner.fail('Failed to initialize context');
    logger.error('Error initializing context', error as Error);
  }
}

/**
 * Validate context against schema
 */
async function validateContext() {
  const spinner = ora('Validating context').start();
  
  try {
    // Check if context exists
    if (!await contextUtils.contextExists()) {
      spinner.fail('No context file found in current directory');
      logger.command('dev context init', 'Create a context file first');
      return;
    }
    
    // Read context file
    const contextContent = await contextUtils.readContext();
    
    // Validate context
    spinner.text = 'Checking for placeholders...';
    const placeholders = await contextUtils.validateContext(contextContent);
    
    if (placeholders.length > 0) {
      spinner.warn('Context contains unfilled placeholders');
      logger.info('\nThe following placeholders need to be filled:');
      
      placeholders.slice(0, 10).forEach(p => logger.info(`- ${p}`));
      
      if (placeholders.length > 10) {
        logger.info(`... and ${placeholders.length - 10} more`);
      }
      
      logger.info(`\nEdit ${chalk.blue('project-context.md')} to fill in these details`);
    } else {
      spinner.succeed('Context validation passed');
      logger.info('All placeholders have been filled in');
    }
    
    // TODO: Implement full schema validation when we add JSON parser
  } catch (error) {
    spinner.fail('Failed to validate context');
    logger.error('Error validating context', error as Error);
  }
}

export default function(program: Command) {
  const contextCommand = program
    .command('context')
    .description('Manage project context for AI assistants');
  
  // Add the original commands
  contextCommand
    .command('init')
    .description('Initialize a new project context file')
    .action(initContext);

  contextCommand
    .command('validate')
    .description('Validate context against schema')
    .action(validateContext);
  
  // Add our new commands
  contextCommand.addCommand(listCommand);
  contextCommand.addCommand(addCommand);
  contextCommand.addCommand(removeCommand);
  contextCommand.addCommand(clearCommand);
  contextCommand.addCommand(showCommand);
  contextCommand.addCommand(pushCommand);
  
  // Add group commands
  contextCommand.addCommand(groupListCommand);
  contextCommand.addCommand(groupCreateCommand);
  contextCommand.addCommand(groupAddCommand);
  contextCommand.addCommand(groupDeleteCommand);
  
  return contextCommand;
}