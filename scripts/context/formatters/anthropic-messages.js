/**
 * Anthropic Messages Context Formatter
 * 
 * This formatter prepares context modules for the Anthropic Messages API format,
 * creating a properly structured message with context in system role.
 */

/**
 * Format context modules for Anthropic Messages API
 * 
 * @param {Array} modules - Array of context modules to format
 * @param {Object} options - Formatting options
 * @param {boolean} options.includeInactive - Whether to include inactive modules (default: false)
 * @param {string} options.defaultDomain - Default domain to filter by (optional)
 * @param {boolean} options.addPreface - Whether to add a preface about the context (default: true)
 * @param {boolean} options.addMetadata - Whether to include module metadata (default: false)
 * @returns {Object} Anthropic messages object with properly formatted context
 */
function formatForAnthropicMessages(modules, options = {}) {
  // Set default options
  const {
    includeInactive = false,
    defaultDomain = null,
    addPreface = true,
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

  // Build the system content
  let systemContent = '';
  
  // Add preface if requested
  if (addPreface && filteredModules.length > 0) {
    systemContent += 'I\'m providing you with the following context to help with your response. Each section contains important information that may be relevant to my question.\n\n';
  }

  // Format each module
  filteredModules.forEach((module, index) => {
    // Add section separator if not the first module
    if (index > 0) {
      systemContent += '\n\n---\n\n';
    }
    
    // Add section header with module name
    systemContent += `## ${module.name}\n\n`;
    
    // Add metadata if requested
    if (addMetadata) {
      if (module.description) {
        systemContent += `${module.description}\n\n`;
      }
      
      systemContent += `Type: ${module.type}\n`;
      systemContent += `Domain: ${module.domain}\n`;
      
      if (module.tags && module.tags.length > 0) {
        systemContent += `Tags: ${module.tags.join(', ')}\n`;
      }
      
      systemContent += '\n';
    }
    
    // Add the main content
    systemContent += module.content;
  });

  // If no modules were included, return empty system message
  if (filteredModules.length === 0) {
    systemContent = '';
  }

  // Return the properly formatted Anthropic message object
  return {
    system: systemContent,
    messages: [] // Empty messages array, to be filled by the consumer
  };
}

module.exports = formatForAnthropicMessages;