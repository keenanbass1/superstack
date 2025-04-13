#!/usr/bin/env node

/**
 * DSP Context Module Build Integration
 * 
 * This script integrates context module optimization into the build pipeline.
 * It can check for modules that need optimization and optionally run
 * optimization before continuing with the build process.
 */

const { spawn, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const { program } = require('commander');

// Configure command-line options
program
  .option('--check-modules', 'Check for modules that need optimization')
  .option('--optimize', 'Optimize modules that need improvement before building')
  .option('--threshold <number>', 'Improvement score threshold (0-100, lower means more need)', '50')
  .option('--model <model>', 'Target model for optimization', 'gpt-4-turbo')
  .option('--skip-build', 'Skip the actual build (for testing)')
  .option('--min-feedback <number>', 'Minimum feedback count to consider', '1')
  .option('--limit <number>', 'Maximum number of modules to optimize', '5')
  .option('--auto-apply', 'Automatically apply optimizations if they improve performance by at least 10%')
  .parse(process.argv);

const options = program.opts();

// Function to run a child process and handle output
function runProcess(command, args) {
  return new Promise((resolve, reject) => {
    console.log(`Running: ${command} ${args.join(' ')}`);
    const proc = spawn(command, args, { shell: true });
    
    let stdout = '';
    let stderr = '';
    
    proc.stdout.on('data', (data) => {
      const output = data.toString();
      stdout += output;
      console.log(output.trim());
    });
    
    proc.stderr.on('data', (data) => {
      const output = data.toString();
      stderr += output;
      console.error(output.trim());
    });
    
    proc.on('close', (code) => {
      if (code === 0) {
        resolve({ stdout, stderr, code });
      } else {
        reject(new Error(`Process exited with code ${code}\n${stderr}`));
      }
    });
  });
}

// Identify modules that need optimization using feedback system
async function identifyModulesNeedingOptimization() {
  try {
    const args = [
      'feedback_system.py',
      'show-needs-optimization',
      '--json',
      `--threshold=${options.threshold}`,
      `--min-feedback=${options.minFeedback}`,
      `--limit=${options.limit}`
    ];
    
    if (options.model) {
      args.push(`--model=${options.model}`);
    }
    
    const { stdout } = await runProcess('python3', args);
    const result = JSON.parse(stdout);
    return result.modules_needing_optimization || [];
  } catch (error) {
    console.error('Error identifying modules:', error.message);
    return [];
  }
}

// Optimize modules using DSP implementation
async function optimizeModules(modules) {
  const results = {
    successful: [],
    failed: [],
    improved: [],
    applied: []
  };
  
  for (const module of modules) {
    try {
      console.log(`\n🔄 Optimizing module: ${module}`);
      
      // Step 1: Run optimization
      await runProcess('python3', [
        'dsp-implementation-plan.py',
        'optimize',
        module,
        '--model', options.model,
        '--verbose'
      ]);
      results.successful.push(module);
      
      // Step 2: Evaluate improvement
      const { stdout } = await runProcess('python3', [
        'dsp-implementation-plan.py',
        'evaluate',
        module,
        '--verbose'
      ]);
      
      // Parse evaluation results to check improvement
      if (stdout.includes('IMPROVED')) {
        results.improved.push(module);
        
        // Check if we should auto-apply
        if (options.autoApply) {
          // Extract improvement percentage from output
          const match = stdout.match(/Improvement:\s+(\d+\.?\d*)%/);
          const improvementPercentage = match ? parseFloat(match[1]) : 0;
          
          if (improvementPercentage >= 10) {
            console.log(`\n✅ Auto-applying optimization for ${module} (${improvementPercentage.toFixed(2)}% improvement)`);
            await runProcess('python3', [
              'dsp-implementation-plan.py',
              'apply',
              module
            ]);
            results.applied.push(module);
            
            // Record as applied in feedback system
            await runProcess('python3', [
              'feedback_system.py',
              'mark-applied',
              module,
              options.model
            ]);
          } else {
            console.log(`\n⚠️ Improvement not sufficient for auto-apply: ${improvementPercentage.toFixed(2)}%`);
          }
        }
      }
    } catch (error) {
      console.error(`\n❌ Failed to optimize module ${module}:`, error.message);
      results.failed.push(module);
    }
  }
  
  return results;
}

// Main function
async function main() {
  try {
    if (options.checkModules) {
      console.log('\n📊 Checking for modules that need optimization...');
      const modulesToOptimize = await identifyModulesNeedingOptimization();
      
      if (modulesToOptimize.length > 0) {
        console.log(`\n🔍 Found ${modulesToOptimize.length} modules that need optimization:`);
        modulesToOptimize.forEach(module => console.log(`  - ${module}`));
        
        if (options.optimize) {
          console.log('\n🚀 Starting optimization process...');
          const results = await optimizeModules(modulesToOptimize);
          
          // Output summary
          console.log('\n📋 Optimization Summary:');
          console.log(`  Total modules processed: ${modulesToOptimize.length}`);
          console.log(`  Successfully optimized: ${results.successful.length}`);
          console.log(`  Improved modules: ${results.improved.length}`);
          console.log(`  Applied optimizations: ${results.applied.length}`);
          console.log(`  Failed optimizations: ${results.failed.length}`);
          
          if (results.failed.length > 0) {
            console.log('\n⚠️ Failed modules:');
            results.failed.forEach(module => console.log(`  - ${module}`));
          }
        } else {
          console.log('\n⚠️ Optimization skipped (use --optimize flag to optimize)');
        }
      } else {
        console.log('\n✅ No modules need optimization at this time.');
      }
    }
    
    // Continue with the normal build process
    if (!options.skipBuild) {
      console.log('\n🏗️ Running build process...');
      // Replace with your actual build command
      await runProcess('npm', ['run', 'build']);
      console.log('\n✅ Build completed successfully.');
    } else {
      console.log('\n⏩ Build process skipped (--skip-build flag)');
    }
  } catch (error) {
    console.error('\n❌ Error:', error.message);
    process.exit(1);
  }
}

// Start the process
main(); 