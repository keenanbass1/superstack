import { Command } from 'commander';
import ora from 'ora';
import chalk from 'chalk';
import { 
  getActiveContext, 
  removeModulesFromActiveContext 
} from '../../utils/contextModules.js';
import { logger } from '../../utils/logger.js';

export const removeCommand = new Command('remove')
  .description('Remove module(s) from active context')
  .argument('<modules...>', 'Module paths to remove')
  .action(async (modulePaths) => {
    const spinner = ora('Removing modules from active context...').start();
    
    try {
      // Get current active context
      const activeContext = await getActiveContext();
      
      // Check if modules are in active context
      const modulesToRemove = modulePaths.filter((path: string) => 
        activeContext.modules.includes(path)
      );
      
      if (modulesToRemove.length === 0) {
        spinner.fail('None of the specified modules are in the active context');
        logger.command('dev context list --active', 'See currently active modules');
        return;
      }
      
      // Remove from active context
      await removeModulesFromActiveContext(modulesToRemove);
      
      spinner.succeed(`Removed ${chalk.yellow(modulesToRemove.length)} module(s) from active context`);
      
      // Show updated active context
      const updatedContext = await getActiveContext();
      
      if (updatedContext.modules.length > 0) {
        console.log(chalk.cyan('\nRemaining active context:'));
        updatedContext.modules.forEach(module => {
          console.log(`- ${module}`);
        });
      } else {
        console.log(chalk.cyan('\nNo active context modules remaining.'));
      }
      
    } catch (error) {
      spinner.fail('Failed to remove modules');
      logger.error('Error removing modules', error as Error);
    }
  });
