#!/usr/bin/env node

/**
 * Enhanced CLI for Context Management System
 * 
 * Provides a more powerful interface to the context management system,
 * with intelligent recommendations, token management, and better integration.
 */

const { program } = require('commander');
const path = require('path');
const fs = require('fs');

// Load utility modules
const contextCommands = require('./context-commands');
const contextIntegration = require('./context-integration');
const moduleRecommender = require('./utils/module-recommender');
const tokenManager = require('./utils/token-manager');
const clipboardManager = require('./utils/clipboard-manager');

// Initialize program
program
  .name('context')
  .description('AI Context Management System')
  .version('0.2.0');

// Basic context management commands
program
  .command('list')
  .description('List available context modules')
  .action(() => {
    contextCommands.listAvailableContexts();
  });

program
  .command('active')
  .description('List active context modules')
  .action(() => {
    contextCommands.listActiveContexts();
  });

program
  .command('add <modulePath>')
  .description('Add a context module to active context')
  .action((modulePath) => {
    contextCommands.addContext(modulePath);
  });

program
  .command('remove <modulePath>')
  .description('Remove a context module from active context')
  .action((modulePath) => {
    contextCommands.removeContext(modulePath);
  });

program
  .command('clear')
  .description('Clear all active context modules')
  .action(() => {
    contextCommands.clearContext();
  });

program
  .command('show <modulePath>')
  .description('Show content of a context module')
  .action((modulePath) => {
    const content = contextCommands.getContextContent(modulePath);
    if (content) {
      console.log(`\n=== ${modulePath} ===\n`);
      console.log(content);
    }
  });

// Group management commands
const groupCmd = program
  .command('group')
  .description('Manage context groups');

groupCmd
  .command('list')
  .description('List available context groups')
  .action(() => {
    contextCommands.listContextGroups();
  });

groupCmd
  .command('create <name> [modulePaths...]')
  .description('Create a new context group with specified modules')
  .action((name, modulePaths) => {
    contextCommands.createContextGroup(name, modulePaths);
  });

groupCmd
  .command('add <name>')
  .description('Add all modules from a group to active context')
  .action((name) => {
    contextCommands.applyContextGroup(name);
  });

// Enhanced clipboard integration
program
  .command('copy')
  .description('Copy active context to clipboard')
  .option('-m, --model <model>', 'Target AI model for token optimization', 'default')
  .option('-t, --tokens <limit>', 'Manual token limit override', parseInt)
  .option('--no-metrics', 'Hide token metrics')
  .action((options) => {
    // Get active context content
    const content = contextCommands.getActiveContextContent();
    
    if (!content) {
      console.error('No active context content to copy');
      return;
    }
    
    // Get token limit (from model or manual override)
    const tokenLimit = options.tokens || 
      (tokenManager.MODEL_LIMITS[options.model] || tokenManager.MODEL_LIMITS.default);
    
    // Check if content exceeds token limit
    const tokenCheck = tokenManager.checkTokenLimit(
      content, 
      options.model, 
      500 // Assume 500 tokens for user prompt
    );
    
    let finalContent = content;
    let optimizationApplied = false;
    
    if (!tokenCheck.fits) {
      console.warn(`⚠️  Content exceeds token limit for ${options.model || 'default'} model`);
      console.warn(`   Content: ~${tokenCheck.contentTokens} tokens, Available: ${tokenCheck.availableTokens} tokens`);
      
      // Offer to optimize the content
      console.log('Optimizing content to fit token limit...');
      
      const optimized = tokenManager.optimizeForTokenLimit(
        content, 
        tokenCheck.availableTokens,
        { preserveStructure: true }
      );
      
      finalContent = optimized.content;
      optimizationApplied = true;
      
      console.log(`✓ Reduced from ~${optimized.originalTokens} to ~${optimized.optimizedTokens} tokens`);
      if (optimized.truncated) {
        console.log(`  Included ${optimized.includedSections} of ${optimized.totalSections} sections`);
      }
    }
    
    // Copy to clipboard
    const result = clipboardManager.copyWithMetrics(finalContent, {
      showTokenEstimate: options.metrics !== false,
      showPreview: true,
      previewLength: 100
    });
    
    if (result.success) {
      console.log(`✓ Copied ${result.characters} characters (${result.lines} lines) to clipboard`);
      
      if (options.metrics !== false) {
        console.log(`  Estimated tokens: ~${result.tokenEstimate}`);
        console.log(`  Context preview: "${result.preview}"`);
      }
      
      if (optimizationApplied) {
        console.log('  Note: Content was optimized to fit token limit');
      }
    }
  });

