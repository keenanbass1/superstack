import chalk from 'chalk';
import ora from 'ora';
import inquirer from 'inquirer';
import path from 'path';
import { startSession, endSession, addEntryToCurrentSession, LogEntryType, isSessionActive, getCurrentSessionId, loadSession, getRecentSessions, searchLogs, formatDate, formatTime, generateSessionSummary } from '../utils/logging.js';
import { logger } from '../utils/logger.js';
/**
 * Start a development log session
 */
async function startLogSession(description, options) {
    const spinner = ora('Starting log session').start();
    try {
        // Parse tags
        const tags = options.tags ? options.tags.split(',').map(tag => tag.trim()) : undefined;
        // Determine project name
        let project = options.project;
        if (!project) {
            // Try to get from current directory
            project = path.basename(process.cwd());
        }
        // Start the session
        const session = await startSession(description, project, tags);
        spinner.succeed(`Started log session: ${chalk.green(session.id)}`);
        // Display info about the session
        console.log(chalk.cyan(`\nSession Description: ${description}`));
        console.log(chalk.cyan(`Project: ${project}`));
        if (tags) {
            console.log(chalk.cyan(`Tags: ${tags.join(', ')}`));
        }
        // Suggest next steps
        logger.info('');
        logger.command('dev log add "Your log entry"', 'Add an entry to this session');
        logger.command('dev log end', 'End the current session');
    }
    catch (error) {
        spinner.fail('Failed to start log session');
        logger.error('Error starting session', error);
    }
}
/**
 * End the current log session
 */
async function endLogSession(options) {
    const spinner = ora('Ending log session').start();
    try {
        // Check if there's an active session
        if (!await isSessionActive()) {
            spinner.fail('No active session to end');
            logger.command('dev log start "Description"', 'Start a new session');
            return;
        }
        // Get current session
        const sessionId = await getCurrentSessionId();
        if (!sessionId) {
            spinner.fail('No active session found');
            return;
        }
        // Load session
        const session = await loadSession(sessionId);
        if (!session) {
            spinner.fail(`Could not load session: ${sessionId}`);
            return;
        }
        let summary;
        // If summary option is enabled, generate or ask for a summary
        if (options.summary) {
            spinner.text = 'Generating session summary...';
            // Generate an automated summary
            const generatedSummary = generateSessionSummary(session);
            // Pause the spinner to show the prompt
            spinner.stop();
            // Ask user to confirm or modify summary
            const { userSummary } = await inquirer.prompt([
                {
                    type: 'editor',
                    name: 'userSummary',
                    message: 'Edit the session summary:',
                    default: generatedSummary
                }
            ]);
            summary = userSummary;
            spinner.start('Ending log session...');
        }
        // End the session
        const endedSession = await endSession(summary);
        if (endedSession) {
            spinner.succeed(`Ended log session: ${chalk.green(endedSession.id)}`);
            // Show duration if available
            if (endedSession.startTime && endedSession.endTime) {
                const startDate = new Date(endedSession.startTime);
                const endDate = new Date(endedSession.endTime);
                const durationMs = endDate.getTime() - startDate.getTime();
                const durationMinutes = Math.floor(durationMs / 60000);
                console.log(chalk.cyan(`\nSession duration: ${durationMinutes} minutes`));
            }
            // Show summary if available
            if (summary) {
                console.log(chalk.cyan('\nSession summary:'));
                console.log(summary);
            }
            // Suggest next step
            logger.info('');
            logger.command('dev log start "Description"', 'Start a new session');
        }
    }
    catch (error) {
        spinner.fail('Failed to end log session');
        logger.error('Error ending session', error);
    }
}
/**
 * Add a general log entry to the current session
 */
