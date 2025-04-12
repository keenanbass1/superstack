/**
 * CLI Integration Module
 * 
 * Handles clipboard interactions and terminal output for the
 * AI Context System. Provides utilities for pushing formatted
 * context to clipboard and printing to terminal.
 */

const fs = require('fs');
const path = require('path');

// Handle chalk import (works with both CommonJS and ESM versions)
let chalk;
try {
  // Try CommonJS import first
  chalk = require('chalk');
} catch (e) {
  // If CommonJS fails, we'll simply use string templates without colors
  chalk = {
    red: (text) => text,
    green: (text) => text,
    blue: (text) => text,
    yellow: (text) => text,
    cyan: (text) => text,
    magenta: (text) => text,
    gray: (text) => text,
    white: (text) => text,
    bold: {
      green: (text) => text
    }
  };
  console.warn('Chalk module not available, terminal output will not be colored');
}

const { 
  formatForClaudeMCP,
  formatForAnthropicMessages,
  formatForOpenAIAssistant,
  formatForClaudeCompletion,
  getAvailableFormatters
} = require('./formatters');

/**
 * Load available clipboard module based on OS
 * @returns {Object|null} Clipboard module or null if not available
 */
function loadClipboardModule() {
  let clipboardModule = null;
  
  try {
    // Try to load clipboard module based on platform
    if (process.platform === 'darwin') {
      // macOS - use pbcopy
      const { execSync } = require('child_process');
      clipboardModule = {
        write: (text) => {
          try {
            execSync('pbcopy', { input: text });
            return true;
          } catch (error) {
            console.error('Failed to copy to clipboard:', error.message);
            return false;
          }
        }
      };
    } else if (process.platform === 'win32') {
      // Windows - use clipboardy or powershell
      try {
        const clipboardy = require('clipboardy');
        clipboardModule = {
          write: (text) => {
            try {
              clipboardy.writeSync(text);
              return true;
            } catch (error) {
              console.error('Failed to copy to clipboard:', error.message);
              return false;
            }
          }
        };
      } catch (e) {
        // Fallback to PowerShell
        const { execSync } = require('child_process');
        clipboardModule = {
          write: (text) => {
            try {
              const tempFile = path.join(require('os').tmpdir(), 'clipboard-content.txt');
              fs.writeFileSync(tempFile, text);
              execSync(`powershell -command "Get-Content '${tempFile}' | Set-Clipboard"`);
              fs.unlinkSync(tempFile);
              return true;
            } catch (error) {
              console.error('Failed to copy to clipboard:', error.message);
              return false;
            }
          }
        };
      }
    } else if (process.platform === 'linux') {
      // Linux - try xclip, xsel, or wl-copy
      const { execSync } = require('child_process');
      
      // Check for wl-clipboard (Wayland)
      let hasWlCopy = false;
      try {
        execSync('which wl-copy', { stdio: 'ignore' });
        hasWlCopy = true;
      } catch (e) {
        // wl-copy not available
      }
      
      // Check for xclip (X11)
      let hasXclip = false;
      try {
        execSync('which xclip', { stdio: 'ignore' });
        hasXclip = true;
      } catch (e) {
        // xclip not available
      }
      
      // Check for xsel (X11 alternative)
      let hasXsel = false;
      try {
        execSync('which xsel', { stdio: 'ignore' });
        hasXsel = true;
      } catch (e) {
        // xsel not available
      }
      
      // Set up the clipboard module based on available tool
      if (hasWlCopy) {
        clipboardModule = {
          write: (text) => {
            try {
              execSync('wl-copy', { input: text });
              return true;
            } catch (error) {
              console.error('Failed to copy to clipboard:', error.message);
              return false;
            }
          }
        };
      } else if (hasXclip) {
        clipboardModule = {
          write: (text) => {
            try {
              execSync('xclip -selection clipboard', { input: text });
              return true;
            } catch (error) {
              console.error('Failed to copy to clipboard:', error.message);
              return false;
            }
          }
        };
      } else if (hasXsel) {
        clipboardModule = {
          write: (text) => {
            try {
              execSync('xsel --clipboard --input', { input: text });
              return true;
            } catch (error) {
              console.error('Failed to copy to clipboard:', error.message);
              return false;
            }
          }
        };
      }
    }
  } catch (error) {
    console.error('Error loading clipboard module:', error.message);
  }
  
  return clipboardModule;
}

/**
 * Push content to clipboard
 * @param {string} content - Content to push to clipboard
 * @returns {boolean} Success status
 */
function pushToClipboard(content) {
  const clipboard = loadClipboardModule();
  
  if (!clipboard) {
    console.error(chalk.red('No clipboard module available for this platform'));
    return false;
  }
  
  return clipboard.write(content);
}

/**
 * Format context for Claude Desktop and push to clipboard
 * @param {Array} contextModules - Array of context modules to format
 * @param {Object} options - Formatting options
 * @returns {boolean} Success status
 */
