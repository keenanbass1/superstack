import chalk from 'chalk';
import fs from 'fs-extra';
import path from 'path';
import { format } from 'date-fns';
import inquirer from 'inquirer';
import ora from 'ora';
import { fileURLToPath } from 'url';
// Get directory name
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
// Paths
const DEV_ROOT = path.resolve(process.env.DEV_ROOT || path.join(__dirname, '../../../../../'));
const LOGS_DIR = path.join(DEV_ROOT, 'superstack/logs');
/**
 * Add a new log entry
 */
async function addLog(message, options) {
    const spinner = ora('Logging entry').start();
    try {
        // Ensure logs directory exists
        await fs.ensureDir(LOGS_DIR);
        // Format today's date for filename
        const today = new Date();
        const dateStr = format(today, 'yyyy-MM-dd');
        const timeStr = format(today, 'HH:mm:ss');
        // Determine log file path
        const logFilePath = path.join(LOGS_DIR, `${dateStr}.md`);
        // Check if file exists already
        const fileExists = await fs.pathExists(logFilePath);
        // Current project
        const currentDir = process.cwd();
        const projectName = path.basename(currentDir);
        // Parse tags
        const tags = options.tags ? options.tags.split(',').map(t => t.trim()) : [];
        // Create log entry
        let logEntry = '';
        if (!fileExists) {
            // Create header for new file
            logEntry += `# Development Log: ${dateStr}\n\n`;
        }
        // Start session if requested
        if (options.session) {
            logEntry += `## Session: ${timeStr} - Project: ${projectName}\n\n`;
            logEntry += `**Focus:** ${message}\n\n`;
        }
        else {
            // Add timestamp and project
            logEntry += `### ${timeStr} | Project: ${projectName}\n\n`;
            logEntry += `${message}\n\n`;
            // Add tags if present
            if (tags.length > 0) {
                logEntry += `Tags: ${tags.map(t => `#${t}`).join(' ')}\n\n`;
            }
            logEntry += `---\n\n`;
        }
        // Append to log file
        await fs.appendFile(logFilePath, logEntry);
        spinner.succeed(`Log entry added to ${dateStr}.md`);
    }
    catch (error) {
        spinner.fail('Failed to add log entry');
        console.error(chalk.red('Error:'), error);
    }
}
/**
 * Start a new session log
 */
async function startSession(focus) {
    return addLog(focus, { session: true });
}
/**
 * End a session with summary
 */
async function endSession(options) {
    const spinner = ora('Ending session').start();
    try {
        // Format today's date for filename
        const today = new Date();
        const dateStr = format(today, 'yyyy-MM-dd');
        const timeStr = format(today, 'HH:mm:ss');
        // Determine log file path
        const logFilePath = path.join(LOGS_DIR, `${dateStr}.md`);
        if (!await fs.pathExists(logFilePath)) {
            spinner.fail('No active session found for today');
            return;
        }
        let summary = '';
        // If summary option is enabled, prompt for summary
        if (options.summary) {
            spinner.stop();
            const responses = await inquirer.prompt([
                {
                    type: 'editor',
                    name: 'summary',
                    message: 'Enter session summary:',
                }
            ]);
            summary = responses.summary;
            spinner.start('Adding session summary');
        }
        // Create session end entry
        let logEntry = `### Session Ended: ${timeStr}\n\n`;
        if (summary) {
            logEntry += `**Summary:**\n\n${summary}\n\n`;
        }
        logEntry += `---\n\n`;
        // Append to log file
        await fs.appendFile(logFilePath, logEntry);
        spinner.succeed('Session ended');
    }
    catch (error) {
        spinner.fail('Failed to end session');
        console.error(chalk.red('Error:'), error);
    }
}
/**
 * Show recent logs
 */
async function showLogs(options) {
    const spinner = ora('Fetching logs').start();
    try {
        const days = options.days || 1;
        // Ensure logs directory exists
        if (!await fs.pathExists(LOGS_DIR)) {
            spinner.info('No logs directory found');
            return;
        }
        // Get log files
        const files = await fs.readdir(LOGS_DIR);
        const logFiles = files
            .filter(f => f.endsWith('.md'))
            .sort()
            .reverse()
            .slice(0, days);
        if (logFiles.length === 0) {
            spinner.info('No logs found');
            return;
        }
        spinner.succeed(`Found ${logFiles.length} log files`);
        // Display each log file
        for (const file of logFiles) {
            const filePath = path.join(LOGS_DIR, file);
            const content = await fs.readFile(filePath, 'utf8');
            // If project filter is specified, only show entries for that project
            if (options.project) {
                const projectPattern = new RegExp(`Project: ${options.project}`, 'i');
                const lines = content.split('\n');
                let includeLines = false;
                let filteredContent = '';
                for (const line of lines) {
                    if (line.startsWith('##') || line.startsWith('###')) {
                        includeLines = projectPattern.test(line);
                    }
                    if (includeLines) {
                        filteredContent += line + '\n';
                    }
                }
                if (filteredContent.trim()) {
                    console.log(chalk.bold(`\n${file} (filtered for ${options.project})\n`));
                    console.log(filteredContent);
                }
            }
            else {
                console.log(chalk.bold(`\n${file}\n`));
                console.log(content);
            }
        }
    }
    catch (error) {
        spinner.fail('Failed to show logs');
        console.error(chalk.red('Error:'), error);
    }
}
export default function (program) {
    const logCommand = program
        .command('log')
        .description('Log development activities and insights');
    // Basic log entry
    logCommand
        .argument('[message]', 'Log message')
        .option('-t, --tags <tags>', 'Comma-separated tags')
        .action((message, options) => {
        if (!message) {
            // If no message provided, show recent logs
            showLogs({});
        }
        else {
            addLog(message, options);
        }
    });
    // Session management
    logCommand
        .command('start')
        .description('Start a new development session')
        .argument('<focus>', 'Session focus')
        .action(startSession);
    logCommand
        .command('end')
        .description('End current development session')
        .option('-s, --summary', 'Add session summary')
        .action(endSession);
    // Log viewing
    logCommand
        .command('show')
        .description('Show recent logs')
        .option('-d, --days <number>', 'Number of days to show', (v) => parseInt(v, 10))
        .option('-p, --project <name>', 'Filter by project name')
        .action(showLogs);
    return logCommand;
}
//# sourceMappingURL=log.js.map