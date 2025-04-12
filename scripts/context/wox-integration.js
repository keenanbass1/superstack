/**
 * Wox Integration Module
 * 
 * This module provides the core functionality needed to integrate the
 * context management system with the Wox launcher.
 * 
 * Note: This is not a complete Wox plugin - it provides the underlying
 * JavaScript functionality that would be called by the Python Wox plugin wrapper.
 */

const contextCommands = require('./context-commands');
const contextIntegration = require('./context-integration');
const moduleRecommender = require('./utils/module-recommender');
const clipboardManager = require('./utils/clipboard-manager');
const path = require('path');
const fs = require('fs');

// Root directory for templates
const TEMPLATE_DIR = process.env.PROMPT_DIR || 
                     path.join(process.env.DEV_ROOT || path.join(require('os').homedir(), 'dev'), 
                     'superstack', 'templates', 'prompts');

/**
 * Get default suggestions for the Wox UI
 * @returns {Array} Array of suggestion objects
 */
function getDefaultSuggestions() {
  return [
    {
      Title: "Add Context Module",
      SubTitle: "Add a module to active context",
      IcoPath: "Images\\add.png",
      JsonRPCAction: {
        method: "showContextModules",
        parameters: []
      }
    },
    {
      Title: "Apply Context Group",
      SubTitle: "Apply a pre-defined context group",
      IcoPath: "Images\\group.png",
      JsonRPCAction: {
        method: "showContextGroups",
        parameters: []
      }
    },
    {
      Title: "Show Active Context",
      SubTitle: "Display currently active context modules",
      IcoPath: "Images\\list.png",
      JsonRPCAction: {
        method: "showActiveContext",
        parameters: []
      }
    },
    {
      Title: "Clear Context",
      SubTitle: "Remove all active context modules",
      IcoPath: "Images\\clear.png",
      JsonRPCAction: {
        method: "clearAllContext",
        parameters: []
      }
    },
    {
      Title: "Copy Context to Clipboard",
      SubTitle: "Copy active context content to clipboard",
      IcoPath: "Images\\copy.png",
      JsonRPCAction: {
        method: "copyContextToClipboard",
        parameters: []
      }
    },
    {
      Title: "Load Prompt Template",
      SubTitle: "Choose a prompt template to use",
      IcoPath: "Images\\prompt.png",
      JsonRPCAction: {
        method: "showPromptTemplates",
        parameters: []
      }
    },
    {
      Title: "Analyze Clipboard",
      SubTitle: "Analyze clipboard and recommend context modules",
      IcoPath: "Images\\analyze.png",
      JsonRPCAction: {
        method: "analyzeClipboard",
        parameters: []
      }
    }
  ];
}

/**
 * Get all available context modules for the Wox UI
 * @returns {Array} Array of context module objects
 */
function getAllContextModules() {
  try {
    // Use the existing context command to get modules
    const modules = contextCommands.listAvailableContexts();
    
    // Convert to Wox format
    return modules.map(module => ({
      Title: module,
      SubTitle: `Add "${module}" to active context`,
      IcoPath: "Images\\module.png",
      JsonRPCAction: {
        method: "addContextModule",
        parameters: [module]
      }
    }));
  } catch (error) {
    console.error('Error getting context modules:', error.message);
    return [{
      Title: "Error Getting Modules",
      SubTitle: error.message,
      IcoPath: "Images\\error.png"
    }];
  }
}

/**
 * Get all available context groups for the Wox UI
 * @returns {Array} Array of context group objects
 */
function getAllContextGroups() {
  try {
    // Get groups using the context command
    const groups = contextCommands.listContextGroups();
    
    // Convert to Wox format
    return groups.map(group => ({
      Title: group,
      SubTitle: `Apply "${group}" context group`,
      IcoPath: "Images\\group.png",
      JsonRPCAction: {
        method: "applyContextGroup",
        parameters: [group]
      }
    }));
  } catch (error) {
    console.error('Error getting context groups:', error.message);
    return [{
      Title: "Error Getting Groups",
      SubTitle: error.message,
      IcoPath: "Images\\error.png"
    }];
  }
}

/**
 * Get active context modules for the Wox UI
 * @returns {Array} Array of active context module objects
 */
