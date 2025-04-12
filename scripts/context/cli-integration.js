/**
 * CLI Integration for AI Context System
 * 
 * This file demonstrates how to integrate the context management system
 * with the dev CLI tool.
 */

const { Command } = require('commander');
const contextCommands = require('./context-commands');

/**
 * Register context commands with the CLI
 * @param {Command} program The commander program instance
 */
function registerContextCommands(program) {
  const contextCmd = program
    .command('context')
    .description('Manage AI context modules');

  // List commands
  contextCmd
    .command('list')
    .description('List available context modules')
    .action(() => {
      contextCommands.listAvailableContexts();
    });

  contextCmd
    .command('list-active')
    .description('List active context modules')
    .action(() => {
      contextCommands.listActiveContexts();
    });

  contextCmd
    .command('list-groups')
    .description('List available context groups')
    .action(() => {
      contextCommands.listContextGroups();
    });

  // Add/remove context modules
  contextCmd
    .command('add <contextPath>')
    .description('Add a context module to the active context')
    .action((contextPath) => {
      contextCommands.addContext(contextPath);
    });

  contextCmd
    .command('remove <contextPath>')
    .description('Remove a context module from the active context')
    .action((contextPath) => {
      contextCommands.removeContext(contextPath);
    });
  
  contextCmd
    .command('clear')
    .description('Clear all active context modules')
    .action(() => {
      contextCommands.clearContext();
    });

  // Context group management
  contextCmd
    .command('create-group <groupName> [contextPaths...]')
    .description('Create a named context group')
    .action((groupName, contextPaths) => {
      contextCommands.createContextGroup(groupName, contextPaths);
    });
  
  contextCmd
    .command('add-group <groupName>')
    .description('Add a context group to the active context')
    .action((groupName) => {
      contextCommands.applyContextGroup(groupName);
    });

  // Context content
  contextCmd
    .command('show <contextPath>')
    .description('Show the content of a context module')
    .action((contextPath) => {
      const content = contextCommands.getContextContent(contextPath);
      if (content) {
        console.log(content);
      }
    });
  
  contextCmd
    .command('show-active')
    .description('Show the content of all active context modules')
    .action(() => {
      const content = contextCommands.getActiveContextContent();
      if (content) {
        console.log(content);
      }
    });

  // Create new context module
  contextCmd
    .command('create <contextPath>')
    .description('Create a new context module from template')
    .action((contextPath) => {
      contextCommands.createContextModule(contextPath);
    });

  // Integration commands
  
  // Push context to clipboard
  contextCmd
    .command('push')
    .description('Copy active context to clipboard for use with AI tools')
    .action(() => {
      const content = contextCommands.getActiveContextContent();
      if (content) {
        try {
          // Copy to clipboard - this is platform-specific and might need adjustment
          // This is just a placeholder - implement actual clipboard handling based on your environment
          console.log('Copied active context to clipboard (simulation)');
          console.log(`Content length: ${content.length} characters`);
        } catch (error) {
          console.error('Error copying to clipboard:', error.message);
        }
      }
    });
  
  // Context-aware AI prompt
  contextCmd
    .command('prompt <prompt>')
    .description('Send a prompt to AI with active context')
    .action((prompt) => {
      const content = contextCommands.getActiveContextContent();
      
      // This is a placeholder for actual AI integration
      console.log('Sending prompt to AI with context (simulation)');
      console.log(`Context length: ${content.length} characters`);
      console.log(`Prompt: ${prompt}`);
      
      // Implement actual AI integration based on your setup
    });

  return contextCmd;
}

module.exports = {
  registerContextCommands
};

// Example of how to use this in your main CLI file:
/*
const { program } = require('commander');
const { registerContextCommands } = require('./context/cli-integration');

// Register context commands
registerContextCommands(program);

program.parse(process.argv);
*/
