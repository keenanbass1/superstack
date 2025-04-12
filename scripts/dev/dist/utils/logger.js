import chalk from 'chalk';
import ora from 'ora';
/**
 * Log a message with color and formatting
 */
export function log(message, level = 'info') {
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
export function spinner(text) {
    return ora(text).start();
}
/**
 * Create a section header
 */
export function section(title) {
    console.log('\n' + chalk.bold.cyan(`■ ${title}`));
}
/**
 * Display a command suggestion
 */
export function command(cmd, description) {
    if (description) {
        console.log(`${chalk.gray('$')} ${chalk.green(cmd)}  ${chalk.gray('- ' + description)}`);
    }
    else {
        console.log(`${chalk.gray('$')} ${chalk.green(cmd)}`);
    }
}
// Export a logger object that simulates the standard logger interface
export const logger = {
    log: log,
    info: (message) => log(message, 'info'),
    success: (message) => log(message, 'success'),
    warn: (message) => log(message, 'warning'),
    error: (message, err) => {
        log(message, 'error');
        if (err && process.env.DEBUG) {
            console.error(err);
        }
    },
    debug: (message) => log(message, 'debug'),
    command: command
};
//# sourceMappingURL=logger.js.map