async function addLogEntry(content, options) {
    const spinner = ora('Adding log entry').start();
    try {
        // Parse tags
        const tags = options.tags ? options.tags.split(',').map(tag => tag.trim()) : undefined;
        // Determine entry type
        let entryType = LogEntryType.NOTE;
        if (options.type) {
            switch (options.type.toLowerCase()) {
                case 'challenge':
                    entryType = LogEntryType.CHALLENGE;
                    break;
                case 'solution':
                    entryType = LogEntryType.SOLUTION;
                    break;
                case 'decision':
                    entryType = LogEntryType.DECISION;
                    break;
                case 'discovery':
                    entryType = LogEntryType.DISCOVERY;
                    break;
                default:
                    entryType = LogEntryType.NOTE;
            }
        }
        // Add the entry
        const entry = await addEntryToCurrentSession(entryType, content, tags);
        if (entry) {
            spinner.succeed('Added log entry');
            // Show entry details
            console.log(chalk.cyan(`\nEntry type: ${options.type || 'note'}`));
            console.log(chalk.gray(entry.content));
            if (tags) {
                console.log(chalk.cyan(`Tags: ${tags.join(', ')}`));
            }
        }
    }
    catch (error) {
        spinner.fail('Failed to add log entry');
        logger.error('Error adding entry', error);
        // If not active session, suggest starting one
        if (error instanceof Error && error.message.includes('No active session')) {
            logger.command('dev log start "Description"', 'Start a new session first');
        }
    }
}
/**
 * Add a specific type of log entry
 */
async function addTypedLogEntry(content, type, options) {
    return addLogEntry(content, {
        ...options,
        type: type.toString().toLowerCase()
    });
}
/**
 * Show log entries
 */
