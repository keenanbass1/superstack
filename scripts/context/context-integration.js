/**
 * Context Integration Module
 * 
 * This module provides integration utilities for the context management system,
 * allowing easier incorporation of context modules into various workflows.
 */

const fs = require('fs');
const path = require('path');
const contextCommands = require('./context-commands');

// Token counting and management
const AVG_CHARS_PER_TOKEN = 4; // Approximation

/**
 * Count tokens in a text string (approximate)
 * @param {string} text The text to count tokens for
 * @returns {number} Approximate token count
 */
function countTokens(text) {
  if (!text) return 0;
  // Simple approximation: ~4 characters per token on average
  return Math.ceil(text.length / AVG_CHARS_PER_TOKEN);
}

/**
 * Get context content that fits within token limits
 * @param {number} maxTokens Maximum tokens to include (default: 6000)
 * @returns {Object} Object containing content and metadata
 */
function getLimitedContextContent(maxTokens = 6000) {
  const activeContexts = contextCommands.getActiveContexts();
  
  if (activeContexts.length === 0) {
    return { 
      content: '',
      includedModules: [],
      excludedModules: [],
      totalTokens: 0,
      truncated: false
    };
  }
  
  const chunks = [];
  const includedModules = [];
  const excludedModules = [];
  let totalTokens = 0;
  let truncated = false;
  
  // Header tokens (estimated)
  const headerTokens = countTokens('# CONTEXT INFORMATION\n\nThe following context modules are included to provide relevant information:\n\n');
  totalTokens += headerTokens;
  
  for (const ctx of activeContexts) {
    const content = contextCommands.getContextContent(ctx);
    if (!content) {
      excludedModules.push({ path: ctx, reason: 'Content not available' });
      continue;
    }
    
    const contextHeader = `## ${ctx}\n\n`;
    const contextFooter = '\n\n---\n\n';
    const fullChunk = contextHeader + content + contextFooter;
    const chunkTokens = countTokens(fullChunk);
    
    if (totalTokens + chunkTokens <= maxTokens) {
      chunks.push(fullChunk);
      includedModules.push({ path: ctx, tokens: chunkTokens });
      totalTokens += chunkTokens;
    } else {
      excludedModules.push({ path: ctx, reason: 'Token limit exceeded' });
      truncated = true;
    }
  }
  
  const content = chunks.length > 0 
    ? '# CONTEXT INFORMATION\n\nThe following context modules are included to provide relevant information:\n\n' + chunks.join('')
    : '';
  
  return {
    content,
    includedModules,
    excludedModules,
    totalTokens,
    truncated
  };
}

/**
 * Process a template string, replacing variables and injecting context
 * @param {string} template The template string with placeholders
 * @param {Object} variables Variables to replace in the template
 * @param {Object} options Additional options
 * @returns {string} The processed template
 */
function processTemplate(template, variables = {}, options = {}) {
  const { maxTokens = 6000, includeContext = true } = options;
  let result = template;
  
  // Replace standard variables
  for (const [key, value] of Object.entries(variables)) {
    const placeholder = `{{${key}}}`;
    result = result.replace(new RegExp(placeholder, 'g'), value || '');
  }
  
  // Replace context variable with active context if requested
  if (includeContext && result.includes('{{CONTEXT}}')) {
    const contextData = getLimitedContextContent(maxTokens);
    
    if (contextData.truncated) {
      console.warn(`Context was truncated to fit token limit (${maxTokens})`);
      console.warn(`Included ${contextData.includedModules.length} modules, excluded ${contextData.excludedModules.length} modules`);
    }
    
    result = result.replace(/{{CONTEXT}}/g, contextData.content);
  }
  
  return result;
}

/**
 * Load a prompt template from file
 * @param {string} templatePath Path to the prompt template file
 * @returns {string} The template content or null if not found
 */
