import fs from 'fs-extra';
import path from 'path';
import { getPaths } from './paths.js';

// Define path constants since they're not exported from paths.js
const CONTEXT_SCHEMA_PATH = path.join(getPaths().schemasDir, 'context-schema.json');
const PROJECT_CONTEXT_TEMPLATE_PATH = path.join(getPaths().templatesDir, 'context', 'project-context-template.md');

/**
 * Utility functions for managing project context
 */
export const contextUtils = {
  /**
   * Get the context file path for the current directory
   */
  getContextPath: (dir: string = process.cwd()): string => {
    return path.join(dir, 'project-context.md');
  },

  /**
   * Check if a context file exists in the given directory
   */
  contextExists: async (dir: string = process.cwd()): Promise<boolean> => {
    const contextPath = contextUtils.getContextPath(dir);
    return fs.pathExists(contextPath);
  },

  /**
   * Initialize a new context file in the given directory
   */
  initContext: async (
    dir: string = process.cwd(),
    projectName: string = path.basename(dir),
    overwrite: boolean = false
  ): Promise<boolean> => {
    const contextPath = contextUtils.getContextPath(dir);
    
    // Check if context already exists
    if (await fs.pathExists(contextPath) && !overwrite) {
      return false;
    }
    
    // Ensure template exists
    if (!await fs.pathExists(PROJECT_CONTEXT_TEMPLATE_PATH)) {
      throw new Error(`Template not found at ${PROJECT_CONTEXT_TEMPLATE_PATH}`);
    }
    
    // Read template and replace project name
    let templateContent = await fs.readFile(PROJECT_CONTEXT_TEMPLATE_PATH, 'utf8');
    templateContent = templateContent.replace(/\{\{PROJECT_NAME\}\}/g, projectName);
    
    // Write the context file
    await fs.writeFile(contextPath, templateContent);
    
    return true;
  },

  /**
   * Read the context file from the given directory
   */
  readContext: async (dir: string = process.cwd()): Promise<string> => {
    const contextPath = contextUtils.getContextPath(dir);
    
    if (!await fs.pathExists(contextPath)) {
      throw new Error('No context file found');
    }
    
    return fs.readFile(contextPath, 'utf8');
  },

  /**
   * Validate context against schema
   * Returns array of unfilled placeholders or empty array if all good
   */
  validateContext: async (contextContent: string): Promise<string[]> => {
    // For now, just check for unfilled placeholders
    const placeholderRegex = /\{\{([A-Z_]+)\}\}/g;
    return Array.from(contextContent.matchAll(placeholderRegex))
      .map(match => match[0]);
    
    // TODO: Implement full schema validation when we add JSON parsing
  },

  /**
   * Push context to AI assistants
   * Currently a stub for future implementation
   */
  pushContext: async (contextContent: string): Promise<{[key: string]: boolean}> => {
    // TODO: Implement actual pushing to AI services
    
    // Just return success for now
    return {
      claude: true,
      gpt: true,
      cursor: true
    };
  }
};