// Template integration
program
  .command('prompt <templatePath>')
  .description('Process a prompt template with active context')
  .option('-v, --var <variables>', 'Variables for template in key=value format', collectVariables, {})
  .option('-t, --tokens <limit>', 'Token limit for context', parseInt, 6000)
  .option('-c, --copy', 'Copy result to clipboard', false)
  .action((templatePath, options) => {
    // Load the template
    const template = contextIntegration.loadPromptTemplate(templatePath);
    
    if (!template) {
      console.error(`Could not load template: ${templatePath}`);
      return;
    }
    
    // Process the template with context
    const processed = contextIntegration.processTemplate(
      template, 
      options.var,
      { maxTokens: options.tokens }
    );
    
    if (options.copy) {
      // Copy to clipboard
      const result = clipboardManager.copyWithMetrics(processed, {
        showTokenEstimate: true
      });
      
      if (result.success) {
        console.log(`✓ Processed template ${path.basename(templatePath)} copied to clipboard`);
        console.log(`  Characters: ${result.characters}, Lines: ${result.lines}, Est. Tokens: ${result.tokenEstimate}`);
      }
    } else {
      // Just print to console
      console.log(`\n=== Processed Template: ${path.basename(templatePath)} ===\n`);
      console.log(processed);
    }
  });

// Enhanced analysis and recommendations
program
  .command('analyze [filePath]')
  .description('Analyze content and recommend context modules')
  .option('-c, --clipboard', 'Analyze clipboard content instead of file', false)
  .option('-a, --add', 'Automatically add recommended modules', false)
  .option('-g, --group', 'Automatically add recommended groups', false)
  .option('-d, --detailed', 'Show detailed analysis', false)
  .action(async (filePath, options) => {
    let content = '';
    
    // Get content from file or clipboard
    if (options.clipboard) {
      content = clipboardManager.readFromClipboard();
      console.log('Analyzing clipboard content...');
    } else if (filePath) {
      try {
        content = fs.readFileSync(filePath, 'utf8');
        console.log(`Analyzing file: ${filePath}...`);
      } catch (error) {
        console.error(`Error reading file: ${error.message}`);
        return;
      }
    } else {
      console.error('No content to analyze. Provide a file path or use --clipboard');
      return;
    }
    
    if (!content) {
      console.error('No content available to analyze');
      return;
    }
    
    // Get recommendations
    const recommendations = moduleRecommender.getRecommendations(content, {
      maxModules: 5,
      maxGroups: 2,
      includeDomainAnalysis: options.detailed
    });
    
    // Display results
    console.log('\nRecommended context modules:');
    if (recommendations.modules.length > 0) {
      recommendations.modules.forEach((module, index) => {
        console.log(`  ${index + 1}. ${module}`);
      });
    } else {
      console.log('  No specific modules recommended for this content');
    }
    
    console.log('\nRecommended context groups:');
    if (recommendations.groups.length > 0) {
      recommendations.groups.forEach((group, index) => {
        console.log(`  ${index + 1}. ${group}`);
      });
    } else {
      console.log('  No specific groups recommended for this content');
    }
    
    // Show detailed analysis if requested
    if (options.detailed && recommendations.domainAnalysis) {
      console.log('\nDomain Analysis:');
      recommendations.domainAnalysis.forEach(domain => {
        console.log(`  ${domain.domain}: score ${domain.score}`);
        
        if (domain.matches.keywords && Object.keys(domain.matches.keywords).length > 0) {
          console.log('    Keywords:');
          Object.entries(domain.matches.keywords)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
            .forEach(([keyword, count]) => {
              console.log(`      - "${keyword}" (${count} matches)`);
            });
        }
      });
    }
    
    // Auto-add modules if requested
    if (options.add && recommendations.modules.length > 0) {
      console.log('\nAdding recommended modules to active context:');
      let addedCount = 0;
      
      for (const module of recommendations.modules) {
        const success = contextCommands.addContext(module);
        if (success) addedCount++;
      }
      
      console.log(`  Added ${addedCount} modules to active context`);
    }
    
    // Auto-add groups if requested
    if (options.group && recommendations.groups.length > 0) {
      console.log('\nAdding recommended groups to active context:');
      let addedCount = 0;
      
      for (const group of recommendations.groups) {
        const success = contextCommands.applyContextGroup(group);
        if (success) addedCount++;
      }
      
      console.log(`  Applied ${addedCount} groups to active context`);
    }
  });