function pushToClaudeDesktop(contextModules, options = {}) {
  const formattedContext = formatForClaudeMCP(contextModules, options);
  return pushToClipboard(formattedContext);
}

/**
 * Format context for Anthropic Messages API and push to clipboard
 * @param {Array} contextModules - Array of context modules to format
 * @param {Object} options - Formatting options
 * @returns {boolean} Success status
 */
function pushAnthropicMessages(contextModules, options = {}) {
  const formattedContext = formatForAnthropicMessages(contextModules, options);
  return pushToClipboard(formattedContext);
}

/**
 * Format context for OpenAI Assistant API and push to clipboard
 * @param {Array} contextModules - Array of context modules to format
 * @param {Object} options - Formatting options
 * @returns {boolean} Success status
 */
function pushOpenAIAssistant(contextModules, options = {}) {
  const formattedContext = formatForOpenAIAssistant(contextModules, options);
  return pushToClipboard(formattedContext);
}

/**
 * Format context for Claude Completion API and push to clipboard
 * @param {Array} contextModules - Array of context modules to format
 * @param {Object} options - Formatting options
 * @returns {boolean} Success status
 */
function pushClaudeCompletion(contextModules, options = {}) {
  const formattedContext = formatForClaudeCompletion(contextModules, options);
  return pushToClipboard(formattedContext);
}

/**
 * Push context to any supported AI model using the appropriate formatter
 * @param {Array} contextModules - Array of context modules to format
 * @param {string} targetModel - Target model: 'claude-mcp', 'anthropic-messages', 'openai-assistant', 'claude-completion'
 * @param {Object} options - Formatting options specific to the formatter
 * @returns {boolean} Success status
 * @throws {Error} If the target model is not supported
 */
function pushToModel(contextModules, targetModel, options = {}) {
  const formatters = getAvailableFormatters();
  
  // Check if we have a direct match for the model name
  if (formatters[targetModel]) {
    switch (targetModel) {
      case 'claude-mcp':
        return pushToClaudeDesktop(contextModules, options);
      case 'anthropic-messages':
        return pushAnthropicMessages(contextModules, options);
      case 'openai-assistant':
        return pushOpenAIAssistant(contextModules, options);
      case 'claude-completion':
        return pushClaudeCompletion(contextModules, options);
    }
  }
  
  // Check if we can find a formatter with matching targetModel
  const matchingFormatters = Object.entries(formatters)
    .filter(([key, info]) => info.targetModel === targetModel.toLowerCase());
  
  if (matchingFormatters.length > 0) {
    // Use the first matching formatter
    const [formatterKey] = matchingFormatters[0];
    return pushToModel(contextModules, formatterKey, options);
  }
  
  // No matching formatter found
  throw new Error(`No formatter found for target model: ${targetModel}`);
}

/**
 * Format context for clipboard output in markdown
 * @param {Array} contextModules - Array of context modules to format
 * @param {Object} options - Formatting options
 * @returns {string} Formatted markdown
 */
function formatContextForClipboardMarkdown(contextModules, options = {}) {
  const {
    includeHeaders = true,
    includeDomain = true,
    includeType = true,
    includeTags = true,
    separator = '---',
    headingLevel = 2
  } = options;
  
  const headingPrefix = '#'.repeat(headingLevel) + ' ';
  
  return contextModules.map((module, index) => {
    let output = '';
    
    // Add separator between modules (except for first one)
    if (index > 0 && separator) {
      output += `${separator}\n\n`;
    }
    
    // Add module header
    if (includeHeaders && module.name) {
      output += `${headingPrefix}${module.name}\n\n`;
    }
    
    // Add metadata if requested
    const metadataParts = [];
    
    if (includeDomain && module.domain) {
      metadataParts.push(`**Domain:** ${module.domain}`);
    }
    
    if (includeType && module.type) {
      metadataParts.push(`**Type:** ${module.type}`);
    }
    
    if (includeTags && module.tags && module.tags.length > 0) {
      metadataParts.push(`**Tags:** ${module.tags.join(', ')}`);
    }
    
    if (metadataParts.length > 0) {
      output += metadataParts.join(' • ') + '\n\n';
    }
    
    // Add content
    output += module.content;
    
    return output;
  }).join('\n\n');
}

/**
 * Format context for clipboard output in plain text
 * @param {Array} contextModules - Array of context modules to format
 * @param {Object} options - Formatting options
 * @returns {string} Formatted plain text
 */
