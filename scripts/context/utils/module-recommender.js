/**
 * Context Module Recommender
 * 
 * This utility analyzes content and recommends appropriate context modules
 * based on content topics, keywords, and patterns.
 */

// Domain definitions with associated keywords, modules, and patterns
const DOMAIN_DEFINITIONS = {
  'accessibility': {
    keywords: [
      'accessibility', 'wcag', 'aria', 'screen reader', 'keyboard', 'a11y',
      'contrast', 'focus', 'semantic', 'alt text', 'form label', 'landmark',
      'tab index', 'color contrast', 'tabindex', 'role', 'assistive technology'
    ],
    codePatterns: [
      /\baria-[a-z]+/i,
      /\brole="[a-z]+"/i,
      /\btabindex/i,
      /\balt="[^"]*"/i,
      /<label\b/i
    ],
    recommendedModules: [
      'accessibility/core-principles',
      'accessibility/wcag-guidelines',
      'accessibility/aria-implementation',
      'accessibility/semantic-html',
      'accessibility/implementation/forms',
      'accessibility/implementation/interactive-elements',
      'accessibility/implementation/keyboard-navigation',
      'accessibility/testing/axe-guide',
      'accessibility/testing/manual-testing'
    ],
    contextGroups: [
      'web-accessibility',
      'accessibility-review',
      'accessibility-forms'
    ]
  },
  
  'react': {
    keywords: [
      'react', 'component', 'hook', 'jsx', 'props', 'state', 'effect',
      'context', 'redux', 'next.js', 'usestate', 'useeffect', 'usememo',
      'functional component', 'class component', 'react router'
    ],
    codePatterns: [
      /\bimport\s+React\b/i,
      /\buseState\(/i,
      /\buseEffect\(/i,
      /\breturn\s*\(\s*</i,
      /<[A-Z][A-Za-z]*\s/i, // React components
      /^function\s+[A-Z][A-Za-z]*\s*\(/m // Function component
    ],
    recommendedModules: [
      'react/component-patterns',
      'react/hooks-guide',
      'react/performance-optimization',
      'react/accessibility'
    ],
    contextGroups: [
      'react-basics',
      'react-advanced',
      'react-performance'
    ]
  },
  
  'css': {
    keywords: [
      'css', 'flexbox', 'grid', 'responsive', 'media query', 'animation',
      'transition', 'transform', 'selector', 'specificity', 'tailwind',
      'sass', 'scss', 'css-in-js', 'styled-components'
    ],
    codePatterns: [
      /\bdisplay:\s*(flex|grid)\b/i,
      /@media\s+/i,
      /\banimation\b/i,
      /\btransition\b/i,
      /\b(margin|padding|border|width|height)\b/i
    ],
    recommendedModules: [
      'css/layout-patterns',
      'css/responsive-design',
      'css/animation-techniques',
      'css/best-practices'
    ],
    contextGroups: [
      'css-fundamentals',
      'css-advanced'
    ]
  },
  
  // Add more domains as needed
};

/**
 * Score content for relevance to each domain
 * @param {string} content The content to analyze
 * @returns {Object} Domain scores and match details
 */
function scoreContentDomains(content) {
  const results = {};
  
  for (const [domain, definition] of Object.entries(DOMAIN_DEFINITIONS)) {
    let score = 0;
    const matches = {
      keywords: {},
      codePatterns: []
    };
    
    // Check for keyword matches
    for (const keyword of definition.keywords) {
      const regex = new RegExp(`\\b${keyword}\\b`, 'gi');
      const keywordMatches = (content.match(regex) || []).length;
      
      if (keywordMatches > 0) {
        matches.keywords[keyword] = keywordMatches;
        score += keywordMatches;
      }
    }
    
    // Check for code pattern matches
    for (const pattern of definition.codePatterns) {
      const patternMatches = (content.match(pattern) || []).length;
      
      if (patternMatches > 0) {
        matches.codePatterns.push({
          pattern: pattern.toString(),
          count: patternMatches
        });
        
        // Code patterns are weighted more heavily
        score += patternMatches * 2;
      }
    }
    
    results[domain] = {
      score,
      matches
    };
  }
  
  return results;
}

/**
 * Recommend context modules based on content analysis
 * @param {string} content The content to analyze
 * @param {Object} options Options for recommendations
 * @returns {Object} Recommendations and analysis results
 */
function getRecommendations(content, options = {}) {
  const {
    maxModules = 5,
    maxGroups = 2,
    minScore = 2,
    includeDomainAnalysis = false
  } = options;
  
  // Score content against domains
  const domainScores = scoreContentDomains(content);
  
  // Sort domains by score
  const rankedDomains = Object.entries(domainScores)
    .map(([domain, data]) => ({
      domain,
      score: data.score,
      matches: data.matches
    }))
    .sort((a, b) => b.score - a.score)
    .filter(item => item.score >= minScore);
  
  // Collect module recommendations
  const moduleRecommendations = [];
  const groupRecommendations = [];
  
  for (const { domain, score } of rankedDomains) {
    const definition = DOMAIN_DEFINITIONS[domain];
    
    // Add recommended modules
    for (const module of definition.recommendedModules) {
      if (!moduleRecommendations.includes(module)) {
        moduleRecommendations.push(module);
        
        if (moduleRecommendations.length >= maxModules) {
          break;
        }
      }
    }
    
    // Add recommended groups
    for (const group of definition.contextGroups) {
      if (!groupRecommendations.includes(group)) {
        groupRecommendations.push(group);
        
        if (groupRecommendations.length >= maxGroups) {
          break;
        }
      }
    }
  }
  
  // Prepare the result
  const result = {
    modules: moduleRecommendations.slice(0, maxModules),
    groups: groupRecommendations.slice(0, maxGroups)
  };
  
  // Include domain analysis if requested
  if (includeDomainAnalysis) {
    result.domainAnalysis = rankedDomains;
  }
  
  return result;
}

/**
 * Get a summary of available context modules by domain
 * @returns {Object} Summary of available modules
 */
function getModuleSummary() {
  const summary = {};
  
  for (const [domain, definition] of Object.entries(DOMAIN_DEFINITIONS)) {
    summary[domain] = {
      modules: definition.recommendedModules,
      groups: definition.contextGroups
    };
  }
  
  return summary;
}

module.exports = {
  getRecommendations,
  scoreContentDomains,
  getModuleSummary,
  DOMAIN_DEFINITIONS
};
