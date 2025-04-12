import { Command } from 'commander';
import ora from 'ora';
import chalk from 'chalk';
import { getContextGroups } from '../../utils/contextModules.js';
import { logger } from '../../utils/logger.js';
export const groupListCommand = new Command('group-list')
    .description('List available context groups')
    .option('-j, --json', 'Output as JSON', false)
    .action(async (options) => {
    const spinner = ora('Loading context groups...').start();
    try {
        const groups = await getContextGroups();
        const groupNames = Object.keys(groups);
        spinner.stop();
        if (groupNames.length === 0) {
            console.log(chalk.yellow('No context groups found.'));
            logger.command('dev context group-create <name> <modules...>', 'Create a new group');
            return;
        }
        // Output as JSON if requested
        if (options.json) {
            console.log(JSON.stringify(groups, null, 2));
            return;
        }
        // Display groups
        console.log(chalk.cyan(`\nFound ${groupNames.length} context groups:\n`));
        groupNames.forEach(name => {
            const group = groups[name];
            const moduleCount = group.modules.length;
            const created = new Date(group.created).toLocaleDateString();
            console.log(chalk.green(`${name}`) + chalk.gray(` (${moduleCount} modules, created ${created})`));
            if (group.description) {
                console.log(`  ${group.description}`);
            }
            // Show first few modules in the group
            const maxModulesToShow = 3;
            const shownModules = group.modules.slice(0, maxModulesToShow);
            const remainingCount = group.modules.length - maxModulesToShow;
            shownModules.forEach(module => {
                console.log(`  - ${module}`);
            });
            if (remainingCount > 0) {
                console.log(`  - ${chalk.gray(`... and ${remainingCount} more`)}`);
            }
            console.log('');
        });
        // Suggest commands
        logger.command('dev context group-add <name>', 'Add a group to active context');
    }
    catch (error) {
        spinner.fail('Failed to list context groups');
        logger.error('Error listing groups', error);
    }
});
//# sourceMappingURL=group-list.js.map