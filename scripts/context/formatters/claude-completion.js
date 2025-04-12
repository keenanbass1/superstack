/**
 * Claude Completion Context Formatter
 * 
 * This formatter prepares context modules for the Anthropic Claude Completion API.
 * It structures content according to Claude's message format for optimal results.
 */

/**
 * Format context modules for Claude Completion API
 * 
 * @param {Array} modules - Array of context modules to format
 * @param {Object} options - Formatting options
 * @param {boolean} options.includeInactive - Whether to include inactive modules (default: false)
 * @param {string} options.defaultDomain - Default domain to filter by (optional)
 * @param {boolean} options.addMetadata - Whether to include module metadata (default: false)
 * @param {string} options.preface - Optional preface to add before the formatted content
 * @param {string} options.systemPrompt - Optional system prompt override
 * @returns {string} Formatted context for Claude Completion API
 */
function formatForClaudeCompletion(modules, options = {}) {
  // Set default options
  const {
    includeInactive = false,
    defaultDomain = null,
    addMetadata = false,
    preface = null,
    systemPrompt = null
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

  // Default system prompt if not provided
  const defaultSystemPrompt = "You are Claude, an AI assistant by Anthropic. You are helpful, harmless, and honest.";
  
  // Build the formatted content
  let formattedContent = '';
  
  // Add system prompt
  formattedContent += `\n\nHuman: <system>\n${systemPrompt || defaultSystemPrompt}\n\n`;
  
  // Add preface if provided or generate a default one if there are modules
  if (preface) {
    formattedContent += `${preface}\n\n`;
  } else if (filteredModules.length > 0) {
    formattedContent += 'Please use the following context to help answer my questions. Each section contains relevant information for different topics:\n\n';
  }

  // Format each module
  filteredModules.forEach((module, index) => {
    // Add section separator if not the first module
    if (index > 0) {
      formattedContent += '\n\n---\n\n';
    }
    
    // Add section header with module name
    formattedContent += `## ${module.name}\n\n`;
    
    // Add metadata if requested
    if (addMetadata) {
      if (module.description) {
        formattedContent += `${module.description}\n\n`;
      }
      
      formattedContent += `Type: ${module.type}\n`;
      formattedContent += `Domain: ${module.domain}\n`;
      
      if (module.tags && module.tags.length > 0) {
        formattedContent += `Tags: ${module.tags.join(', ')}\n`;
      }
      
      formattedContent += '\n';
    }
    
    // Add the main content
    formattedContent += module.content;
  });
  
  // Close the system tag
  formattedContent += "\n</system>\n\n";
  
  // Add the actual user query placeholder
  formattedContent += "My query is: \n\nAssistant: ";
  
  return formattedContent;
}

module.exports = formatForClaudeCompletion;