async function showLogs(options) {
    const spinner = ora('Loading logs').start();
    try {
        // If session is specified, show that session
        if (options.session) {
            const session = await loadSession(options.session);
            if (!session) {
                spinner.fail(`Session not found: ${options.session}`);
                return;
            }
            spinner.succeed(`Loaded session: ${chalk.green(session.id)}`);
            // Format session as text or JSON
            if (options.json) {
                console.log(JSON.stringify(session, null, 2));
            }
            else {
                // Display session details
                console.log(chalk.cyan(`\nSession: ${session.id}`));
                console.log(chalk.cyan(`Description: ${session.description}`));
                const startDateFormatted = formatDate(session.startTime) + ' ' + formatTime(session.startTime);
                console.log(chalk.cyan(`Started: ${startDateFormatted}`));
                if (session.endTime) {
                    const endDateFormatted = formatDate(session.endTime) + ' ' + formatTime(session.endTime);
                    console.log(chalk.cyan(`Ended: ${endDateFormatted}`));
                    // Calculate duration
                    const startDate = new Date(session.startTime);
                    const endDate = new Date(session.endTime);
                    const durationMs = endDate.getTime() - startDate.getTime();
                    const durationMinutes = Math.floor(durationMs / 60000);
                    console.log(chalk.cyan(`Duration: ${durationMinutes} minutes`));
                }
                else {
                    console.log(chalk.yellow('Status: Active (not ended)'));
                }
                if (session.project) {
                    console.log(chalk.cyan(`Project: ${session.project}`));
                }
                if (session.tags && session.tags.length > 0) {
                    console.log(chalk.cyan(`Tags: ${session.tags.join(', ')}`));
                }
                // Show entries
                if (session.entries && session.entries.length > 0) {
                    console.log(chalk.cyan('\nEntries:'));
                    for (const entry of session.entries) {
                        // Skip internal entries
                        if (entry.type === LogEntryType.SESSION_START ||
                            (entry.type === LogEntryType.SESSION_END && !session.summary)) {
                            continue;
                        }
                        const entryTimeFormatted = formatTime(entry.timestamp);
                        let entryTypeStr = '';
                        switch (entry.type) {
                            case LogEntryType.NOTE:
                                entryTypeStr = chalk.blue('Note');
                                break;
                            case LogEntryType.CHALLENGE:
                                entryTypeStr = chalk.red('Challenge');
                                break;
                            case LogEntryType.SOLUTION:
                                entryTypeStr = chalk.green('Solution');
                                break;
                            case LogEntryType.DECISION:
                                entryTypeStr = chalk.yellow('Decision');
                                break;
                            case LogEntryType.DISCOVERY:
                                entryTypeStr = chalk.magenta('Discovery');
                                break;
                            case LogEntryType.SESSION_END:
                                entryTypeStr = chalk.cyan('Summary');
                                break;
                        }
                        console.log(chalk.gray(`\n[${entryTimeFormatted}] ${entryTypeStr}`));
                        console.log(entry.content);
                        if (entry.tags && entry.tags.length > 0) {
                            console.log(chalk.cyan(`Tags: ${entry.tags.join(', ')}`));
                        }
                    }
                }
                // Show summary
                if (session.summary) {
                    console.log(chalk.cyan('\nSummary:'));
                    console.log(session.summary);
                }
            }
            return;
        }
        // If recent is specified, show recent sessions
        if (options.recent !== undefined) {
            const recentLimit = typeof options.recent === 'number' ? options.recent : 5;
            const recentSessions = await getRecentSessions(recentLimit, options.project);
            if (recentSessions.length === 0) {
                spinner.info('No recent sessions found');
                return;
            }
            spinner.succeed(`Found ${recentSessions.length} recent sessions`);
            // Format sessions as text or JSON
            if (options.json) {
                console.log(JSON.stringify(recentSessions, null, 2));
            }
            else {
                console.log(chalk.cyan('\nRecent Sessions:'));
                for (const session of recentSessions) {
                    const dateFormatted = formatDate(session.startTime);
                    const isActive = !session.endTime;
                    console.log(`\n${chalk.green(session.id)} - ${dateFormatted} ${isActive ? chalk.yellow('[Active]') : ''}`);
                    console.log(`  ${session.description}`);
                    if (session.project) {
                        console.log(`  Project: ${session.project}`);
                    }
                    if (session.tags && session.tags.length > 0) {
                        console.log(`  Tags: ${session.tags.join(', ')}`);
                    }
                    // Show entry counts
                    if (session.entries) {
                        const entryCount = session.entries.filter(e => e.type !== LogEntryType.SESSION_START &&
                            e.type !== LogEntryType.SESSION_END).length;
                        if (entryCount > 0) {
                            console.log(`  Entries: ${entryCount}`);
                        }
                    }
                    // Show command to view full session
                    logger.command(`dev log show --session=${session.id}`, 'View complete session');
                }
            }
            return;
        }
        // Otherwise, show active session if there is one
        if (await isSessionActive()) {
            const sessionId = await getCurrentSessionId();
            if (sessionId) {
                const session = await loadSession(sessionId);
                if (session) {
                    spinner.succeed('Found active session');
                    console.log(chalk.cyan(`\nActive Session: ${session.id}`));
                    console.log(chalk.cyan(`Description: ${session.description}`));
                    const startDateFormatted = formatDate(session.startTime) + ' ' + formatTime(session.startTime);
                    console.log(chalk.cyan(`Started: ${startDateFormatted}`));
                    if (session.project) {
                        console.log(chalk.cyan(`Project: ${session.project}`));
                    }
                    if (session.tags && session.tags.length > 0) {
                        console.log(chalk.cyan(`Tags: ${session.tags.join(', ')}`));
                    }
                    // Show entries count
                    if (session.entries) {
                        const entryCount = session.entries.filter(e => e.type !== LogEntryType.SESSION_START &&
                            e.type !== LogEntryType.SESSION_END).length;
                        console.log(chalk.cyan(`Entries: ${entryCount}`));
                    }
                    // Suggest commands
                    logger.info('');
                    logger.command('dev log add "Your log entry"', 'Add an entry to this session');
                    logger.command('dev log end', 'End the current session');
                    logger.command(`dev log show --session=${session.id}`, 'View complete session');
                    return;
                }
            }
        }
        // No active session, suggest showing recent sessions
        spinner.info('No active session');
        logger.command('dev log start "Description"', 'Start a new session');
        logger.command('dev log show --recent=5', 'Show recent sessions');
    }
    catch (error) {
        spinner.fail('Failed to load logs');
        logger.error('Error loading logs', error);
    }
}
/**
 * Search logs for a term
 */
