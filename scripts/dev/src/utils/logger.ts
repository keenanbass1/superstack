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