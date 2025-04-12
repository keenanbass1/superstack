import { Command } from 'commander';
import ora from 'ora';
import chalk from 'chalk';
import clipboardy from 'clipboardy';
import { 
  getActiveContext, 
  getFormattedActiveContext 
} from '../../utils/contextModules.js';
import { logger } from '../../utils/logger.js';

export const pushCommand = new Command('push')
  .description('Push active context to clipboard or AI tool')
  .option('-t, --target <target>', 'Target destination (clipboard, claude, gpt)', 'clipboard')
  .action(async (options) => {
    // Check if we have active context
    const activeContext = await getActiveContext();
    
    if (activeContext.modules.length === 0) {
      logger.error('No active context modules');
      logger.command('dev context add <module>', 'Add modules to context first');
      return;
    }
    
    const spinner = ora('Preparing context...').start();
    
    try {
      // Format the context
      const formattedContext = await getFormattedActiveContext();
      
      // Push to destination
      if (options.target === 'clipboard') {
        await clipboardy.write(formattedContext);
        spinner.succeed('Context copied to clipboard');
        
        console.log(chalk.cyan(`\nPushed ${activeContext.modules.length} context modules to clipboard`));
        console.log('Paste this context into your AI tool of choice');
      } 
      else if (options.target === 'claude' || options.target === 'gpt') {
        // For now, just copy to clipboard with a note about the target
        await clipboardy.write(formattedContext);
        spinner.succeed(`Context copied to clipboard for ${options.target}`);
        spinner.info(`Direct ${options.target} API integration not yet implemented`);
        
        console.log(chalk.cyan(`\nPushed ${activeContext.modules.length} context modules`));
        console.log(`Paste this context into ${options.target}`);
      }
      else {
        spinner.fail(`Unknown target: ${options.target}`);
        logger.error('Supported targets: clipboard, claude, gpt');
      }
      
    } catch (error) {
      spinner.fail('Failed to push context');
      logger.error('Error pushing context', error as Error);
    }
  });
