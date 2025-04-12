import fs from 'fs-extra';
import path from 'path';
import { log, spinner, section } from '../../utils/logger.js';
import { isSuperstackProject, getProjectRoot } from '../../utils/paths.js';
import clipboardy from 'clipboardy';
export async function push(options) {
    // Check if current directory is a Superstack project
    if (!isSuperstackProject()) {
        log('Current directory is not a Superstack project.', 'error');
        log('Run this command from a Superstack project directory or create a new project with "dev new".', 'info');
        return;
    }
    section('Pushing Project Context');
    const projectRoot = getProjectRoot();
    if (!projectRoot) {
        log('Unable to find project root.', 'error');
        return;
    }
    // Check if context exists
    const contextFilePath = path.join(projectRoot, '.superstack', 'context', 'project-context.md');
    if (!fs.existsSync(contextFilePath)) {
        log('Project context not found.', 'error');
        log('Initialize project context first with "dev context init".', 'info');
        return;
    }
    // Read context
    const contextContent = fs.readFileSync(contextFilePath, 'utf8');
    // Push to Claude
    if (options.target === 'all' || options.target === 'claude') {
        const spin = spinner('Preparing context for Claude...');
        try {
            // Create Claude-specific context directory
            fs.ensureDirSync(path.join(projectRoot, '.superstack', 'context', 'claude'));
            fs.writeFileSync(path.join(projectRoot, '.superstack', 'context', 'claude', 'project-context.md'), contextContent, 'utf8');
            // Copy to clipboard
            clipboardy.writeSync(contextContent);
            spin.succeed('Context prepared for Claude');
            log('Context copied to clipboard ready to paste into Claude.', 'info');
        }
        catch (error) {
            spin.fail('Failed to prepare context for Claude');
            console.error(error);
        }
    }
    // Push to GPT
    if (options.target === 'all' || options.target === 'gpt') {
        const spin = spinner('Preparing context for GPT...');
        try {
            // Create GPT-specific context directory
            fs.ensureDirSync(path.join(projectRoot, '.superstack', 'context', 'gpt'));
            fs.writeFileSync(path.join(projectRoot, '.superstack', 'context', 'gpt', 'project-context.md'), contextContent, 'utf8');
            spin.succeed('Context prepared for GPT');
            log('Context is ready to be pasted into ChatGPT.', 'info');
            if (options.target === 'gpt') {
                // Only copy to clipboard if GPT is specifically targeted
                // Otherwise Claude's copy takes precedence
                clipboardy.writeSync(contextContent);
                log('Context copied to clipboard ready to paste into ChatGPT.', 'info');
            }
        }
        catch (error) {
            spin.fail('Failed to prepare context for GPT');
            console.error(error);
        }
    }
    // Push to Cursor
    if (options.target === 'all' || options.target === 'cursor') {
        const spin = spinner('Preparing context for Cursor...');
        try {
            // Create Cursor-specific context directory
            fs.ensureDirSync(path.join(projectRoot, '.superstack', 'context', 'cursor'));
            fs.writeFileSync(path.join(projectRoot, '.superstack', 'context', 'cursor', 'project-context.md'), contextContent, 'utf8');
            spin.succeed('Context prepared for Cursor');
            log('Context is ready to be used in Cursor AI.', 'info');
            log('In Cursor, press Ctrl+L to start a new conversation and paste the context.', 'info');
        }
        catch (error) {
            spin.fail('Failed to prepare context for Cursor');
            console.error(error);
        }
    }
    log('Context push completed.', 'success');
    log('Your AI assistants now have the latest project context.', 'info');
}
//# sourceMappingURL=push.js.map