function getActiveContextModules() {
  try {
    const modules = contextCommands.getActiveContexts();
    
    if (modules.length === 0) {
      return [{
        Title: "No Active Context Modules",
        SubTitle: "Add modules using 'context add <module>'",
        IcoPath: "Images\\info.png"
      }];
    }
    
    // Convert to Wox format
    return modules.map(module => ({
      Title: module,
      SubTitle: `Remove "${module}" from active context`,
      IcoPath: "Images\\active.png",
      JsonRPCAction: {
        method: "removeContextModule",
        parameters: [module]
      }
    }));
  } catch (error) {
    console.error('Error getting active context modules:', error.message);
    return [{
      Title: "Error Getting Active Modules",
      SubTitle: error.message,
      IcoPath: "Images\\error.png"
    }];
  }
}

/**
 * Get all prompt templates for the Wox UI
 * @returns {Array} Array of prompt template objects
 */
function getAllPromptTemplates() {
  try {
    // Scan template directory for markdown files
    const templates = [];
    
    // Function to scan a directory recursively
    function scanDirectory(dir, baseDir = '') {
      const files = fs.readdirSync(dir);
      
      for (const file of files) {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);
        
        if (stat.isDirectory()) {
          // Scan subdirectory
          scanDirectory(fullPath, path.join(baseDir, file));
        } else if (stat.isFile() && file.endsWith('.md')) {
          // Get relative path to use as ID
          const relativePath = path.join(baseDir, file);
          
          // Read first line to use as title
          let title = file.replace('.md', '');
          try {
            const content = fs.readFileSync(fullPath, 'utf8');
            const firstLine = content.split('\n')[0];
            if (firstLine.startsWith('# ')) {
              title = firstLine.substring(2);
            }
          } catch (e) {
            // Ignore error, use filename as title
          }
          
          templates.push({
            path: relativePath,
            title
          });
        }
      }
    }
    
    // Scan template directory
    if (fs.existsSync(TEMPLATE_DIR)) {
      scanDirectory(TEMPLATE_DIR);
    }
    
    // Convert to Wox format
    return templates.map(template => ({
      Title: template.title,
      SubTitle: template.path,
      IcoPath: "Images\\template.png",
      JsonRPCAction: {
        method: "loadPromptTemplate",
        parameters: [template.path]
      }
    }));
  } catch (error) {
    console.error('Error getting prompt templates:', error.message);
    return [{
      Title: "Error Getting Templates",
      SubTitle: error.message,
      IcoPath: "Images\\error.png"
    }];
  }
}

/**
 * Add a context module to active context
 * @param {string} modulePath Path to the context module
 * @returns {Array} Array of result objects
 */
function addContextModule(modulePath) {
  try {
    const success = contextCommands.addContext(modulePath);
    
    return [{
      Title: success ? "Module Added Successfully" : "Failed to Add Module",
      SubTitle: `${modulePath} ${success ? 'added to' : 'could not be added to'} active context`,
      IcoPath: success ? "Images\\success.png" : "Images\\error.png"
    }];
  } catch (error) {
    return [{
      Title: "Error Adding Module",
      SubTitle: error.message,
      IcoPath: "Images\\error.png"
    }];
  }
}

/**
 * Remove a context module from active context
 * @param {string} modulePath Path to the context module
 * @returns {Array} Array of result objects
 */
function removeContextModule(modulePath) {
  try {
    const success = contextCommands.removeContext(modulePath);
    
    return [{
      Title: success ? "Module Removed Successfully" : "Failed to Remove Module",
      SubTitle: `${modulePath} ${success ? 'removed from' : 'could not be removed from'} active context`,
      IcoPath: success ? "Images\\success.png" : "Images\\error.png"
    }];
  } catch (error) {
    return [{
      Title: "Error Removing Module",
      SubTitle: error.message,
      IcoPath: "Images\\error.png"
    }];
  }
}

/**
 * Apply a context group
 * @param {string} groupName Name of the context group
 * @returns {Array} Array of result objects
 */
function applyContextGroup(groupName) {
  try {
    const success = contextCommands.applyContextGroup(groupName);
    
    return [{
      Title: success ? "Group Applied Successfully" : "Failed to Apply Group",
      SubTitle: `${groupName} ${success ? 'applied to' : 'could not be applied to'} active context`,
      IcoPath: success ? "Images\\success.png" : "Images\\error.png"
    }];
  } catch (error) {
    return [{
      Title: "Error Applying Group",
      SubTitle: error.message,
      IcoPath: "Images\\error.png"
    }];
  }
}

