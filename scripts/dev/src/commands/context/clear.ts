import { Command } from 'commander';
import ora from 'ora';
import chalk from 'chalk';
import inquirer from 'inquirer';
import { getActiveContext, clearActiveContext } from '../../utils/contextModules.js';
import { logger } from '../../utils/logger.js';

export const clearCommand = new Command('clear')
  .description('Clear all active context modules')
  .option('-f, --force', 'Skip confirmation', false)
  .action(async (options) => {
    // Check current active context
    const activeContext = await getActiveContext();
    
    if (activeContext.modules.length === 0) {
      console.log(chalk.yellow('No active context modules to clear.'));
      return;
    }
    
    // Confirm unless force option is provided
    if (!options.force) {
      console.log(chalk.cyan('\nCurrently active modules:'));
      activeContext.modules.forEach(module => {
        console.log(`- ${module}`);
      });
      
      const { confirm } = await inquirer.prompt([{
        type: 'confirm',
        name: 'confirm',
        message: `Clear all ${activeContext.modules.length} active context modules?`,
        default: false
      }]);
      
      if (!confirm) {
        logger.info('Operation cancelled');
        return;
      }
    }
    
    const spinner = ora('Clearing active context...').start();
    
    try {
      await clearActiveContext();
      spinner.succeed('All active context modules cleared');
      
      // Suggest next actions
      logger.command('dev context add <module>', 'Add new modules to context');
      logger.command('dev context list', 'See available modules');
      
    } catch (error) {
      spinner.fail('Failed to clear active context');
      logger.error('Error clearing context', error as Error);
    }
  });
