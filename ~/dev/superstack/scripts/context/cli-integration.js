/**
 * CLI Integration Module for AI Context System
 * Handles clipboard interactions and terminal output
 */

const os = require('os');
const chalk = require('chalk');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Load platform-specific clipboard modules
const loadClipboardModules = () => {
  const platform = os.platform();
  
  if (platform === 'darwin') {
    return {
      copy: (text) => {
        try {
          execSync('pbcopy', { input: text });
          return true;
        } catch (err) {
          console.error('Failed to copy to clipboard:', err.message);
          return false;
        }
      }
    };
  } else if (platform === 'linux') {
    try {
      // Check for xclip
      execSync('which xclip', { stdio: 'ignore' });
      return {
        copy: (text) => {
          try {
            execSync('xclip -selection clipboard', { input: text });
            return true;
          } catch (err) {
            console.error('Failed to copy to clipboard:', err.message);
            return false;
          }
        }
      };
    } catch (e) {
      try {
        // Try wl-copy for Wayland
        execSync('which wl-copy', { stdio: 'ignore' });
        return {
          copy: (text) => {
            try {
              execSync('wl-copy', { input: text });
              return true;
            } catch (err) {
              console.error('Failed to copy to clipboard:', err.message);
              return false;
            }
          }
        };
      } catch (e) {
        console.warn(chalk.yellow('Neither xclip nor wl-copy found. Clipboard functionality disabled.'));
        return { copy: () => false };
      }
    }
  } else if (platform === 'win32') {
    // For WSL environments
    const isWsl = (() => {
      try {
        return fs.readFileSync('/proc/version', 'utf8').toLowerCase().includes('microsoft');
      } catch (e) {
        return false;
      }
    })();
    
    if (isWsl) {
      return {
        copy: (text) => {
          try {
            // Use PowerShell through WSL for clipboard access
            const powershellCmd = `echo "${text.replace(/"/g, '\\"')}" | clip.exe`;
            execSync(powershellCmd, { shell: '/bin/bash' });
            return true;
          } catch (err) {
            console.error('Failed to copy to clipboard in WSL:', err.message);
            return false;
          }
        }
      };
    } else {
      try {
        // Standard Windows approach
        return {
          copy: (text) => {
            try {
              const cmd = `echo ${text.replace(/"/g, '\\"')} | clip`;
              execSync(cmd);
              return true;
            } catch (err) {
              console.error('Failed to copy to clipboard:', err.message);
              return false;
            }
          }
        };
      } catch (e) {
        console.warn(chalk.yellow('Clipboard functionality not available'));
        return { copy: () => false };
      }
    }
  }
  
  console.warn(chalk.yellow(`No clipboard support for platform: ${platform}`));
  return { copy: () => false };
};

// Initialize clipboard
const clipboard = loadClipboardModules();

/**
 * Push content to clipboard
 * @param {string} content - The content to push to clipboard
 * @returns {boolean} Success status
 */
const pushToClipboard = (content) => {
  return clipboard.copy(content);
};

/**
 * Format context for clipboard output (markdown format)
 * @param {Object} context - The context object
 * @returns {string} Formatted markdown string
 */
const formatContextMarkdown = (context) => {
  if (!context) return '';
  
  let output = `# ${context.title || 'Context'}\n\n`;
  
  if (context.description) {
    output += `${context.description}\n\n`;
  }
  
  if (context.content) {
    output += `\`\`\`${context.language || ''}\n${context.content}\n\`\`\`\n\n`;
  }
  
  if (context.metadata) {
    output += '## Metadata\n\n';
    Object.entries(context.metadata).forEach(([key, value]) => {
      output += `- **${key}**: ${value}\n`;
    });
  }
  
  return output;
};

/**
 * Format context for clipboard output (plain text)
 * @param {Object} context - The context object
 * @returns {string} Formatted plain text string
 */
const formatContextPlain = (context) => {
  if (!context) return '';
  
  let output = `${context.title || 'Context'}\n\n`;
  
  if (context.description) {
    output += `${context.description}\n\n`;
  }
  
  if (context.content) {
    output += `${context.content}\n\n`;
  }
  
  if (context.metadata) {
    output += 'Metadata:\n';
    Object.entries(context.metadata).forEach(([key, value]) => {
      output += `${key}: ${value}\n`;
    });
  }
  
  return output;
};

/**
 * Print context to terminal
 * @param {Object} context - The context object
 * @param {Object} options - Display options
 */
const printContext = (context, options = {}) => {
  if (!context) {
    console.log(chalk.yellow('No context available'));
    return;
  }
  
  const {
    showMetadata = true,
    colorize = true,
    verbose = false
  } = options;
  
  console.log('\n' + chalk.bold.blue('='.repeat(60)));
  console.log(chalk.bold.white(context.title || 'Context'));
  console.log(chalk.bold.blue('='.repeat(60)) + '\n');
  
  if (context.description) {
    console.log(chalk.italic.gray(context.description) + '\n');
  }
  
  if (context.content) {
    if (colorize && context.language) {
      // Basic syntax highlighting could be implemented here
      // For now, just output with language label
      console.log(chalk.magenta(`Language: ${context.language}`));
    }
    console.log(context.content + '\n');
  }
  
  if (showMetadata && context.metadata && Object.keys(context.metadata).length > 0) {
    console.log(chalk.bold.cyan('Metadata:'));
    Object.entries(context.metadata).forEach(([key, value]) => {
      console.log(chalk.cyan(`  ${key}:`), value);
    });
    console.log();
  }
  
  if (verbose && context.source) {
    console.log(chalk.gray(`Source: ${context.source}`));
  }
  
  console.log(chalk.bold.blue('='.repeat(60)) + '\n');
};

module.exports = {
  pushToClipboard,
  formatContextMarkdown,
  formatContextPlain,
  printContext
}; 