/**
 * Clear all active context modules
 * @returns {Array} Array of result objects
 */
function clearAllContext() {
  try {
    contextCommands.clearContext();
    
    return [{
      Title: "Context Cleared",
      SubTitle: "All active context modules have been removed",
      IcoPath: "Images\\success.png"
    }];
  } catch (error) {
    return [{
      Title: "Error Clearing Context",
      SubTitle: error.message,
      IcoPath: "Images\\error.png"
    }];
  }
}

/**
 * Copy active context to clipboard
 * @returns {Array} Array of result objects
 */
function copyContextToClipboard() {
  try {
    const content = contextCommands.getActiveContextContent();
    
    if (!content) {
      return [{
        Title: "No Active Context",
        SubTitle: "There are no active context modules to copy",
        IcoPath: "Images\\info.png"
      }];
    }
    
    const result = clipboardManager.copyWithMetrics(content);
    
    if (result.success) {
      return [{
        Title: "Context Copied to Clipboard",
        SubTitle: `Copied ${result.characters} characters (${result.lines} lines, ~${result.tokenEstimate} tokens)`,
        IcoPath: "Images\\success.png"
      }];
    } else {
      return [{
        Title: "Failed to Copy Context",
        SubTitle: "Error copying content to clipboard",
        IcoPath: "Images\\error.png"
      }];
    }
  } catch (error) {
    return [{
      Title: "Error Copying Context",
      SubTitle: error.message,
      IcoPath: "Images\\error.png"
    }];
  }
}

/**
 * Load and process a prompt template
 * @param {string} templatePath Path to the prompt template
 * @returns {Array} Array of result objects
 */
function loadPromptTemplate(templatePath) {
  try {
    const templateFullPath = path.join(TEMPLATE_DIR, templatePath);
    
    if (!fs.existsSync(templateFullPath)) {
      return [{
        Title: "Template Not Found",
        SubTitle: `Could not find template at ${templatePath}`,
        IcoPath: "Images\\error.png"
      }];
    }
    
    const template = fs.readFileSync(templateFullPath, 'utf8');
    const processed = contextIntegration.processTemplate(template);
    
    const result = clipboardManager.copyWithMetrics(processed);
    
    if (result.success) {
      return [{
        Title: "Template Processed and Copied",
        SubTitle: `Template ${path.basename(templatePath)} with context (~${result.tokenEstimate} tokens)`,
        IcoPath: "Images\\success.png"
      }];
    } else {
      return [{
        Title: "Failed to Copy Template",
        SubTitle: "Error copying processed template to clipboard",
        IcoPath: "Images\\error.png"
      }];
    }
  } catch (error) {
    return [{
      Title: "Error Processing Template",
      SubTitle: error.message,
      IcoPath: "Images\\error.png"
    }];
  }
}

/**
 * Analyze clipboard content and recommend context modules
 * @returns {Array} Array of result objects
 */
function analyzeClipboard() {
  try {
    const content = clipboardManager.readFromClipboard();
    
    if (!content) {
      return [{
        Title: "No Content in Clipboard",
        SubTitle: "Clipboard is empty or could not be read",
        IcoPath: "Images\\error.png"
      }];
    }
    
    const recommendations = moduleRecommender.getRecommendations(content, {
      maxModules: 5,
      maxGroups: 2
    });
    
    // Create results with two sections:
    // 1. Information about recommendations
    // 2. Actions to add recommended modules/groups
    
    const results = [];
    
    // Add info about recommendations
    results.push({
      Title: "Content Analysis Complete",
      SubTitle: `Found ${recommendations.modules.length} relevant modules and ${recommendations.groups.length} groups`,
      IcoPath: "Images\\info.png"
    });
    
    // Add module recommendations with actions
    for (const module of recommendations.modules) {
      results.push({
        Title: `Add Module: ${module}`,
        SubTitle: `Add "${module}" to active context`,
        IcoPath: "Images\\module.png",
        JsonRPCAction: {
          method: "addContextModule",
          parameters: [module]
        }
      });
    }
    
    // Add group recommendations with actions
    for (const group of recommendations.groups) {
      results.push({
        Title: `Apply Group: ${group}`,
        SubTitle: `Apply "${group}" context group`,
        IcoPath: "Images\\group.png",
        JsonRPCAction: {
          method: "applyContextGroup",
          parameters: [group]
        }
      });
    }
    
    // If no recommendations, add a message
    if (results.length === 1) {
      results.push({
        Title: "No Relevant Modules Found",
        SubTitle: "The clipboard content didn't match any known context domains",
        IcoPath: "Images\\info.png"
      });
    }
    
    return results;
  } catch (error) {
    return [{
      Title: "Error Analyzing Clipboard",
      SubTitle: error.message,
      IcoPath: "Images\\error.png"
    }];
  }
}

