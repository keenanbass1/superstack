import chalk from 'chalk';
import ora from 'ora';

type LogLevel = 'info' | 'success' | 'warning' | 'error' | 'debug';

/**
 * Log a message with color and formatting
 */
export function log(message: string, level: LogLevel = 'info'): void {
  switch (level) {
    case 'success':
      console.log(chalk.green(`✓ ${message}`));
      break;
    case 'warning':
      console.log(chalk.yellow(`⚠ ${message}`));
      break;
    case 'error':
      console.log(chalk.red(`✖ ${message}`));
      break;
    case 'debug':
      if (process.env.DEBUG) {
        console.log(chalk.gray(`🔍 ${message}`));
      }
      break;
    case 'info':
    default:
      console.log(chalk.blue(`ℹ ${message}`));
  }
}

/**
 * Create and return a spinner
 */
export function spinner(text: string) {
  return ora(text).start();
}

/**
 * Create a section header
 */
export function section(title: string): void {
  console.log('\n' + chalk.bold.cyan(`■ ${title}`));
}

/**
 * Display a command suggestion
 */
export function command(cmd: string, description?: string): void {
  if (description) {
    console.log(`${chalk.gray('$')} ${chalk.green(cmd)}  ${chalk.gray('- ' + description)}`);
  } else {
    console.log(`${chalk.gray('$')} ${chalk.green(cmd)}`);
  }
}

// Export a logger object that simulates the standard logger interface
export const logger = {
  log: log,
  info: (message: string) => log(message, 'info'),
  success: (message: string) => log(message, 'success'),
  warn: (message: string) => log(message, 'warning'),
  error: (message: string, err?: Error) => {
    log(message, 'error');
    if (err && process.env.DEBUG) {
      console.error(err);
    }
  },
  debug: (message: string) => log(message, 'debug'),
  command: command
};