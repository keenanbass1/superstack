/**
 * AI Context Management System
 * 
 * This module provides CLI commands for managing and using AI context modules
 * in the superstack development system.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// Configuration
const CONFIG = {
  // Base directory for context modules
  contextDir: path.join(process.env.DEV_ROOT || path.join(os.homedir(), 'dev'), 
                        'superstack', 'docs', 'ai-context'),
  
  // Path to active context session file
  activeContextFile: path.join(os.homedir(), '.config', 'superstack', 'active-context.json'),
  
  // Path to context groups configuration
  contextGroupsFile: path.join(os.homedir(), '.config', 'superstack', 'context-groups.json'),
};

/**
 * Initialize the context management system
 */
function initContextSystem() {
  // Ensure config directory exists
  const configDir = path.dirname(CONFIG.activeContextFile);
  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
  }
  
  // Initialize active context file if it doesn't exist
  if (!fs.existsSync(CONFIG.activeContextFile)) {
    fs.writeFileSync(CONFIG.activeContextFile, JSON.stringify({
      active: [],
      lastUpdated: new Date().toISOString()
    }));
  }
  
  // Initialize context groups file if it doesn't exist
  if (!fs.existsSync(CONFIG.contextGroupsFile)) {
    fs.writeFileSync(CONFIG.contextGroupsFile, JSON.stringify({
      groups: {}
    }));
  }
}

/**
 * Get the list of active context modules
 * @returns {Array} The list of active context modules
 */
function getActiveContexts() {
  try {
    const data = fs.readFileSync(CONFIG.activeContextFile, 'utf8');
    const contextData = JSON.parse(data);
    return contextData.active || [];
  } catch (error) {
    console.error('Error reading active contexts:', error.message);
    return [];
  }
}

/**
 * Save the list of active context modules
 * @param {Array} contexts The list of active context modules
 */
function saveActiveContexts(contexts) {
  try {
    const contextData = {
      active: contexts,
      lastUpdated: new Date().toISOString()
    };
    fs.writeFileSync(CONFIG.activeContextFile, JSON.stringify(contextData, null, 2));
  } catch (error) {
    console.error('Error saving active contexts:', error.message);
  }
}

/**
 * Add a context module to the active context list
 * @param {string} contextPath The path to the context module, relative to the context directory
 */
function addContext(contextPath) {
  // Check if the context module exists
  const fullPath = getFullModulePath(contextPath);
  if (!fs.existsSync(fullPath)) {
    console.error(`Context module not found: ${contextPath}`);
    return false;
  }
  
  // Add to active contexts if not already present
  const activeContexts = getActiveContexts();
  if (!activeContexts.includes(contextPath)) {
    activeContexts.push(contextPath);
    saveActiveContexts(activeContexts);
    console.log(`Added context: ${contextPath}`);
    return true;
  } else {
    console.log(`Context already active: ${contextPath}`);
    return true;
  }
}

/**
 * Remove a context module from the active context list
 * @param {string} contextPath The path to the context module, relative to the context directory
 */
function removeContext(contextPath) {
  const activeContexts = getActiveContexts();
  const index = activeContexts.indexOf(contextPath);
  
  if (index !== -1) {
    activeContexts.splice(index, 1);
    saveActiveContexts(activeContexts);
    console.log(`Removed context: ${contextPath}`);
    return true;
  } else {
    console.log(`Context not active: ${contextPath}`);
    return false;
  }
}

/**
 * Clear all active context modules
 */
function clearContext() {
  saveActiveContexts([]);
  console.log('Cleared all active context modules');
  return true;
}

/**
 * List all available context modules
 */
function listAvailableContexts() {
  const contexts = findAllContextModules();
  
  if (contexts.length === 0) {
    console.log('No context modules found');
    return [];
  }
  
  // Group by domain
  const groupedContexts = {};
  contexts.forEach(ctx => {
    const parts = ctx.split('/');
    const domain = parts[0] || 'other';
    
    if (!groupedContexts[domain]) {
      groupedContexts[domain] = [];
    }
    
    groupedContexts[domain].push(ctx);
  });
  
  // Print grouped contexts
  console.log('Available context modules:');
  for (const [domain, modules] of Object.entries(groupedContexts)) {
    console.log(`\n${domain.toUpperCase()}`);
    modules.forEach(module => {
      console.log(`  ${module}`);
    });
  }
  
  return contexts;
}

