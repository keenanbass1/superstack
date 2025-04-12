/**
 * CLI Command Module for AI Context System
 * Provides command-line interface for context management
 */

const { Command } = require('commander');
const chalk = require('chalk');
const inquirer = require('inquirer');
const contextSystem = require('./index');

// Create context command
const createContextCommand = new Command('create')
  .description('Create a new context from a template')
  .argument('[template]', 'Template name to use')
  .option('-v, --vars <variables>', 'JSON string of variables for template')
  .option('-i, --interactive', 'Use interactive mode to fill template variables')
  .option('-c, --copy', 'Copy the result to clipboard')
  .option('-s, --save <filename>', 'Save the result to a file')
  .option('-f, --format <format>', 'Output format (markdown, plain, json)', 'markdown')
  .option('-p, --print', 'Print the result to the console')
  .action(async (template, options) => {
    try {
      // Initialize the context system
      await contextSystem.initialize();
      
      // If no template provided, list available templates
      if (!template) {
        const templates = await contextSystem.templates.listTemplates();
        
        if (templates.length === 0) {
          console.log(chalk.yellow('No templates found'));
          console.log(chalk.gray(`Templates should be placed in: ${contextSystem.getContextRoot()}/templates`));
          return;
        }
        
        console.log(chalk.bold('Available templates:'));
        templates.forEach(t => {
          console.log(`  ${chalk.cyan(t.name)} (${t.extension})`);
        });
        
        if (options.interactive) {
          const { selectedTemplate } = await inquirer.prompt([
            {
              type: 'list',
              name: 'selectedTemplate',
              message: 'Select a template:',
              choices: templates.map(t => t.name)
            }
          ]);
          template = selectedTemplate;
        } else {
          return;
        }
      }
      
      // Parse variables
      let variables = {};
      
      if (options.vars) {
        try {
          variables = JSON.parse(options.vars);
        } catch (err) {
          console.error(chalk.red(`Error parsing variables: ${err.message}`));
          return;
        }
      }
      
      // Interactive mode
      if (options.interactive) {
        try {
          // Load template to get metadata
          const templateObj = await contextSystem.templates.loadTemplate(template);
          const requiredVars = templateObj.content.match(/{{([^{}]+)}}/g) || [];
          
          // Extract variable names without handlebars and helpers
          const varNames = new Set();
          requiredVars.forEach(match => {
            const varName = match
              .replace(/{{/g, '')
              .replace(/}}/g, '')
              .trim()
              .split(' ')[0] // Remove helper parameters
              .replace(/^#/, '') // Remove block helper prefix
              .replace(/^\//, ''); // Remove block helper end
              
            // Skip helpers and conditionals
            if (!varName.includes('if') && 
                !varName.includes('each') && 
                !varName.includes('date') && 
                !varName.includes('uppercase') && 
                !varName.includes('lowercase') && 
                !varName.includes('titlecase')) {
              varNames.add(varName);
            }
          });
          
          // Ask for each variable
          const questions = Array.from(varNames).map(varName => {
            return {
              type: 'input',
              name: varName,
              message: `Enter value for ${varName}:`,
              default: variables[varName] || ''
            };
          });
          
          if (questions.length > 0) {
            const answers = await inquirer.prompt(questions);
            variables = { ...variables, ...answers };
          }
        } catch (err) {
          console.error(chalk.red(`Error in interactive mode: ${err.message}`));
          return;
        }
      }
      
      // Create context
      const context = await contextSystem.createContextFromTemplate(template, variables);
      
      if (!context) {
        console.error(chalk.red(`Failed to create context from template: ${template}`));
        return;
      }
      
      // Process the context based on options
      if (options.copy) {
        await contextSystem.processContext(context, 'copy', { 
          format: options.format,
          preview: true
        });
      }
      
      if (options.save) {
        await contextSystem.processContext(context, 'save', {
          filename: options.save,
          format: options.format
        });
      }
      
      if (options.print || (!options.copy && !options.save)) {
        await contextSystem.processContext(context, 'print');
      }
      
    } catch (err) {
      console.error(chalk.red(`Error: ${err.message}`));
    }
  });

// List templates command
const listTemplatesCommand = new Command('list')
  .description('List available templates')
  .action(async () => {
    try {
      await contextSystem.initialize();
      
      const templates = await contextSystem.templates.listTemplates();
      
      if (templates.length === 0) {
        console.log(chalk.yellow('No templates found'));
        console.log(chalk.gray(`Templates should be placed in: ${contextSystem.getContextRoot()}/templates`));
        return;
      }
      
      console.log(chalk.bold('Available templates:'));
      templates.forEach(t => {
        console.log(`  ${chalk.cyan(t.name)} (${t.extension})`);
      });
    } catch (err) {
      console.error(chalk.red(`Error: ${err.message}`));
    }
  });

// Create new template command
const newTemplateCommand = new Command('new-template')
  .description('Create a new template')
  .argument('<name>', 'Template name')
  .option('-i, --interactive', 'Create template interactively')
  .option('-c, --content <content>', 'Template content')
  .action(async (name, options) => {
    try {
      await contextSystem.initialize();
      
      let content = options.content || '';
      let metadata = {};
      
      if (options.interactive) {
        const answers = await inquirer.prompt([
          {
            type: 'input',
            name: 'title',
            message: 'Template title:',
            default: name
          },
          {
            type: 'input',
            name: 'description',
            message: 'Template description:'
          },
          {
            type: 'editor',
            name: 'content',
            message: 'Enter the template content (press i to start editing):',
            default: content
          }
        ]);
        
        content = answers.content;
        metadata.title = answers.title;
        metadata.description = answers.description;
      }
      
      const success = await contextSystem.templates.createTemplate(name, content, metadata);
      
      if (success) {
        console.log(chalk.green(`Template '${name}' created successfully`));
      } else {
        console.error(chalk.red(`Failed to create template '${name}'`));
      }
    } catch (err) {
      console.error(chalk.red(`Error: ${err.message}`));
    }
  });

// Initialize the main command
const contextCommand = new Command('context')
  .description('AI Context Management System')
  .addCommand(createContextCommand)
  .addCommand(listTemplatesCommand)
  .addCommand(newTemplateCommand);

module.exports = contextCommand; 