/**
 * Claude MCP Context Formatter
 * 
 * This formatter prepares context modules for Claude Anthropic API in a format
 * optimized for Multi-Context Processing (MCP).
 */

/**
 * Format context modules for Claude MCP
 * 
 * @param {Array} modules - Array of context modules to format
 * @param {Object} options - Formatting options
 * @param {boolean} options.includeInactive - Whether to include inactive modules (default: false)
 * @param {boolean} options.includeMetadata - Whether to include module metadata (default: true)
 * @param {string} options.defaultDomain - Default domain to filter by (optional)
 * @param {boolean} options.wrapWithXML - Whether to wrap content in XML tags (default: true)
 * @returns {string} Formatted context as string
 */
function formatForClaudeMCP(modules, options = {}) {
  // Set default options
  const {
    includeInactive = false,
    includeMetadata = true,
    defaultDomain = null,
    wrapWithXML = true
  } = options;

  // Filter modules based on options
  let filteredModules = [...modules];
  
  // Filter out inactive modules if not explicitly including them
  if (!includeInactive) {
    filteredModules = filteredModules.filter(module => module.active);
  }
  
  // Filter by domain if specified
  if (defaultDomain) {
    filteredModules = filteredModules.filter(module => module.domain === defaultDomain);
  }

  // If no modules remain after filtering, return empty string
  if (filteredModules.length === 0) {
    return '';
  }

  // Format each module
  const formattedModules = filteredModules.map(module => {
    let formattedModule = '';
    
    // Include metadata if requested
    if (includeMetadata) {
      formattedModule += `# ${module.name}\n\n`;
      
      if (module.description) {
        formattedModule += `${module.description}\n\n`;
      }
      
      formattedModule += `Type: ${module.type}\n`;
      formattedModule += `Domain: ${module.domain}\n`;
      
      if (module.tags && module.tags.length > 0) {
        formattedModule += `Tags: ${module.tags.join(', ')}\n`;
      }
      
      formattedModule += '\n';
    }
    
    // Add the main content
    formattedModule += `${module.content}\n`;
    
    return formattedModule;
  });

  // Join all formatted modules with clear separation
  let result = formattedModules.join('\n---\n\n');
  
  // Wrap with XML tags if requested
  if (wrapWithXML) {
    result = `<context>\n${result}\n</context>`;
  }
  
  return result;
}

module.exports = formatForClaudeMCP;