/**
 * Process a query and return matching results
 * @param {string} query The query string
 * @returns {Array} Array of results
 */
function processQuery(query) {
  if (!query || query.trim() === '') {
    return getDefaultSuggestions();
  }
  
  const lowerQuery = query.toLowerCase().trim();
  
  // Command: add <module>
  if (lowerQuery.startsWith('add ')) {
    const moduleQuery = lowerQuery.substring(4).trim();
    const modules = contextCommands.listAvailableContexts();
    
    // Filter modules that match the query
    const matchingModules = modules.filter(module => 
      module.toLowerCase().includes(moduleQuery)
    );
    
    if (matchingModules.length === 0) {
      return [{
        Title: "No Matching Modules",
        SubTitle: `No modules found matching "${moduleQuery}"`,
        IcoPath: "Images\\info.png"
      }];
    }
    
    // Return matching modules
    return matchingModules.map(module => ({
      Title: `Add: ${module}`,
      SubTitle: `Add "${module}" to active context`,
      IcoPath: "Images\\module.png",
      JsonRPCAction: {
        method: "addContextModule",
        parameters: [module]
      }
    }));
  }
  
  // Command: group <name>
  if (lowerQuery.startsWith('group ')) {
    const groupQuery = lowerQuery.substring(6).trim();
    
    try {
      const groups = contextCommands.listContextGroups();
      
      // Filter groups that match the query
      const matchingGroups = groups.filter(group => 
        group.toLowerCase().includes(groupQuery)
      );
      
      if (matchingGroups.length === 0) {
        return [{
          Title: "No Matching Groups",
          SubTitle: `No groups found matching "${groupQuery}"`,
          IcoPath: "Images\\info.png"
        }];
      }
      
      // Return matching groups
      return matchingGroups.map(group => ({
        Title: `Apply: ${group}`,
        SubTitle: `Apply "${group}" context group`,
        IcoPath: "Images\\group.png",
        JsonRPCAction: {
          method: "applyContextGroup",
          parameters: [group]
        }
      }));
    } catch (error) {
      return [{
        Title: "Error Getting Groups",
        SubTitle: error.message,
        IcoPath: "Images\\error.png"
      }];
    }
  }
  
  // Command: prompt <name>
  if (lowerQuery.startsWith('prompt ')) {
    const promptQuery = lowerQuery.substring(7).trim();
    
    try {
      // Get all templates
      const templates = [];
      
      // Function to scan a directory recursively
      function scanDirectory(dir, baseDir = '') {
        if (!fs.existsSync(dir)) {
          return;
        }
        
        const files = fs.readdirSync(dir);
        
        for (const file of files) {
          const fullPath = path.join(dir, file);
          const stat = fs.statSync(fullPath);
          
          if (stat.isDirectory()) {
            // Scan subdirectory
            scanDirectory(fullPath, path.join(baseDir, file));
          } else if (stat.isFile() && file.endsWith('.md')) {
            // Get relative path to use as ID
            const relativePath = path.join(baseDir, file);
            
            // Read first line to use as title
            let title = file.replace('.md', '');
            try {
              const content = fs.readFileSync(fullPath, 'utf8');
              const firstLine = content.split('\n')[0];
              if (firstLine.startsWith('# ')) {
                title = firstLine.substring(2);
              }
            } catch (e) {
              // Ignore error, use filename as title
            }
            
            templates.push({
              path: relativePath,
              title,
              fullPath
            });
          }
        }
      }
      
      // Scan template directory
      scanDirectory(TEMPLATE_DIR);
      
      // Filter templates that match the query
      const matchingTemplates = templates.filter(template => 
        template.title.toLowerCase().includes(promptQuery) ||
        template.path.toLowerCase().includes(promptQuery)
      );
      
      if (matchingTemplates.length === 0) {
        return [{
          Title: "No Matching Templates",
          SubTitle: `No templates found matching "${promptQuery}"`,
          IcoPath: "Images\\info.png"
        }];
      }
      
      // Return matching templates
      return matchingTemplates.map(template => ({
        Title: template.title,
        SubTitle: template.path,
        IcoPath: "Images\\template.png",
        JsonRPCAction: {
          method: "loadPromptTemplate",
          parameters: [template.path]
        }
      }));
    } catch (error) {
      return [{
        Title: "Error Finding Templates",
        SubTitle: error.message,
        IcoPath: "Images\\error.png"
      }];
    }
  }
  
  // Command: remove <module>
  if (lowerQuery.startsWith('remove ')) {
    const moduleQuery = lowerQuery.substring(7).trim();
    const activeModules = contextCommands.getActiveContexts();
    
    // Filter modules that match the query
    const matchingModules = activeModules.filter(module => 
      module.toLowerCase().includes(moduleQuery)
    );
    
    if (matchingModules.length === 0) {
      return [{
        Title: "No Matching Active Modules",
        SubTitle: `No active modules found matching "${moduleQuery}"`,
        IcoPath: "Images\\info.png"
      }];
    }
    
    // Return matching modules
    return matchingModules.map(module => ({
      Title: `Remove: ${module}`,
      SubTitle: `Remove "${module}" from active context`,
      IcoPath: "Images\\remove.png",
      JsonRPCAction: {
        method: "removeContextModule",
        parameters: [module]
      }
    }));
  }
  
  // Default: search across all commands and actions
  const defaultResults = [];
  
  // Add pre-defined actions that match the query
  const actions = [
    {
      keywords: ['add', 'module'],
      title: "Add Context Module",
      subtitle: "Add a module to active context",
      icon: "Images\\add.png",
      method: "showContextModules",
      parameters: []
    },
    {
      keywords: ['apply', 'group'],
      title: "Apply Context Group",
      subtitle: "Apply a pre-defined context group",
      icon: "Images\\group.png",
      method: "showContextGroups",
      parameters: []
    },
    {
      keywords: ['show', 'active', 'list'],
      title: "Show Active Context",
      subtitle: "Display currently active context modules",
      icon: "Images\\list.png",
      method: "showActiveContext",
      parameters: []
    },
    {
      keywords: ['clear', 'reset', 'remove all'],
      title: "Clear Context",
      subtitle: "Remove all active context modules",
      icon: "Images\\clear.png",
      method: "clearAllContext",
      parameters: []
    },
    {
      keywords: ['copy', 'clipboard'],
      title: "Copy Context to Clipboard",
      subtitle: "Copy active context content to clipboard",
      icon: "Images\\copy.png",
      method: "copyContextToClipboard",
      parameters: []
    },
    {
      keywords: ['prompt', 'template'],
      title: "Load Prompt Template",
      subtitle: "Choose a prompt template to use",
      icon: "Images\\prompt.png",
      method: "showPromptTemplates",
      parameters: []
    },
    {
      keywords: ['analyze', 'recommend'],
      title: "Analyze Clipboard",
      subtitle: "Analyze clipboard and recommend context modules",
      icon: "Images\\analyze.png",
      method: "analyzeClipboard",
      parameters: []
    }
  ];
  
  // Filter actions that match the query
  for (const action of actions) {
    if (action.keywords.some(keyword => keyword.includes(lowerQuery)) ||
        action.title.toLowerCase().includes(lowerQuery) ||
        action.subtitle.toLowerCase().includes(lowerQuery)) {
      defaultResults.push({
        Title: action.title,
        SubTitle: action.subtitle,
        IcoPath: action.icon,
        JsonRPCAction: {
          method: action.method,
          parameters: action.parameters
        }
      });
    }
  }
  
  // If we have matching actions, return them
  if (defaultResults.length > 0) {
    return defaultResults;
  }
  
  // No matches found, return default suggestions
  return getDefaultSuggestions();
}

module.exports = {
  getDefaultSuggestions,
  getAllContextModules,
  getAllContextGroups,
  getActiveContextModules,
  getAllPromptTemplates,
  addContextModule,
  removeContextModule,
  applyContextGroup,
  clearAllContext,
  copyContextToClipboard,
  loadPromptTemplate,
  analyzeClipboard,
  processQuery
};
