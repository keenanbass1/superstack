import { Command } from 'commander';
import ora from 'ora';
import chalk from 'chalk';
import { 
  getAllContextModules, 
  addModulesToActiveContext, 
  getActiveContext 
} from '../../utils/contextModules.js';
import { logger } from '../../utils/logger.js';

export const addCommand = new Command('add')
  .description('Add module(s) to active context')
  .argument('<modules...>', 'Module paths to add (e.g., design/principles/typography)')
  .action(async (modulePaths) => {
    const spinner = ora('Adding modules to active context...').start();
    
    try {
      // Verify modules exist
      const allModules = await getAllContextModules();
      const allPaths = allModules.map(m => m.path);
      
      const invalidModules = modulePaths.filter((path: string) => !allPaths.includes(path));
      if (invalidModules.length > 0) {
        spinner.fail(`Invalid module paths: ${invalidModules.join(', ')}`);
        logger.info('Available modules:');
        logger.command('dev context list', 'See all available modules');
        return;
      }
      
      // Add to active context
      await addModulesToActiveContext(modulePaths);
      
      spinner.succeed(`Added ${chalk.green(modulePaths.length)} module(s) to active context`);
      
      // Show current active context
      const activeContext = await getActiveContext();
      console.log(chalk.cyan('\nActive context:'));
      activeContext.modules.forEach(module => {
        console.log(`- ${module}`);
      });
      
      // Suggest next actions
      logger.command('dev context push', 'Push context to clipboard for use with AI tools');
      
    } catch (error) {
      spinner.fail('Failed to add modules');
      logger.error('Error adding modules', error as Error);
    }
  });
