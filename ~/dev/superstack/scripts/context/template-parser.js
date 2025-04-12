/**
 * Template Parser Module for AI Context System
 * Handles template loading, variable substitution, and processing
 */

const fs = require('fs');
const path = require('path');
const handlebars = require('handlebars');
const chalk = require('chalk');

// Get templates directory
const getTemplatesDir = () => {
  return path.join(process.env.HOME, 'dev', 'superstack', 'insights', 'templates');
};

/**
 * List available templates
 * @returns {Promise<Array>} Array of template objects with name and path
 */
const listTemplates = async () => {
  const templatesDir = getTemplatesDir();
  
  try {
    // Check if directory exists
    if (!fs.existsSync(templatesDir)) {
      console.warn(chalk.yellow(`Templates directory not found: ${templatesDir}`));
      return [];
    }
    
    const files = await fs.promises.readdir(templatesDir);
    const templates = [];
    
    for (const file of files) {
      if (file.endsWith('.hbs') || file.endsWith('.md') || file.endsWith('.txt')) {
        const fullPath = path.join(templatesDir, file);
        const stats = await fs.promises.stat(fullPath);
        
        if (stats.isFile()) {
          templates.push({
            name: file.replace(/\.(hbs|md|txt)$/, ''),
            path: fullPath,
            extension: path.extname(file).substring(1)
          });
        }
      }
    }
    
    return templates;
  } catch (err) {
    console.error(chalk.red(`Error listing templates: ${err.message}`));
    return [];
  }
};

/**
 * Load template content
 * @param {string} templateName - Name of the template (without extension)
 * @returns {Promise<Object>} Template object with content and metadata
 */
const loadTemplate = async (templateName) => {
  const templatesDir = getTemplatesDir();
  
  // Try different possible extensions
  const possibleExtensions = ['hbs', 'md', 'txt'];
  let templatePath = null;
  let extension = '';
  
  for (const ext of possibleExtensions) {
    const testPath = path.join(templatesDir, `${templateName}.${ext}`);
    if (fs.existsSync(testPath)) {
      templatePath = testPath;
      extension = ext;
      break;
    }
  }
  
  if (!templatePath) {
    throw new Error(`Template '${templateName}' not found in ${templatesDir}`);
  }
  
  try {
    const content = await fs.promises.readFile(templatePath, 'utf8');
    
    // Parse metadata (if any) - assuming frontmatter format
    const metadataMatch = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
    
    if (metadataMatch) {
      const metadataStr = metadataMatch[1];
      const actualContent = metadataMatch[2];
      
      // Simple YAML-like parsing
      const metadata = {};
      const metadataLines = metadataStr.split('\n');
      
      metadataLines.forEach(line => {
        const match = line.match(/^([^:]+):\s*(.*)$/);
        if (match) {
          const [, key, value] = match;
          metadata[key.trim()] = value.trim();
        }
      });
      
      return {
        name: templateName,
        content: actualContent.trim(),
        metadata,
        extension
      };
    }
    
    // No metadata found
    return {
      name: templateName,
      content: content.trim(),
      metadata: {},
      extension
    };
  } catch (err) {
    throw new Error(`Error loading template '${templateName}': ${err.message}`);
  }
};

/**
 * Process template with variables
 * @param {string} templateContent - Template content with handlebars syntax
 * @param {Object} variables - Object containing variables for substitution
 * @returns {string} Processed template content
 */
const processTemplate = (templateContent, variables = {}) => {
  try {
    // Register helpers
    handlebars.registerHelper('uppercase', (str) => str.toUpperCase());
    handlebars.registerHelper('lowercase', (str) => str.toLowerCase());
    handlebars.registerHelper('titlecase', (str) => {
      return str.replace(/\w\S*/g, txt => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase());
    });
    handlebars.registerHelper('date', (format = 'YYYY-MM-DD') => {
      const now = new Date();
      // Very basic format handling
      let formatted = format
        .replace('YYYY', now.getFullYear())
        .replace('MM', String(now.getMonth() + 1).padStart(2, '0'))
        .replace('DD', String(now.getDate()).padStart(2, '0'))
        .replace('HH', String(now.getHours()).padStart(2, '0'))
        .replace('mm', String(now.getMinutes()).padStart(2, '0'))
        .replace('ss', String(now.getSeconds()).padStart(2, '0'));
      return formatted;
    });
    
    // Compile and process template
    const template = handlebars.compile(templateContent);
    return template(variables);
  } catch (err) {
    console.error(chalk.red(`Error processing template: ${err.message}`));
    return templateContent; // Return original on error
  }
};

/**
 * Create a new template
 * @param {string} name - Template name
 * @param {string} content - Template content
 * @param {Object} metadata - Template metadata
 * @returns {Promise<boolean>} Success status
 */
const createTemplate = async (name, content, metadata = {}) => {
  const templatesDir = getTemplatesDir();
  
  // Create directory if it doesn't exist
  if (!fs.existsSync(templatesDir)) {
    await fs.promises.mkdir(templatesDir, { recursive: true });
  }
  
  try {
    // Add metadata as frontmatter if provided
    let finalContent = content;
    
    if (Object.keys(metadata).length > 0) {
      let metadataContent = '---\n';
      for (const [key, value] of Object.entries(metadata)) {
        metadataContent += `${key}: ${value}\n`;
      }
      metadataContent += '---\n\n';
      finalContent = metadataContent + content;
    }
    
    // Default to .hbs extension
    const templatePath = path.join(templatesDir, `${name}.hbs`);
    await fs.promises.writeFile(templatePath, finalContent);
    
    return true;
  } catch (err) {
    console.error(chalk.red(`Error creating template '${name}': ${err.message}`));
    return false;
  }
};

module.exports = {
  listTemplates,
  loadTemplate,
  processTemplate,
  createTemplate
}; 