async function searchLogEntries(term, options) {
    const spinner = ora(`Searching logs for: ${term}`).start();
    try {
        const results = await searchLogs(term, {
            maxResults: options.limit || 10,
            project: options.project,
            startDate: options.startDate,
            endDate: options.endDate
        });
        if (results.length === 0) {
            spinner.info(`No results found for: ${term}`);
            return;
        }
        spinner.succeed(`Found ${results.length} matches for: ${term}`);
        // Display results
        console.log(chalk.cyan('\nSearch Results:'));
        for (const result of results) {
            console.log(`\n${chalk.green(result.sessionId)}`);
            console.log(result.context);
            // Suggest viewing full session
            logger.command(`dev log show --session=${result.sessionId}`, 'View complete session');
        }
    }
    catch (error) {
        spinner.fail(`Search failed for: ${term}`);
        logger.error('Error searching logs', error);
    }
}
export default function (program) {
    const logCommand = program
        .command('log')
        .description('Manage development logs');
    // Start a log session
    logCommand
        .command('start')
        .description('Start a new development log session')
        .argument('<description>', 'Description of the session')
        .option('-p, --project <project>', 'Project name (defaults to current directory name)')
        .option('-t, --tags <tags>', 'Comma-separated tags for the session')
        .action(startLogSession);
    // End the current log session
    logCommand
        .command('end')
        .description('End the current development log session')
        .option('-s, --summary', 'Create a summary for the session', false)
        .action(endLogSession);
    // Add a log entry
    logCommand
        .command('add')
        .description('Add an entry to the current log session')
        .argument('<content>', 'Content of the log entry')
        .option('-t, --tags <tags>', 'Comma-separated tags for the entry')
        .option('--type <type>', 'Type of entry (note, challenge, solution, decision, discovery)')
        .action(addLogEntry);
    // Add specific entry types
    logCommand
        .command('note')
        .description('Add a note to the current log session')
        .argument('<content>', 'Content of the note')
        .option('-t, --tags <tags>', 'Comma-separated tags for the note')
        .action((content, options) => addTypedLogEntry(content, LogEntryType.NOTE, options));
    logCommand
        .command('challenge')
        .description('Add a challenge entry to the current log session')
        .argument('<content>', 'Description of the challenge')
        .option('-t, --tags <tags>', 'Comma-separated tags for the challenge')
        .action((content, options) => addTypedLogEntry(content, LogEntryType.CHALLENGE, options));
    logCommand
        .command('solution')
        .description('Add a solution entry to the current log session')
        .argument('<content>', 'Description of the solution')
        .option('-t, --tags <tags>', 'Comma-separated tags for the solution')
        .action((content, options) => addTypedLogEntry(content, LogEntryType.SOLUTION, options));
    logCommand
        .command('decision')
        .description('Add a decision entry to the current log session')
        .argument('<content>', 'Description of the decision')
        .option('-t, --tags <tags>', 'Comma-separated tags for the decision')
        .action((content, options) => addTypedLogEntry(content, LogEntryType.DECISION, options));
    logCommand
        .command('discovery')
        .description('Add a discovery entry to the current log session')
        .argument('<content>', 'Description of the discovery')
        .option('-t, --tags <tags>', 'Comma-separated tags for the discovery')
        .action((content, options) => addTypedLogEntry(content, LogEntryType.DISCOVERY, options));
    // Show logs
    logCommand
        .command('show')
        .description('Show development logs')
        .option('-d, --date <date>', 'Show logs for a specific date (YYYY-MM-DD)')
        .option('-s, --session <session>', 'Show a specific session')
        .option('-p, --project <project>', 'Show logs for a specific project')
        .option('-r, --recent [count]', 'Show recent sessions', (value) => value ? parseInt(value) : 5)
        .option('-j, --json', 'Output as JSON', false)
        .action(showLogs);
    // Search logs
    logCommand
        .command('search')
        .description('Search development logs')
        .argument('<term>', 'Search term')
        .option('-l, --limit <limit>', 'Maximum number of results', (value) => parseInt(value))
        .option('-p, --project <project>', 'Search in a specific project')
        .option('--start-date <date>', 'Start date for search range (YYYY-MM-DD)')
        .option('--end-date <date>', 'End date for search range (YYYY-MM-DD)')
        .action(searchLogEntries);
    return logCommand;
}
//# sourceMappingURL=log.js.map