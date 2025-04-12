/**
 * Token Management Utilities
 * 
 * Tools for managing token usage, counting, and optimizing context for 
 * different AI models and their token limits.
 */

// Constants for token estimation
const AVG_CHARS_PER_TOKEN = 4; // General approximation
const TOKEN_OVERHEAD_PERCENT = 10; // Overhead for metadata, etc.

// Model-specific token limits
const MODEL_LIMITS = {
  'gpt-3.5-turbo': 4096,
  'gpt-4': 8192,
  'gpt-4-32k': 32768,
  'claude-2': 100000,
  'claude-instant': 100000,
  'claude-3-opus': 200000,
  'claude-3-sonnet': 180000,
  'claude-3-haiku': 150000,
  'default': 4096
};

/**
 * Count tokens in a text string (approximate)
 * @param {string} text The text to count tokens for
 * @returns {number} Approximate token count
 */
function estimateTokenCount(text) {
  if (!text) return 0;
  
  // Simple approximation based on character count
  return Math.ceil(text.length / AVG_CHARS_PER_TOKEN);
}

/**
 * Get more precise token count estimates by text properties
 * @param {string} text The text to analyze
 * @returns {Object} Token count estimates by different metrics
 */
function getDetailedTokenEstimate(text) {
  if (!text) {
    return {
      byChars: 0,
      byWords: 0,
      byLines: 0,
      recommended: 0
    };
  }
  
  // Character-based (most common approximation)
  const byChars = Math.ceil(text.length / AVG_CHARS_PER_TOKEN);
  
  // Word-based (good for English text)
  const words = text.split(/\s+/).filter(w => w.length > 0).length;
  const byWords = Math.ceil(words * 0.75); // Most words are ~0.75 tokens
  
  // Line-based (helpful for code)
  const lines = text.split('\n').length;
  const byLines = Math.ceil(lines * 5); // Average line might be ~5 tokens
  
  // Get a recommended estimate (blended approach)
  // Give more weight to character-based for general content
  const recommended = Math.ceil((byChars * 2 + byWords + byLines) / 4);
  
  return {
    byChars,
    byWords,
    byLines,
    recommended
  };
}

/**
 * Check if content fits within a model's token limit
 * @param {string} content The content to check
 * @param {string} model The model name to check against
 * @param {number} userPromptTokens Estimated tokens for user's prompt
 * @returns {Object} Status information about token usage
 */
function checkTokenLimit(content, model = 'default', userPromptTokens = 500) {
  // Get the token limit for the specified model
  const modelLimit = MODEL_LIMITS[model] || MODEL_LIMITS.default;
  
  // Estimate tokens for the content
  const contentTokens = estimateTokenCount(content);
  
  // Calculate overhead (model responses, formatting, etc.)
  const overheadTokens = Math.ceil(modelLimit * (TOKEN_OVERHEAD_PERCENT / 100));
  
  // Calculate available tokens for context
  const availableTokens = modelLimit - userPromptTokens - overheadTokens;
  
  // Check if content fits
  const fits = contentTokens <= availableTokens;
  
  return {
    fits,
    contentTokens,
    availableTokens,
    modelLimit,
    userPromptTokens,
    overheadTokens,
    usage: {
      percentOfAvailable: Math.round((contentTokens / availableTokens) * 100),
      percentOfTotal: Math.round((contentTokens / modelLimit) * 100)
    },
    recommendation: fits ? 'Content fits within limits' : 'Content exceeds model limit'
  };
}

/**
 * Optimize content to fit within token limits
 * @param {string} content The content to optimize
 * @param {number} targetTokens Target token count
 * @param {Object} options Options for optimization
 * @returns {Object} Optimized content and metadata
 */
function optimizeForTokenLimit(content, targetTokens, options = {}) {
  const {
    preserveStructure = true,
    prioritizeSections = []
  } = options;
  
  // If content already fits, return as is
  const currentTokens = estimateTokenCount(content);
  if (currentTokens <= targetTokens) {
    return {
      content,
      originalTokens: currentTokens,
      optimizedTokens: currentTokens,
      truncated: false
    };
  }
  
  // Simple approach: truncate the content
  if (!preserveStructure) {
    const ratio = targetTokens / currentTokens;
    const targetChars = Math.floor(content.length * ratio);
    const truncatedContent = content.slice(0, targetChars) + '\n\n[Content truncated to fit token limit]';
    
    return {
      content: truncatedContent,
      originalTokens: currentTokens,
      optimizedTokens: estimateTokenCount(truncatedContent),
      truncated: true
    };
  }
  
  // More sophisticated approach: preserve structure by working with sections
  const sections = content.split(/\n\s*\n/); // Split by paragraph breaks
  
  // If we have priority sections, move them to the front
  if (prioritizeSections.length > 0) {
    // Create a score for each section based on keywords
    const sectionScores = sections.map(section => {
      let score = 0;
      for (const keyword of prioritizeSections) {
        if (section.toLowerCase().includes(keyword.toLowerCase())) {
          score += 1;
        }
      }
      return score;
    });
    
    // Sort sections by score (descending)
    const sortedSections = sections
      .map((section, index) => ({ section, score: sectionScores[index] }))
      .sort((a, b) => b.score - a.score)
      .map(item => item.section);
    
    sections.length = 0;
    sections.push(...sortedSections);
  }
  
  // Grab sections until we hit the target token count
  let optimizedContent = '';
  let currentOptimizedTokens = 0;
  let includedSections = 0;
  
  for (const section of sections) {
    const sectionTokens = estimateTokenCount(section);
    
    if (currentOptimizedTokens + sectionTokens <= targetTokens) {
      optimizedContent += section + '\n\n';
      currentOptimizedTokens += sectionTokens;
      includedSections++;
    } else {
      break;
    }
  }
  
  // Add truncation notice if needed
  if (includedSections < sections.length) {
    optimizedContent += '[Content truncated to fit token limit]';
  }
  
  return {
    content: optimizedContent,
    originalTokens: currentTokens,
    optimizedTokens: estimateTokenCount(optimizedContent),
    truncated: includedSections < sections.length,
    includedSections,
    totalSections: sections.length
  };
}

module.exports = {
  estimateTokenCount,
  getDetailedTokenEstimate,
  checkTokenLimit,
  optimizeForTokenLimit,
  MODEL_LIMITS
};
