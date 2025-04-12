#!/usr/bin/env node

/**
 * Initialize Accessibility Context Groups
 * 
 * This script creates pre-defined context groups for the
 * accessibility module to make it easier to use in different
 * development scenarios.
 */

const contextCommands = require('./context-commands');
const path = require('path');

// Define accessibility-focused context groups
const ACCESSIBILITY_GROUPS = {
  // Core accessibility knowledge
  'web-accessibility': [
    'accessibility/core-principles',
    'accessibility/wcag-guidelines', 
    'accessibility/aria-implementation',
    'accessibility/semantic-html'
  ],
  
  // Focused on accessibility reviewing and testing
  'accessibility-review': [
    'accessibility/checklists',
    'accessibility/testing/axe-guide',
    'accessibility/testing/manual-testing',
    'accessibility/decision-tree'
  ],
  
  // Forms and interactive elements
  'accessibility-forms': [
    'accessibility/implementation/forms',
    'accessibility/implementation/keyboard-navigation',
    'accessibility/implementation/interactive-elements'
  ],
  
  // Media and visual components
  'accessibility-media': [
    'accessibility/implementation/images-media',
    'accessibility/implementation/color-contrast',
    'accessibility/implementation/responsive-design'
  ],
  
  // Cognitive accessibility
  'accessibility-cognitive': [
    'accessibility/cognitive-considerations',
    'accessibility/implementation/forms',
    'accessibility/implementation/responsive-design'
  ],
  
  // Comprehensive accessibility knowledge
  'accessibility-comprehensive': [
    'accessibility/core-principles',
    'accessibility/wcag-guidelines',
    'accessibility/semantic-html',
    'accessibility/implementation/forms',
    'accessibility/implementation/interactive-elements',
    'accessibility/implementation/color-contrast',
    'accessibility/testing/manual-testing',
    'accessibility/decision-tree'
  ]
};

/**
 * Initialize accessibility context groups
 */
function initAccessibilityGroups() {
  console.log('Initializing accessibility context groups:');
  let successCount = 0;
  let failCount = 0;
  
  for (const [name, modules] of Object.entries(ACCESSIBILITY_GROUPS)) {
    try {
      const success = contextCommands.createContextGroup(name, modules);
      
      if (success) {
        console.log(`  ✓ ${name}`);
        successCount++;
      } else {
        console.log(`  ✗ ${name}`);
        failCount++;
      }
    } catch (error) {
      console.log(`  ✗ ${name} - Error: ${error.message}`);
      failCount++;
    }
  }
  
  console.log(`\nSummary: ${successCount} groups created, ${failCount} failed`);
}

/**
 * Display usage information
 */
function showUsage() {
  console.log('\nInitialize Accessibility Context Groups');
  console.log('======================================');
  console.log('\nThis script creates pre-defined context groups for the accessibility module.');
  console.log('Usage:');
  console.log('  node init-accessibility-groups.js');
  console.log('\nAvailable groups:');
  
  for (const [name, modules] of Object.entries(ACCESSIBILITY_GROUPS)) {
    console.log(`  ${name}: ${modules.length} modules`);
  }
}

// Run the initialization if called directly
if (require.main === module) {
  if (process.argv.includes('--help') || process.argv.includes('-h')) {
    showUsage();
  } else {
    // Initialize the context system (ensure paths are set up)
    console.log('Initializing context system...');
    
    // Create the groups
    initAccessibilityGroups();
  }
}

module.exports = {
  ACCESSIBILITY_GROUPS,
  initAccessibilityGroups
};
