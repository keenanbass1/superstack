const fs = require('fs');
const path = require('path');
const os = require('os');

/**
 * Get the path to the superstack config directory
 * @returns {string} Path to the config directory
 */
function getConfigDir() {
  const homedir = os.homedir();
  return path.join(homedir, '.config', 'superstack');
}

/**
 * Get the path to the context modules directory
 * @returns {string} Path to the context modules directory
 */
function getContextModulesDir() {
  return path.join(process.cwd(), 'docs', 'ai-context');
}

/**
 * Get the list of active context modules
 * @returns {Array} List of active context module paths
 */
function getActiveContexts() {
  const configDir = getConfigDir();
  const activeContextPath = path.join(configDir, 'active-context.json');
  
  // Create config directory if it doesn't exist
  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
  }
  
  // Create empty active context file if it doesn't exist
  if (!fs.existsSync(activeContextPath)) {
    fs.writeFileSync(activeContextPath, JSON.stringify([], null, 2));
    return [];
  }
  
  try {
    return JSON.parse(fs.readFileSync(activeContextPath, 'utf8'));
  } catch (error) {
    console.error('Error reading active contexts:', error);
    return [];
  }
}

/**
 * Load context module content
 * @param {string} modulePath - Path to the context module
 * @returns {Object|null} Module object with id and content, or null if not found
 */
function loadContextModule(modulePath) {
  const contextDir = getContextModulesDir();
  const fullPath = path.join(contextDir, `${modulePath}.md`);
  
  if (!fs.existsSync(fullPath)) {
    console.warn(`Context module not found: ${modulePath}`);
    return null;
  }
  
  return {
    id: path.basename(modulePath),
    path: modulePath,
    content: fs.readFileSync(fullPath, 'utf8')
  };
}

/**
 * Load all active context modules
 * @returns {Array} Array of loaded context module objects
 */
function loadActiveContextModules() {
  const activeContexts = getActiveContexts();
  
  return activeContexts
    .map(loadContextModule)
    .filter(Boolean); // Remove null entries
}

module.exports = {
  getConfigDir,
  getContextModulesDir,
  getActiveContexts,
  loadContextModule,
  loadActiveContextModules
};