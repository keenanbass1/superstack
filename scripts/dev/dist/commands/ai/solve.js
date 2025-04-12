import fs from 'fs-extra';
import path from 'path';
import { log, section } from '../../utils/logger.js';
import { getPaths, isSuperstackProject, getProjectRoot } from '../../utils/paths.js';
import clipboardy from 'clipboardy';
export async function solve(problem, options) {
    section('AI Problem Solving');
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
    // Get problem-solving prompt template
    const { templatesDir } = getPaths();
    const promptTemplatePath = path.join(templatesDir, 'prompts', 'problem-solving.md');
    let promptTemplate = '';
    if (fs.existsSync(promptTemplatePath)) {
        promptTemplate = fs.readFileSync(promptTemplatePath, 'utf8');
    }
    else {
        // Default template if not found
        promptTemplate = `# Problem Solving Request

## Problem Description
{{PROBLEM}}

## Current Context
{{CONTEXT}}

Please help me solve this problem with:
1. A clear understanding of what needs to be done
2. A step-by-step solution approach
3. Code examples if applicable
4. Any considerations or potential issues to watch for
`;
    }
    // Prepare prompt
    const prompt = promptTemplate
        .replace(/\{\{PROBLEM\}\}/g, problem)
        .replace(/\{\{CONTEXT\}\}/g, contextContent || 'No context provided');
    // Copy to clipboard
    try {
        clipboardy.writeSync(prompt);
        log('Problem-solving prompt copied to clipboard.', 'success');
        // Provide instructions based on model
        if (options.model === 'claude') {
            log('Open Claude and paste this prompt to get assistance.', 'info');
        }
        else if (options.model === 'gpt') {
            log('Open ChatGPT and paste this prompt to get assistance.', 'info');
        }
        else {
            log(`Open ${options.model} and paste this prompt to get assistance.`, 'info');
        }
    }
    catch (error) {
        log('Failed to copy prompt to clipboard.', 'error');
        log('Here is the prompt you can copy manually:', 'info');
        console.log('\n' + prompt);
    }
}
//# sourceMappingURL=solve.js.map