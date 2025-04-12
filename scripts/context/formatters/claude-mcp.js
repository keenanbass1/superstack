/**
 * Formats context modules for Anthropic's Multi-Context Protocol (MCP)
 * @param {Array} contextModules - Array of context module objects
 * @return {string} - MCP-formatted context string
 */
function formatForClaudeMCP(contextModules) {
    return contextModules.map(module => {
      // Extract metadata from module content
      const metadataMatch = module.content.match(/^##\s*Metadata\b[\s\S]*?Priority:\s*(.+?)[\s,]/m);
      const priorityLevel = metadataMatch ? metadataMatch[1].trim() : 'medium';
      
      // Extract domain if available
      const domainMatch = module.content.match(/^##\s*Metadata\b[\s\S]*?Domain:\s*(.+?)[\s,]/m);
      const domain = domainMatch ? domainMatch[1].trim() : '';
      
      // Create metadata attributes
      const metadataAttrs = [
        `name="${module.id}"`,
        `priority="${priorityLevel}"`,
      ];
      
      if (domain) {
        metadataAttrs.push(`domain="${domain}"`);
      }
      
      return `<context ${metadataAttrs.join(' ')}>
  ${module.content}
  </context>`;
    }).join('\n\n');
  }
  
  module.exports = { formatForClaudeMCP };