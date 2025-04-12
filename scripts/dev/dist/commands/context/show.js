import { Command } from 'commander';
import ora from 'ora';
import chalk from 'chalk';
import { getModuleContent, getActiveContext } from '../../utils/contextModules.js';
import { logger } from '../../utils/logger.js';
export const showCommand = new Command('show')
    .description('Show content of a context module')
    .argument('[module]', 'Module path to show content')
    .option('-a, --active', 'Show all active modules', false)
    .action(async (modulePath, options) => {
    // Check if showing active or specific module
    if (!modulePath && !options.active) {
        logger.error('Please specify a module path or use --active flag');
        logger.command('dev context list', 'See available modules');
        return;
    }
    // Show specific module
    if (modulePath) {
        const spinner = ora(`Loading module: ${modulePath}...`).start();
        try {
            const content = await getModuleContent(modulePath);
            spinner.stop();
            console.log(chalk.cyan(`\nModule: ${modulePath}`));
            console.log(chalk.cyan('─'.repeat(modulePath.length + 8)));
            console.log(content);
        }
        catch (error) {
            spinner.fail(`Failed to load module: ${modulePath}`);
            logger.error('Module not found or could not be loaded');
            logger.command('dev context list', 'See available modules');
        }
        return;
    }
    // Show all active modules
    if (options.active) {
        const spinner = ora('Loading active context modules...').start();
        try {
            const activeContext = await getActiveContext();
            if (activeContext.modules.length === 0) {
                spinner.info('No active context modules');
                logger.command('dev context add <module>', 'Add modules to context');
                return;
            }
            spinner.stop();
            // Display each module
            for (const modulePath of activeContext.modules) {
                try {
                    const content = await getModuleContent(modulePath);
                    console.log(chalk.cyan(`\nModule: ${modulePath}`));
                    console.log(chalk.cyan('─'.repeat(modulePath.length + 8)));
                    console.log(content);
                    console.log('\n' + chalk.cyan('─'.repeat(40)) + '\n');
                }
                catch (error) {
                    console.log(chalk.red(`\nError loading module: ${modulePath}`));
                }
            }
        }
        catch (error) {
            spinner.fail('Failed to load active context');
            logger.error('Error loading active context', error);
        }
    }
});
//# sourceMappingURL=show.js.map