import fs from 'fs-extra';
import path from 'path';
import os from 'os';
import { log, section } from '../../utils/logger.js';
import { getPaths, isSuperstackProject, getProjectRoot } from '../../utils/paths.js';
import clipboardy from 'clipboardy';
export async function review(filePath, options) {
    section('AI Code Review');
    // Check if path exists
    const resolvedPath = path.resolve(process.cwd(), filePath);
    if (!fs.existsSync(resolvedPath)) {
        log(`Path not found: ${resolvedPath}`, 'error');
        return;
    }
    // Get code content
    let codeContent = '';
    if (fs.statSync(resolvedPath).isDirectory()) {
        log('Reviewing a directory is not supported yet.', 'error');
        return;
    }
    else {
        try {
            codeContent = fs.readFileSync(resolvedPath, 'utf8');
        }
        catch (error) {
            log(`Failed to read file: ${resolvedPath}`, 'error');
            return;
        }
    }
    // Get project context if requested
    let contextContent = '';
    if (options.context && isSuperstackProject()) {
        const projectRoot = getProjectRoot();
        if (projectRoot) {
            const contextFilePath = path.join(projectRoot, '.superstack', 'context', 'project-context.md');
            if (fs.existsSync(contextFilePath)) {
                contextContent = fs.readFileSync(contextFilePath, 'utf8');
            }
            else {
                log('Project context not found. Run "dev context init" to create it.', 'warning');
            }
        }
    }
    // Get code review prompt template
    const { templatesDir } = getPaths();
    const promptTemplatePath = path.join(templatesDir, 'prompts', 'code-review.md');
    let promptTemplate = '';
    if (fs.existsSync(promptTemplatePath)) {
        promptTemplate = fs.readFileSync(promptTemplatePath, 'utf8');
    }
    else {
        // Default template if not found
        promptTemplate = `# Code Review Request

## File to Review
\`\`\`
File: {{FILENAME}}
\`\`\`

## Code Content
\`\`\`
{{CODE}}
\`\`\`

## Project Context
{{CONTEXT}}

Please review this code for:
1. Bugs and potential issues
2. Performance concerns
3. Security vulnerabilities
4. Style and best practices
5. Potential improvements

Provide specific recommendations with code examples where applicable.
`;
    }
    // Prepare prompt
    const prompt = promptTemplate
        .replace(/\{\{FILENAME\}\}/g, path.basename(resolvedPath))
        .replace(/\{\{CODE\}\}/g, codeContent)
        .replace(/\{\{CONTEXT\}\}/g, contextContent || 'No context provided');
    // Copy to clipboard if it's not too large
    if (prompt.length < 10000) {
        try {
            clipboardy.writeSync(prompt);
            log('Code review prompt copied to clipboard.', 'success');
            // Provide instructions based on model
            if (options.model === 'claude') {
                log('Open Claude and paste this prompt to get a code review.', 'info');
            }
            else if (options.model === 'gpt') {
                log('Open ChatGPT and paste this prompt to get a code review.', 'info');
            }
            else {
                log(`Open ${options.model} and paste this prompt to get a code review.`, 'info');
            }
        }
        catch (error) {
            log('Failed to copy prompt to clipboard.', 'error');
            savePromptToFile(prompt);
        }
    }
    else {
        log('The prompt is too large to copy to clipboard.', 'info');
        savePromptToFile(prompt);
    }
}
/**
 * Save the prompt to a temporary file when it's too large for the clipboard
 */
function savePromptToFile(prompt) {
    const tempFilePath = path.join(os.tmpdir(), 'superstack-code-review-prompt.md');
    fs.writeFileSync(tempFilePath, prompt, 'utf8');
    log(`Prompt saved to: ${tempFilePath}`, 'info');
    log('You can open this file and copy its contents to your AI assistant.', 'info');
}
//# sourceMappingURL=review.js.map