/**
 * List currently active context modules
 */
function listActiveContexts() {
  const activeContexts = getActiveContexts();
  
  if (activeContexts.length === 0) {
    console.log('No active context modules');
    return [];
  }
  
  console.log('Active context modules:');
  activeContexts.forEach(ctx => {
    console.log(`  ${ctx}`);
  });
  
  return activeContexts;
}

/**
 * Create a named context group
 * @param {string} groupName Name of the context group
 * @param {Array} contexts List of context modules to include
 */
function createContextGroup(groupName, contexts) {
  try {
    const data = fs.readFileSync(CONFIG.contextGroupsFile, 'utf8');
    const groupsData = JSON.parse(data);
    
    // Validate contexts
    const validContexts = [];
    const invalidContexts = [];
    
    for (const ctx of contexts) {
      const fullPath = getFullModulePath(ctx);
      if (fs.existsSync(fullPath)) {
        validContexts.push(ctx);
      } else {
        invalidContexts.push(ctx);
      }
    }
    
    if (invalidContexts.length > 0) {
      console.warn('The following contexts were not found and will be skipped:');
      invalidContexts.forEach(ctx => console.warn(`  ${ctx}`));
    }
    
    if (validContexts.length === 0) {
      console.error('No valid contexts provided for group');
      return false;
    }
    
    // Add or update group
    groupsData.groups[groupName] = validContexts;
    fs.writeFileSync(CONFIG.contextGroupsFile, JSON.stringify(groupsData, null, 2));
    
    console.log(`Created context group: ${groupName} with ${validContexts.length} modules`);
    return true;
  } catch (error) {
    console.error('Error creating context group:', error.message);
    return false;
  }
}

/**
 * Apply a context group to the active contexts
 * @param {string} groupName Name of the context group to apply
 */
function applyContextGroup(groupName) {
  try {
    const data = fs.readFileSync(CONFIG.contextGroupsFile, 'utf8');
    const groupsData = JSON.parse(data);
    
    if (!groupsData.groups[groupName]) {
      console.error(`Context group not found: ${groupName}`);
      return false;
    }
    
    const contexts = groupsData.groups[groupName];
    
    // Check if all contexts still exist
    const validContexts = [];
    const invalidContexts = [];
    
    for (const ctx of contexts) {
      const fullPath = getFullModulePath(ctx);
      if (fs.existsSync(fullPath)) {
        validContexts.push(ctx);
      } else {
        invalidContexts.push(ctx);
      }
    }
    
    if (invalidContexts.length > 0) {
      console.warn('The following contexts in the group were not found and will be skipped:');
      invalidContexts.forEach(ctx => console.warn(`  ${ctx}`));
    }
    
    if (validContexts.length === 0) {
      console.error('No valid contexts found in group');
      return false;
    }
    
    // Add valid contexts to active contexts
    const activeContexts = getActiveContexts();
    let added = 0;
    
    for (const ctx of validContexts) {
      if (!activeContexts.includes(ctx)) {
        activeContexts.push(ctx);
        added++;
      }
    }
    
    saveActiveContexts(activeContexts);
    
    console.log(`Applied context group: ${groupName} (${added} new modules added)`);
    return true;
  } catch (error) {
    console.error('Error applying context group:', error.message);
    return false;
  }
}

/**
 * List all available context groups
 */
function listContextGroups() {
  try {
    const data = fs.readFileSync(CONFIG.contextGroupsFile, 'utf8');
    const groupsData = JSON.parse(data);
    
    const groups = Object.keys(groupsData.groups);
    
    if (groups.length === 0) {
      console.log('No context groups defined');
      return [];
    }
    
    console.log('Available context groups:');
    for (const group of groups) {
      const contexts = groupsData.groups[group];
      console.log(`  ${group} (${contexts.length} modules)`);
    }
    
    return groups;
  } catch (error) {
    console.error('Error listing context groups:', error.message);
    return [];
  }
}

