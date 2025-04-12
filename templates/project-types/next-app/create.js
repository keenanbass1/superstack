#!/usr/bin/env node
/**
 * Next.js Project Template Creator
 * 
 * This script creates a new Next.js project by copying the template
 * and replacing placeholders with the project-specific values.
 */

const fs = require('fs-extra');
const path = require('path');
const { execSync } = require('child_process');

// Parse arguments
const args = process.argv.slice(2);
if (args.length < 2) {
  console.error('Usage: create.js <project-name> <target-directory>');
  process.exit(1);
}

const projectName = args[0];
const targetDir = args[1];

// Validate project name
if (!/^[a-z0-9-_]+$/i.test(projectName)) {
  console.error('Error: Project name can only contain letters, numbers, hyphens, and underscores');
  process.exit(1);
}

// Check if target directory already exists
if (fs.existsSync(targetDir)) {
  console.error(`Error: Directory already exists: ${targetDir}`);
  process.exit(1);
}

// Get template directory
const templateDir = path.join(__dirname, 'template');

// Main function
async function createProject() {
  try {
    console.log(`Creating new Next.js project: ${projectName}`);
    
    // Copy template to target directory
    console.log('Copying template files...');
    await fs.copy(templateDir, targetDir);
    
    // Process all files and replace placeholders
    console.log('Customizing template for your project...');
    await processDirectory(targetDir);
    
    // Initialize git repository
    console.log('Initializing git repository...');
    try {
      execSync('git init', { cwd: targetDir, stdio: 'ignore' });
    } catch (error) {
      console.warn('Warning: Failed to initialize git repository');
    }
    
    console.log('\nProject created successfully! 🎉');
    console.log('\nNext steps:');
    console.log(`  1. cd ${path.relative(process.cwd(), targetDir)}`);
    console.log('  2. npm install');
    console.log('  3. npm run dev');
    console.log('\nHappy coding! 🚀');
  } catch (error) {
    console.error('Error creating project:', error);
    process.exit(1);
  }
}

// Helper function to process all files in a directory
async function processDirectory(dirPath) {
  const items = await fs.readdir(dirPath);
  
  for (const item of items) {
    const itemPath = path.join(dirPath, item);
    const stats = await fs.stat(itemPath);
    
    if (stats.isDirectory()) {
      // Recursively process subdirectories
      await processDirectory(itemPath);
    } else {
      // Process file
      await processFile(itemPath);
    }
  }
}

// Helper function to process a file
async function processFile(filePath) {
  // Skip binary files
  const ext = path.extname(filePath).toLowerCase();
  const binaryExts = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.woff', '.woff2', '.ttf', '.eot'];
  
  if (binaryExts.includes(ext)) {
    return;
  }
  
  try {
    let content = await fs.readFile(filePath, 'utf8');
    
    // Replace placeholders
    content = content.replace(/\{\{projectName\}\}/g, projectName);
    
    // Write modified content back to file
    await fs.writeFile(filePath, content, 'utf8');
  } catch (error) {
    console.warn(`Warning: Could not process file ${filePath}`, error.message);
  }
}

// Run the script
createProject();
