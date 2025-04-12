import { Command } from 'commander';
import ora from 'ora';
import chalk from 'chalk';
import inquirer from 'inquirer';
import { getContextGroups, deleteContextGroup } from '../../utils/contextModules.js';
import { logger } from '../../utils/logger.js';
export const groupDeleteCommand = new Command('group-delete')
    .description('Delete a context group')
    .argument('<n>', 'Name of the group to delete')
    .option('-f, --force', 'Skip confirmation', false)
    .action(async (name, options) => {
    // Check if group exists
    const spinner = ora(`Checking group '${name}'...`).start();
    try {
        const groups = await getContextGroups();
        if (!groups[name]) {
            spinner.fail(`Group '${name}' does not exist`);
            logger.command('dev context group-list', 'See available groups');
            return;
        }
        spinner.stop();
        // Confirm deletion
        if (!options.force) {
            const moduleCount = groups[name].modules.length;
            console.log(chalk.cyan(`\nGroup: ${name}`));
            console.log(`Contains ${moduleCount} modules:`);
            groups[name].modules.forEach(module => {
                console.log(`- ${module}`);
            });
            const { confirm } = await inquirer.prompt([{
                    type: 'confirm',
                    name: 'confirm',
                    message: `Delete group '${name}'?`,
                    default: false
                }]);
            if (!confirm) {
                logger.info('Operation cancelled');
                return;
            }
            spinner.start(`Deleting group '${name}'...`);
        }
        // Delete the group
        const result = await deleteContextGroup(name);
        if (result) {
            spinner.succeed(`Deleted group '${chalk.green(name)}'`);
        }
        else {
            spinner.fail(`Failed to delete group '${name}'`);
        }
    }
    catch (error) {
        spinner.fail(`Failed to delete group '${name}'`);
        logger.error('Error deleting group', error);
    }
});
//# sourceMappingURL=group-delete.js.map