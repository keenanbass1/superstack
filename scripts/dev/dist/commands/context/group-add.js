import { Command } from 'commander';
import ora from 'ora';
import chalk from 'chalk';
import { getContextGroups, addGroupToActiveContext, getActiveContext } from '../../utils/contextModules.js';
import { logger } from '../../utils/logger.js';
export const groupAddCommand = new Command('group-add')
    .description('Add a context group to active context')
    .argument('<n>', 'Name of the group to add')
    .action(async (name) => {
    const spinner = ora(`Adding group '${name}' to active context...`).start();
    try {
        // Check if group exists
        const groups = await getContextGroups();
        if (!groups[name]) {
            spinner.fail(`Group '${name}' does not exist`);
            logger.command('dev context group-list', 'See available groups');
            return;
        }
        // Add group to active context
        const result = await addGroupToActiveContext(name);
        if (!result) {
            spinner.fail(`Failed to add group '${name}' to active context`);
            return;
        }
        const moduleCount = groups[name].modules.length;
        spinner.succeed(`Added group '${chalk.green(name)}' (${moduleCount} modules) to active context`);
        // Show current active context
        const activeContext = await getActiveContext();
        console.log(chalk.cyan('\nActive context:'));
        activeContext.modules.forEach(module => {
            console.log(`- ${module}`);
        });
        // Suggest next actions
        logger.command('dev context push', 'Push context to clipboard for use with AI tools');
    }
    catch (error) {
        spinner.fail(`Failed to add group '${name}'`);
        logger.error('Error adding group', error);
    }
});
//# sourceMappingURL=group-add.js.map