/**
 * AI Context System - Main Entry Point
 * 
 * This module provides a comprehensive system for managing AI context data
 * including templates, clipboard operations, and context management.
 */

const cliIntegration = require('./cli-integration');
const templateParser = require('./template-parser');
const fs = require('fs');
const path = require('path');
const chalk = require('chalk');

/**
 * Get the root directory for context storage
 * @returns {string} Path to context storage directory
 */
const getContextRoot = () => {
  return path.join(process.env.HOME, 'dev', 'superstack', 'insights');
};

/**
 * Initialize the context system
 * @returns {Promise<boolean>} Success status
 */
const initialize = async () => {
  const contextRoot = getContextRoot();
  const templateDir = path.join(contextRoot, 'templates');
  
  try {
    // Create directories if they don't exist
    if (!fs.existsSync(contextRoot)) {
      await fs.promises.mkdir(contextRoot, { recursive: true });
      console.log(chalk.green(`Created context root directory: ${contextRoot}`));
    }
    
    if (!fs.existsSync(templateDir)) {
      await fs.promises.mkdir(templateDir, { recursive: true });
      console.log(chalk.green(`Created templates directory: ${templateDir}`));
    }
    
    return true;
  } catch (err) {
    console.error(chalk.red(`Failed to initialize context system: ${err.message}`));
    return false;
  }
};

/**
 * Create a context from template
 * @param {string} templateName - Name of the template to use
 * @param {Object} variables - Variables to substitute in the template
 * @param {Object} options - Additional options for context creation
 * @returns {Promise<Object>} The created context object
 */
const createContextFromTemplate = async (templateName, variables = {}, options = {}) => {
  try {
    // Initialize system if needed
    await initialize();
    
    // Load template
    const template = await templateParser.loadTemplate(templateName);
    
    // Process template with variables
    const content = templateParser.processTemplate(template.content, variables);
    
    // Create context object
    const context = {
      title: template.metadata.title || variables.title || templateName,
      description: template.metadata.description || variables.description || '',
      content,
      metadata: {
        ...template.metadata,
        template: templateName,
        created: new Date().toISOString(),
        ...options.metadata
      },
      source: `template:${templateName}`,
      language: template.extension === 'md' ? 'markdown' : template.extension
    };
    
    return context;
  } catch (err) {
    console.error(chalk.red(`Error creating context from template: ${err.message}`));
    return null;
  }
};

/**
 * Process context with given action
 * @param {Object} context - Context object
 * @param {string} action - Action to perform (copy, print, save)
 * @param {Object} options - Options for the action
 * @returns {Promise<boolean>} Success status
 */
const processContext = async (context, action = 'print', options = {}) => {
  if (!context) {
    console.error(chalk.red('No context provided'));
    return false;
  }
  
  try {
    switch (action) {
      case 'copy':
        const copyFormat = options.format || 'markdown';
        let formattedContext;
        
        if (copyFormat === 'markdown') {
          formattedContext = cliIntegration.formatContextMarkdown(context);
        } else {
          formattedContext = cliIntegration.formatContextPlain(context);
        }
        
        const success = cliIntegration.pushToClipboard(formattedContext);
        
        if (success) {
          console.log(chalk.green('Context copied to clipboard'));
          
          if (options.preview) {
            console.log(chalk.dim('Preview:'));
            console.log(chalk.dim('-'.repeat(60)));
            console.log(chalk.dim(formattedContext.substring(0, 200) + (formattedContext.length > 200 ? '...' : '')));
            console.log(chalk.dim('-'.repeat(60)));
          }
        } else {
          console.error(chalk.red('Failed to copy to clipboard'));
        }
        
        return success;
        
      case 'print':
        cliIntegration.printContext(context, options);
        return true;
        
      case 'save':
        if (!options.filename) {
          throw new Error('Filename required for save action');
        }
        
        const contextRoot = getContextRoot();
        const saveDir = path.join(contextRoot, 'saved');
        
        if (!fs.existsSync(saveDir)) {
          await fs.promises.mkdir(saveDir, { recursive: true });
        }
        
        const saveFormat = options.format || 'json';
        let fileContent;
        let filePath;
        
        if (saveFormat === 'json') {
          fileContent = JSON.stringify(context, null, 2);
          filePath = path.join(saveDir, `${options.filename}.json`);
        } else if (saveFormat === 'markdown') {
          fileContent = cliIntegration.formatContextMarkdown(context);
          filePath = path.join(saveDir, `${options.filename}.md`);
        } else if (saveFormat === 'txt') {
          fileContent = cliIntegration.formatContextPlain(context);
          filePath = path.join(saveDir, `${options.filename}.txt`);
        } else {
          throw new Error(`Unsupported format: ${saveFormat}`);
        }
        
        await fs.promises.writeFile(filePath, fileContent, 'utf8');
        console.log(chalk.green(`Context saved to: ${filePath}`));
        
        return true;
        
      default:
        throw new Error(`Unknown action: ${action}`);
    }
  } catch (err) {
    console.error(chalk.red(`Error processing context: ${err.message}`));
    return false;
  }
};

module.exports = {
  initialize,
  getContextRoot,
  createContextFromTemplate,
  processContext,
  // Re-export from submodules
  templates: templateParser,
  cli: cliIntegration
}; 