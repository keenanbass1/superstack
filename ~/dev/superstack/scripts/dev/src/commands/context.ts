import { Command } from 'commander';
import chalk from 'chalk';
import path from 'path';
import { spawn } from 'child_process';

// Helper to run the context system command
const runContextCommand = (args: string[] = []): Promise<void> => {
  return new Promise((resolve, reject) => {
    const contextScriptPath = path.join(process.env.HOME || '~', 'dev', 'superstack', 'scripts', 'context');
    const nodeProcess = spawn('node', [path.join(contextScriptPath, 'run.js'), ...args], {
      stdio: 'inherit',
      env: {
        ...process.env,
        FORCE_COLOR: '1' // Ensure colors are passed through
      }
    });

    nodeProcess.on('close', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`Context command failed with code ${code}`));
      }
    });

    nodeProcess.on('error', (err) => {
      reject(err);
    });
  });
};

interface ContextOptions {
  [key: string]: string | boolean | undefined;
}

// Function to create project summary from current directory
export const createProjectSummary = async (): Promise<void> => {
  try {
    console.log(chalk.blue('🧠 Generating Project Summary...'));
    await runContextCommand(['create', 'project-summary', '-i', '-c']);
    console.log(chalk.green('✅ Project summary copied to clipboard'));
  } catch (err) {
    console.error(chalk.red(`Error generating project summary: ${(err as Error).message}`));
  }
};

// Main AI Context command function
export default function contextCommand(program: Command): Command {
  const cmd = program
    .command('context')
    .description('Manage project context for AI assistants');
    
  // Add insights command for AI Context System integration
  const insightsCommand = new Command('insights')
    .description('AI Context Management System')
    .addHelpText('after', `
Examples:
  $ dev context insights create              List available templates and create from one
  $ dev context insights create project-summary -i    Create project summary with interactive prompts
  $ dev context insights list                List all available templates
  $ dev context insights new-template my-template -i  Create new template interactively
    `)
    .argument('[cmd]', 'Context command (create, list, new-template)')
    .argument('[args...]', 'Additional arguments for the context command')
    .action(async (cmd: string | undefined, args: string[], options: ContextOptions) => {
      try {
        console.log(chalk.blue('🧠 AI Context System'));
        
        // Build arguments array
        const commandArgs: string[] = [];
        if (cmd) {
          commandArgs.push(cmd);
          if (args && args.length > 0) {
            commandArgs.push(...args);
          }
        }

        // Map options to arguments
        Object.entries(options).forEach(([key, value]) => {
          if (key !== 'args' && key !== 'command') {
            if (value === true) {
              commandArgs.push(`--${key}`);
            } else if (value !== false && value !== undefined && value !== null) {
              commandArgs.push(`--${key}`, String(value));
            }
          }
        });

        await runContextCommand(commandArgs);
      } catch (err) {
        console.error(chalk.red(`Error running context command: ${(err as Error).message}`));
        process.exit(1);
      }
    });

  // Add summary command as a shortcut
  insightsCommand.command('summary')
    .description('Generate project summary and copy to clipboard')
    .action(createProjectSummary);
    
  // Add the insights command to the context command
  cmd.addCommand(insightsCommand);
  
  return cmd;
} 