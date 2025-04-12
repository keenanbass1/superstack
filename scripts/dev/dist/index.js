#!/usr/bin/env node
import { Command } from 'commander';
import chalk from 'chalk';
import figlet from 'figlet';
import contextCommand from './commands/context.js';
import aiCommand from './commands/ai.js';
import logCommand from './commands/log.js';
import { getVersion } from './utils/config.js';
import { log } from './utils/logger.js';
import { ensureSystemPaths } from './utils/paths.js';
// Ensure all system paths exist
ensureSystemPaths();
const program = new Command();
// Show banner on help or when no commands are provided
if (process.argv.length <= 2 || process.argv.includes('--help') || process.argv.includes('-h')) {
    console.log(chalk.blue(figlet.textSync('Superstack', { font: 'Standard' })));
}
program
    .name('dev')
    .description('Superstack Developer Workflow System')
    .version(getVersion());
// Register command modules
contextCommand(program);
aiCommand(program);
logCommand(program);
// Add placeholder commands for features to be implemented
program
    .command('new')
    .description('[Coming Soon] Create a new project')
    .action(() => {
    log('The "new" command is coming soon!', 'info');
    log('Check the documentation for updates.', 'info');
});
program
    .command('config')
    .description('[Coming Soon] Manage configuration')
    .action(() => {
    log('The "config" command is coming soon!', 'info');
    log('Check the documentation for updates.', 'info');
});
program.parse(process.argv);
//# sourceMappingURL=index.js.map