#!/usr/bin/env node

import { Command } from 'commander';
import chalk from 'chalk';
import figlet from 'figlet';
import path from 'path';
import os from 'os';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import contextCommand from './commands/context.js';
import aiCommand from './commands/ai.js';
import logCommand from './commands/log.js';
import newCommand from './commands/new.js';
import projectCommand from './commands/project.js';
import { getVersion } from './utils/config.js';
import { log } from './utils/logger.js';
import { ensureSystemPaths, setupEnvironment } from './utils/paths.js';

// Setup environment variables
setupEnvironment();

// Ensure all system paths exist
ensureSystemPaths();

const program = new Command();

// Show banner on help or when no commands are provided
if (process.argv.length <= 2 || process.argv.includes('--help') || process.argv.includes('-h')) {
  console.log(
    chalk.blue(
      figlet.textSync('Superstack', { font: 'Standard' })
    )
  );
}

program
  .name('dev')
  .description('Superstack Developer Workflow System')
  .version(getVersion());

// Register command modules
contextCommand(program);
aiCommand(program);
logCommand(program);
newCommand(program);
projectCommand(program);

// Add placeholder commands for features to be implemented
program
  .command('config')
  .description('[Coming Soon] Manage configuration')
  .action(() => {
    log('The "config" command is coming soon!', 'info');
    log('Check the documentation for updates.', 'info');
  });

program.parse(process.argv);