/**
 * Get the full path to a context module
 * @param {string} contextPath The path to the context module, relative to the context directory
 * @returns {string} The full path to the context module
 */
function getFullModulePath(contextPath) {
  // If it already has an extension, use it as is
  if (path.extname(contextPath) === '.md') {
    return path.join(CONFIG.contextDir, contextPath);
  }
  
  // Otherwise, add .md extension
  return path.join(CONFIG.contextDir, `${contextPath}.md`);
}

/**
 * Find all available context modules
 * @returns {Array} List of available context modules
 */
function findAllContextModules() {
  const results = [];
  
  function scanDirectory(dir, basePath = '') {
    try {
      const files = fs.readdirSync(dir);
      
      for (const file of files) {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        
        // Skip template and schema directories
        if (stat.isDirectory()) {
          if (file !== 'templates' && file !== 'schemas') {
            const newBasePath = basePath ? path.join(basePath, file) : file;
            scanDirectory(filePath, newBasePath);
          }
        } else if (stat.isFile() && path.extname(file) === '.md' && file !== 'README.md' && file !== 'CONTRIBUTING.md') {
          // Extract path relative to context directory
          const relativePath = basePath ? path.join(basePath, path.parse(file).name) : path.parse(file).name;
          results.push(relativePath);
        }
      }
    } catch (error) {
      console.error(`Error scanning directory ${dir}:`, error.message);
    }
  }
  
  scanDirectory(CONFIG.contextDir);
  return results;
}

/**
 * Get the content of a context module
 * @param {string} contextPath The path to the context module, relative to the context directory
 * @returns {string} The content of the context module
 */
function getContextContent(contextPath) {
  const fullPath = getFullModulePath(contextPath);
  
  if (!fs.existsSync(fullPath)) {
    console.error(`Context module not found: ${contextPath}`);
    return null;
  }
  
  try {
    return fs.readFileSync(fullPath, 'utf8');
  } catch (error) {
    console.error(`Error reading context module ${contextPath}:`, error.message);
    return null;
  }
}

/**
 * Get concatenated content of active context modules
 * @returns {string} The concatenated content
 */
function getActiveContextContent() {
  const activeContexts = getActiveContexts();
  
  if (activeContexts.length === 0) {
    console.warn('No active context modules');
    return '';
  }
  
  const contentParts = [];
  
  for (const ctx of activeContexts) {
    const content = getContextContent(ctx);
    if (content) {
      contentParts.push(`# CONTEXT: ${ctx}`);
      contentParts.push(content);
      contentParts.push('\n---\n');
    }
  }
  
  return contentParts.join('\n');
}

/**
 * Create a new context module from a template
 * @param {string} contextPath The path to the new context module, relative to the context directory
 */
function createContextModule(contextPath) {
  const fullPath = getFullModulePath(contextPath);
  
  // Check if module already exists
  if (fs.existsSync(fullPath)) {
    console.error(`Context module already exists: ${contextPath}`);
    return false;
  }
  
  // Ensure directory exists
  const dir = path.dirname(fullPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  // Copy template to new file
  try {
    const templatePath = path.join(CONFIG.contextDir, 'templates', 'context-module-template.md');
    const templateContent = fs.readFileSync(templatePath, 'utf8');
    fs.writeFileSync(fullPath, templateContent);
    
    console.log(`Created new context module: ${contextPath}`);
    console.log(`Edit it at: ${fullPath}`);
    return true;
  } catch (error) {
    console.error('Error creating context module:', error.message);
    return false;
  }
}

// Initialize on module load
initContextSystem();

module.exports = {
  // Context management
  addContext,
  removeContext,
  clearContext,
  listAvailableContexts,
  listActiveContexts,
  
  // Context group management
  createContextGroup,
  applyContextGroup,
  listContextGroups,
  
  // Content access
  getContextContent,
  getActiveContextContent,
  
  // Module creation
  createContextModule,
};
