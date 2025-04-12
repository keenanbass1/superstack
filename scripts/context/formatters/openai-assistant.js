/**
 * OpenAI Assistant Context Formatter
 * 
 * This formatter prepares context modules for the OpenAI Assistants API.
 * It formats context modules for file-like upload or direct instruction format.
 */

/**
 * Format context modules for OpenAI Assistants API
 * 
 * @param {Array} modules - Array of context modules to format
 * @param {Object} options - Formatting options
 * @param {boolean} options.includeInactive - Whether to include inactive modules (default: false)
 * @param {string} options.defaultDomain - Default domain to filter by (optional)
 * @param {boolean} options.formatAsFiles - Whether to format for file upload (default: false)
 * @param {boolean} options.addMetadata - Whether to include module metadata (default: false)
 * @returns {Object|string} Formatted context for OpenAI Assistants API
 */
function formatForOpenAIAssistant(modules, options = {}) {
  // Set default options
  const {
    includeInactive = false,
    defaultDomain = null,
    formatAsFiles = false,
    addMetadata = false
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

  // If formatting as files, create an array of virtual files
  if (formatAsFiles) {
    return filteredModules.map(module => {
      // Create filename based on module properties
      const filename = `${module.domain}-${module.name.replace(/\s+/g, '_').toLowerCase()}.txt`;
      
      // Format the content
      let content = '';
      
      // Add metadata if requested
      if (addMetadata) {
        content += `# ${module.name}\n\n`;
        
        if (module.description) {
          content += `${module.description}\n\n`;
        }
        
        content += `Type: ${module.type}\n`;
        content += `Domain: ${module.domain}\n`;
        
        if (module.tags && module.tags.length > 0) {
          content += `Tags: ${module.tags.join(', ')}\n`;
        }
        
        content += '\n---\n\n';
      }
      
      // Add the main content
      content += module.content;
      
      // Return the virtual file object
      return {
        filename,
        content,
        purpose: "assistants"
      };
    });
  }
  
  // Otherwise, format as a single string for instructions
  let instructionsContent = '';
  
  // Add preface if there are modules
  if (filteredModules.length > 0) {
    instructionsContent += 'Use the following context to help answer user queries. Each section contains relevant information for different topics:\n\n';
  }

  // Format each module
  filteredModules.forEach((module, index) => {
    // Add section separator if not the first module
    if (index > 0) {
      instructionsContent += '\n\n---\n\n';
    }
    
    // Add section header with module name
    instructionsContent += `## ${module.name}\n\n`;
    
    // Add metadata if requested
    if (addMetadata) {
      if (module.description) {
        instructionsContent += `${module.description}\n\n`;
      }
      
      instructionsContent += `Type: ${module.type}\n`;
      instructionsContent += `Domain: ${module.domain}\n`;
      
      if (module.tags && module.tags.length > 0) {
        instructionsContent += `Tags: ${module.tags.join(', ')}\n`;
      }
      
      instructionsContent += '\n';
    }
    
    // Add the main content
    instructionsContent += module.content;
  });

  return instructionsContent;
}

module.exports = formatForOpenAIAssistant;