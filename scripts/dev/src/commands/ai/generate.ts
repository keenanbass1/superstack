import fs from 'fs-extra';
import path from 'path';
import { log, section } from '../../utils/logger.js';
import { getPaths, isSuperstackProject, getProjectRoot } from '../../utils/paths.js';
import inquirer from 'inquirer';
import clipboardy from 'clipboardy';

interface GenerateOptions {
  description?: string;
  model: string;
  context: boolean;
}

export async function generate(type: string, options: GenerateOptions): Promise<void> {
  section(`AI Generation: ${type}`);
  
  // Get description if not provided
  let description = options.description;
  if (!description) {
    const { desc } = await inquirer.prompt([{
      type: 'input',
      name: 'desc',
      message: `Describe the ${type} you want to generate:`,
      validate: input => input.length > 0 ? true : 'Description is required'
    }]);
    
    description = desc;
  }
  
  // Get project context if requested
  let contextContent = '';
  
  if (options.context && isSuperstackProject()) {
    const projectRoot = getProjectRoot();
    if (projectRoot) {
      const contextFilePath = path.join(projectRoot, '.superstack', 'context', 'project-context.md');
      
      if (fs.existsSync(contextFilePath)) {
        contextContent = fs.readFileSync(contextFilePath, 'utf8');
      } else {
        log('Project context not found. Run "dev context init" to create it.', 'warning');
      }
    }
  }
  
  // Get the appropriate generation prompt template
  const { templatesDir } = getPaths();
  let promptTemplatePath = path.join(templatesDir, 'prompts', `${type}-generation.md`);
  
  if (!fs.existsSync(promptTemplatePath)) {
    // Fall back to generic template
    promptTemplatePath = path.join(templatesDir, 'prompts', 'generation.md');
  }
  
  let promptTemplate = '';
  
  if (fs.existsSync(promptTemplatePath)) {
    promptTemplate = fs.readFileSync(promptTemplatePath, 'utf8');
  } else {
    // Default template if not found
    promptTemplate = `# ${type.charAt(0).toUpperCase() + type.slice(1)} Generation Request

## Description
{{DESCRIPTION}}

## Project Context
{{CONTEXT}}

Please generate a ${type} based on the description above. Consider:
1. Best practices for ${type} design and implementation
2. Performance and maintainability
3. Clear documentation and usage examples
4. Edge cases and error handling
`;
  }
  
  // Prepare prompt
  const prompt = promptTemplate
    .replace(/\{\{DESCRIPTION\}\}/g, description)
    .replace(/\{\{CONTEXT\}\}/g, contextContent || 'No context provided')
    .replace(/\{\{TYPE\}\}/g, type);
  
  // Copy to clipboard
  try {
    clipboardy.writeSync(prompt);
    log('Generation prompt copied to clipboard.', 'success');
    
    // Provide instructions based on model
    if (options.model === 'claude') {
      log('Open Claude and paste this prompt to generate your content.', 'info');
    } else if (options.model === 'gpt') {
      log('Open ChatGPT and paste this prompt to generate your content.', 'info');
    } else {
      log(`Open ${options.model} and paste this prompt to generate your content.`, 'info');
    }
  } catch (error) {
    log('Failed to copy prompt to clipboard.', 'error');
    log('Here is the prompt you can copy manually:', 'info');
    console.log('\n' + prompt);
  }
}