function formatContextForClipboardPlainText(contextModules, options = {}) {
  const {
    includeHeaders = true,
    includeDomain = true,
    includeType = true,
    includeTags = true,
    separator = '---'
  } = options;
  
  return contextModules.map((module, index) => {
    let output = '';
    
    // Add separator between modules (except for first one)
    if (index > 0 && separator) {
      output += `${separator}\n\n`;
    }
    
    // Add module header
    if (includeHeaders && module.name) {
      output += `== ${module.name} ==\n\n`;
    }
    
    // Add metadata if requested
    const metadataParts = [];
    
    if (includeDomain && module.domain) {
      metadataParts.push(`Domain: ${module.domain}`);
    }
    
    if (includeType && module.type) {
      metadataParts.push(`Type: ${module.type}`);
    }
    
    if (includeTags && module.tags && module.tags.length > 0) {
      metadataParts.push(`Tags: ${module.tags.join(', ')}`);
    }
    
    if (metadataParts.length > 0) {
      output += metadataParts.join(' | ') + '\n\n';
    }
    
    // Add content
    output += module.content;
    
    return output;
  }).join('\n\n');
}

/**
 * Print context to terminal
 * @param {Array} contextModules - Array of context modules to print
 * @param {Object} options - Printing options
 */
function printContextToTerminal(contextModules, options = {}) {
  const {
    colorize = true,
    showModuleCount = true,
    showInactive = false,
    compactMode = false
  } = options;
  
  // Filter inactive modules if needed
  const filteredModules = showInactive 
    ? contextModules 
    : contextModules.filter(m => m.active !== false);
  
  // Show module count if requested
  if (showModuleCount) {
    const totalModules = contextModules.length;
    const activeModules = contextModules.filter(m => m.active !== false).length;
    const inactiveModules = totalModules - activeModules;
    
    const countText = `${activeModules} active module${activeModules !== 1 ? 's' : ''}` + 
      (inactiveModules > 0 ? ` (${inactiveModules} inactive)` : '');
      
    console.log(colorize 
      ? chalk.cyan(`\n== Context: ${countText} ==\n`) 
      : `\n== Context: ${countText} ==\n`);
  }
  
  // Print each module
  filteredModules.forEach((module, index) => {
    // Print separator between modules
    if (index > 0 && !compactMode) {
      console.log(colorize ? chalk.gray('---') : '---');
      console.log();
    }
    
    // Print module name
    const nameDisplay = module.name || 'Unnamed Module';
    console.log(colorize 
      ? chalk.bold.green(nameDisplay) 
      : nameDisplay);
    
    // Print module metadata
    if (!compactMode) {
      const metadataItems = [];
      
      if (module.domain) {
        metadataItems.push(`Domain: ${module.domain}`);
      }
      
      if (module.type) {
        metadataItems.push(`Type: ${module.type}`);
      }
      
      if (module.tags && module.tags.length > 0) {
        metadataItems.push(`Tags: ${module.tags.join(', ')}`);
      }
      
      if (metadataItems.length > 0) {
        const metadataText = metadataItems.join(' • ');
        console.log(colorize 
          ? chalk.yellow(metadataText) 
          : metadataText);
        console.log();
      }
    }
    
    // Print module content
    console.log(module.content);
    
    // Add spacing after module
    if (!compactMode || index < filteredModules.length - 1) {
      console.log();
    }
  });
}

/**
 * List all available formatters with their descriptions and options
 * @param {boolean} colorize - Whether to colorize output
 * @returns {void}
 */
function listFormatters(colorize = true) {
  const formatters = getAvailableFormatters();
  const formatterNames = Object.keys(formatters);
  
  console.log(colorize 
    ? chalk.cyan('\n== Available Context Formatters ==\n')
    : '\n== Available Context Formatters ==\n');
  
  formatterNames.forEach((key) => {
    const formatter = formatters[key];
    
    // Print formatter name and description
    console.log(colorize 
      ? chalk.bold.green(formatter.name) + ' (' + chalk.yellow(key) + ')'
      : formatter.name + ' (' + key + ')');
    
    console.log(colorize 
      ? chalk.white(formatter.description)
      : formatter.description);
    
    console.log(colorize 
      ? chalk.blue(`Target model: ${formatter.targetModel}`)
      : `Target model: ${formatter.targetModel}`);
    
    // Print options
    if (formatter.options && formatter.options.length > 0) {
      console.log(colorize ? chalk.magenta('Options:') : 'Options:');
      
      formatter.options.forEach((option) => {
        const defaultValue = option.default !== null 
          ? `${option.default}` 
          : 'null';
          
        console.log(colorize
          ? `  - ${chalk.yellow(option.name)} (${option.type}): ${chalk.gray('default: ' + defaultValue)}`
          : `  - ${option.name} (${option.type}): default: ${defaultValue}`);
      });
    }
    
    console.log(); // Add spacing between formatters
  });
}

module.exports = { 
  pushToClipboard,
  pushToClaudeDesktop, 
  pushAnthropicMessages,
  pushOpenAIAssistant,
  pushClaudeCompletion,
  pushToModel,
  formatContextForClipboardMarkdown,
  formatContextForClipboardPlainText,
  printContextToTerminal,
  listFormatters,
  getAvailableFormatters
};
