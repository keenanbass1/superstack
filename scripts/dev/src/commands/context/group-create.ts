import { Command } from 'commander';
import ora from 'ora';
import chalk from 'chalk';
import { 
  getAllContextModules, 
  createContextGroup, 
  getContextGroups 
} from '../../utils/contextModules.js';
import { logger } from '../../utils/logger.js';

export const groupCreateCommand = new Command('group-create')
  .description('Create a new context group')
  .argument('<name>', 'Name for the group')
  .argument('<modules...>', 'Module paths to include in the group')
  .option('-d, --description <description>', 'Description for the group')
  .action(async (name, modulePaths, options) => {
    // Check if group name already exists
    const spinner = ora(`Creating context group '${name}'...`).start();
    
    try {
      const groups = await getContextGroups();
      
      if (groups[name]) {
        spinner.fail(`Group '${name}' already exists`);
        return;
      }
      
      // Verify modules exist
      const allModules = await getAllContextModules();
      const allPaths = allModules.map(m => m.path);
      
      const invalidModules = modulePaths.filter(path => !allPaths.includes(path));
      if (invalidModules.length > 0) {
        spinner.fail(`Invalid module paths: ${invalidModules.join(', ')}`);
        logger.info('Available modules:');
        logger.command('dev context list', 'See all available modules');
        return;
      }
      
      // Create the group
      await createContextGroup(name, modulePaths, options.description);
      
      spinner.succeed(`Created context group '${chalk.green(name)}' with ${modulePaths.length} modules`);
      
      // Suggest next command
      logger.command(`dev context group-add ${name}`, 'Add this group to active context');
      
    } catch (error) {
      spinner.fail(`Failed to create group '${name}'`);
      logger.error('Error creating group', error as Error);
    }
  });
