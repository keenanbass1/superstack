import path from 'path';
import os from 'os';
import fs from 'fs-extra';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

interface SystemPaths {
  homeDir: string;
  devDir: string;
  superstackDir: string;
  configDir: string;
  templatesDir: string;
  projectsDir: string;
  logsDir: string;
  scriptsDir: string;
  llmDir: string;
  schemasDir: string;
  currentDir: string;
}

/**
 * Setup environment variables for the CLI
 */
export function setupEnvironment(): void {
  // Try to load from .env file if it exists
  dotenv.config();

  // Get the directory where this file is located
  const __filename = fileURLToPath(import.meta.url);
  const __dirname = path.dirname(__filename);

  // Set default environment variables if not already set
  if (!process.env.DEV_ROOT) {
    // Calculate the dev root directory based on the location of this file
    // This file is in scripts/dev/dist/utils, so we need to go up several levels
    process.env.DEV_ROOT = path.resolve(path.join(__dirname, '../../../../../'));
  }

  if (!process.env.PROJECTS_DIR) {
    process.env.PROJECTS_DIR = path.join(process.env.DEV_ROOT, 'projects');
  }
}

/**
 * Get system paths
 */
export function getPaths(): SystemPaths {
  const homeDir = os.homedir();

  // Use environment variables if available, otherwise use default paths
  const devDir = process.env.DEV_ROOT || path.join(homeDir, 'dev');
  const projectsDir = process.env.PROJECTS_DIR || path.join(devDir, 'projects');
  const superstackDir = path.join(devDir, 'superstack');
  const currentDir = process.cwd();

  return {
    homeDir,
    devDir,
    superstackDir,
    configDir: path.join(superstackDir, 'config'),
    templatesDir: path.join(superstackDir, 'templates'),
    projectsDir,
    logsDir: path.join(superstackDir, 'logs'),
    scriptsDir: path.join(superstackDir, 'scripts'),
    llmDir: path.join(superstackDir, 'llm'),
    schemasDir: path.join(superstackDir, 'llm', 'schemas'),
    currentDir
  };
}

/**
 * Get project templates directory
 */
export function getProjectTemplateDir(templateName: string): string {
  const { templatesDir } = getPaths();
  return path.join(templatesDir, 'project-types', templateName);
}

/**
 * Check if current directory is a Superstack project
 */
export function isSuperstackProject(dir = process.cwd()): boolean {
  return fs.existsSync(path.join(dir, '.superstack.json'));
}

/**
 * Get the project root directory
 * Traverses up the directory tree to find the project root
 */
export function getProjectRoot(startDir = process.cwd()): string | null {
  let currentDir = startDir;

  while (currentDir !== os.homedir() && currentDir !== '/') {
    if (fs.existsSync(path.join(currentDir, '.superstack.json'))) {
      return currentDir;
    }

    currentDir = path.dirname(currentDir);
  }

  return null;
}

/**
 * Ensure all system paths exist
 */
export function ensureSystemPaths(): void {
  const paths = getPaths();

  Object.values(paths).forEach(dir => {
    if (dir !== paths.currentDir) {
      fs.ensureDirSync(dir);
    }
  });

  // Ensure subdirectories exist too
  fs.ensureDirSync(path.join(paths.templatesDir, 'project-types'));
  fs.ensureDirSync(path.join(paths.templatesDir, 'prompts'));
  fs.ensureDirSync(path.join(paths.templatesDir, 'shell'));
  fs.ensureDirSync(path.join(paths.llmDir, 'schemas'));
}