// Statistics and metrics
program
  .command('stats')
  .description('Show context system statistics')
  .action(() => {
    const summary = contextIntegration.getContextSummary();
    
    console.log('\nContext System Statistics');
    console.log('========================');
    console.log(`Active Modules: ${summary.activeModules}`);
    console.log(`Total Tokens: ~${summary.totalTokens}`);
    console.log(`\nToken Estimates:`);
    console.log(`  Claude: ${summary.tokenEstimate.claude}`);
    console.log(`  GPT-4: ${summary.tokenEstimate.gpt4}`);
    
    console.log('\nActive Modules:');
    summary.modules.forEach(module => {
      console.log(`  ${module.path}`);
      console.log(`    - Tokens: ~${module.tokens}`);
      console.log(`    - Lines: ${module.lines}`);
      console.log(`    - Size: ${formatBytes(module.characters)}`);
    });
  });

// Initialize pre-defined groups for accessibility module
program
  .command('init-accessibility')
  .description('Initialize accessibility context groups')
  .action(() => {
    // Define the accessibility groups
    const groups = {
      'web-accessibility': [
        'accessibility/core-principles',
        'accessibility/wcag-guidelines', 
        'accessibility/aria-implementation',
        'accessibility/semantic-html'
      ],
      'accessibility-review': [
        'accessibility/checklists',
        'accessibility/testing/axe-guide',
        'accessibility/testing/manual-testing',
        'accessibility/decision-tree'
      ],
      'accessibility-forms': [
        'accessibility/implementation/forms',
        'accessibility/implementation/keyboard-navigation',
        'accessibility/implementation/interactive-elements'
      ],
      'accessibility-media': [
        'accessibility/implementation/images-media',
        'accessibility/implementation/color-contrast',
        'accessibility/implementation/responsive-design'
      ],
      'accessibility-comprehensive': [
        'accessibility/core-principles',
        'accessibility/wcag-guidelines',
        'accessibility/implementation/forms',
        'accessibility/implementation/interactive-elements',
        'accessibility/testing/manual-testing',
        'accessibility/decision-tree'
      ]
    };
    
    // Create each group
    console.log('Initializing accessibility context groups:');
    
    for (const [name, modules] of Object.entries(groups)) {
      const success = contextCommands.createContextGroup(name, modules);
      console.log(`  ${success ? '✓' : '✗'} ${name}`);
    }
  });

// Helper function to collect key=value variables
function collectVariables(value, previous) {
  const [key, val] = value.split('=');
  if (key && val) {
    previous[key] = val;
  }
  return previous;
}

// Helper function to format bytes
function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(decimals)) + ' ' + sizes[i];
}

// Execute the program
program.parse(process.argv);