function loadPromptTemplate(templatePath) {
  try {
    // Search in multiple possible locations
    const possiblePaths = [
      templatePath, // Use as-is if absolute
      path.join(process.cwd(), templatePath), // Relative to current dir
      path.join(process.env.DEV_ROOT || path.join(require('os').homedir(), 'dev'), 
                'superstack', 'templates', 'prompts', templatePath) // Dev root
    ];
    
    // Try with and without .md extension
    for (const basePath of possiblePaths) {
      const paths = [
        basePath,
        basePath.endsWith('.md') ? basePath : `${basePath}.md`
      ];
      
      for (const p of paths) {
        if (fs.existsSync(p)) {
          return fs.readFileSync(p, 'utf8');
        }
      }
    }
    
    console.error(`Prompt template not found: ${templatePath}`);
    return null;
  } catch (error) {
    console.error(`Error loading prompt template: ${error.message}`);
    return null;
  }
}

/**
 * Create a context summary for debugging and inspection
 * @returns {Object} Object containing context system info
 */
function getContextSummary() {
  const activeContexts = contextCommands.getActiveContexts();
  const contextDetails = [];
  let totalTokens = 0;
  
  for (const ctx of activeContexts) {
    const content = contextCommands.getContextContent(ctx);
    if (!content) continue;
    
    const tokens = countTokens(content);
    totalTokens += tokens;
    
    contextDetails.push({
      path: ctx,
      tokens,
      lines: content.split('\n').length,
      characters: content.length
    });
  }
  
  return {
    activeModules: activeContexts.length,
    totalTokens,
    tokenEstimate: {
      claude: totalTokens < 100000 ? 'Within limits' : 'May exceed context window',
      gpt4: totalTokens < 8000 ? 'Within limits' : 'May exceed context window'
    },
    modules: contextDetails
  };
}

/**
 * Recommend context modules based on content analysis
 * @param {string} content The content to analyze for relevant context modules
 * @param {number} maxRecommendations Maximum number of recommendations to return
 * @returns {Array} List of recommended context modules
 */
function recommendContextModules(content, maxRecommendations = 5) {
  // This would be a more sophisticated implementation in a real system
  // For now, we'll use a simple keyword matching approach
  
  // Keywords associated with different domains
  const domainKeywords = {
    'accessibility': [
      'accessibility', 'wcag', 'aria', 'screen reader', 'keyboard', 'a11y',
      'contrast', 'focus', 'semantic', 'alt text'
    ],
    'react': [
      'react', 'component', 'hook', 'jsx', 'props', 'state', 'effect',
      'context', 'redux', 'next.js'
    ],
    'css': [
      'css', 'flexbox', 'grid', 'responsive', 'media query', 'animation',
      'transition', 'transform', 'selector', 'specificity'
    ]
    // Add more domains as needed
  };
  
  // Count keyword matches for each domain
  const domainScores = {};
  
  for (const [domain, keywords] of Object.entries(domainKeywords)) {
    let score = 0;
    for (const keyword of keywords) {
      const regex = new RegExp(`\\b${keyword}\\b`, 'gi');
      const matches = (content.match(regex) || []).length;
      score += matches;
    }
    domainScores[domain] = score;
  }
  
  // Sort domains by score
  const sortedDomains = Object.entries(domainScores)
    .sort((a, b) => b[1] - a[1])
    .filter(([_, score]) => score > 0)
    .map(([domain]) => domain);
  
  // Define recommended modules for each domain
  const domainModules = {
    'accessibility': [
      'accessibility/core-principles',
      'accessibility/wcag-guidelines',
      'accessibility/implementation/forms',
      'accessibility/implementation/interactive-elements',
      'accessibility/testing/manual-testing'
    ],
    'react': [
      'react/component-patterns',
      'react/hooks-guide',
      'react/performance-optimization',
      'react/accessibility'
    ],
    'css': [
      'css/layout-patterns',
      'css/responsive-design',
      'css/animation-techniques',
      'css/best-practices'
    ]
    // Add more domain modules as needed
  };
  
  // Collect recommendations based on domain scores
  const recommendations = [];
  
  for (const domain of sortedDomains) {
    if (domainModules[domain]) {
      recommendations.push(...domainModules[domain]);
      if (recommendations.length >= maxRecommendations) {
        break;
      }
    }
  }
  
  return recommendations.slice(0, maxRecommendations);
}

module.exports = {
  processTemplate,
  loadPromptTemplate,
  countTokens,
  getLimitedContextContent,
  getContextSummary,
  recommendContextModules
};
