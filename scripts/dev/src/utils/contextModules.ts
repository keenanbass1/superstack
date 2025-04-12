import fs from 'fs-extra';
import path from 'path';
import { glob } from 'glob';
import { getPaths } from './paths.js';
import os from 'os';

export interface ContextModule {
  path: string;              // Relative path to module
  title: string;             // Module title
  description: string;       // Short description
  domain: string;            // Knowledge domain (design, development, etc.)
  type: string;              // Module type (principles, patterns, etc.)
}

export interface ActiveContext {
  modules: string[];         // Array of active module paths
  timestamp: string;         // Last updated timestamp
  project?: string;          // Current project (if in project directory)
}

export interface ContextGroup {
  modules: string[];         // Array of module paths in this group
  description?: string;      // Optional group description
  created: string;           // Creation timestamp
  updated: string;           // Last updated timestamp
}

export interface ContextGroups {
  [groupName: string]: ContextGroup;
}

/**
 * Path to the context configuration directory
 */
function getContextConfigDir(): string {
  return path.join(os.homedir(), '.config', 'superstack');
}

/**
 * Ensure the context configuration directory exists
 */
async function ensureContextConfigDir(): Promise<void> {
  await fs.ensureDir(getContextConfigDir());
}

/**
 * Path to the active context file
 */
function getActiveContextPath(): string {
  return path.join(getContextConfigDir(), 'active-context.json');
}

/**
 * Path to the context groups file
 */
function getContextGroupsPath(): string {
  return path.join(getContextConfigDir(), 'context-groups.json');
}

/**
 * Get path to context module directory
 */
export function getContextModulesPath(): string {
  const { superstackDir } = getPaths();
  return path.join(superstackDir, 'docs', 'ai-context');
}

/**
 * Get all available context modules
 */
export async function getAllContextModules(): Promise<ContextModule[]> {
  const modulesPath = getContextModulesPath();
  
  // Recursively find all .md files using glob pattern
  const files = await glob('**/*.md', { cwd: modulesPath });
  
  // Filter out README and similar files
  const moduleFiles = files.filter(file => 
    !file.includes('README') && 
    !file.includes('CONTRIBUTING') &&
    !file.includes('CONTEXT-MODULE-WORKFLOW') &&
    !file.includes('IMPLEMENTATION-SUMMARY')
  );
  
  // Map to ContextModule objects
  return Promise.all(moduleFiles.map(async file => {
    const fullPath = path.join(modulesPath, file);
    const content = await fs.readFile(fullPath, 'utf8');
    
    // Extract title and description from first few lines
    const lines = content.split('\n').slice(0, 10);
    const titleLine = lines.find(line => line.startsWith('# ')) || '';
    const descLine = lines.find(line => line.startsWith('> ')) || '';
    
    const title = titleLine.replace('# ', '').trim();
    const description = descLine.replace('> ', '').trim();
    
    // Determine domain and type from path
    const pathParts = file.split(path.sep);
    const domain = pathParts[0] || 'unknown';
    const type = pathParts.length > 1 ? pathParts[1] : 'unknown';
    
    return {
      path: file,
      title,
      description,
      domain,
      type
    };
  }));
}

/**
 * Get active context
 */
export async function getActiveContext(): Promise<ActiveContext> {
  await ensureContextConfigDir();
  const configPath = getActiveContextPath();
  
  try {
    const data = await fs.readFile(configPath, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    // Return default if file doesn't exist
    return { 
      modules: [], 
      timestamp: new Date().toISOString() 
    };
  }
}

/**
 * Save active context
 */
export async function saveActiveContext(context: ActiveContext): Promise<void> {
  await ensureContextConfigDir();
  const configPath = getActiveContextPath();
  
  context.timestamp = new Date().toISOString();
  await fs.writeFile(configPath, JSON.stringify(context, null, 2), 'utf8');
}

/**
 * Add modules to active context
 */
export async function addModulesToActiveContext(modulePaths: string[]): Promise<void> {
  const activeContext = await getActiveContext();
  
  // Add modules, avoiding duplicates
  const uniqueModules = new Set([...activeContext.modules, ...modulePaths]);
  activeContext.modules = Array.from(uniqueModules);
  
  await saveActiveContext(activeContext);
}

/**
 * Remove modules from active context
 */
export async function removeModulesFromActiveContext(modulePaths: string[]): Promise<void> {
  const activeContext = await getActiveContext();
  
  activeContext.modules = activeContext.modules.filter(
    module => !modulePaths.includes(module)
  );
  
  await saveActiveContext(activeContext);
}

/**
 * Clear all active context
 */
export async function clearActiveContext(): Promise<void> {
  await saveActiveContext({ 
    modules: [], 
    timestamp: new Date().toISOString() 
  });
}

/**
 * Get all context groups
 */
export async function getContextGroups(): Promise<ContextGroups> {
  await ensureContextConfigDir();
  const configPath = getContextGroupsPath();
  
  try {
    const data = await fs.readFile(configPath, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    // Return empty object if file doesn't exist
    return {};
  }
}

/**
 * Create a new context group
 */
export async function createContextGroup(
  name: string, 
  modulePaths: string[], 
  description?: string
): Promise<void> {
  const groups = await getContextGroups();
  
  groups[name] = {
    modules: modulePaths,
    description,
    created: new Date().toISOString(),
    updated: new Date().toISOString()
  };
  
  await ensureContextConfigDir();
  const configPath = getContextGroupsPath();
  await fs.writeFile(configPath, JSON.stringify(groups, null, 2), 'utf8');
}

/**
 * Delete a context group
 */
export async function deleteContextGroup(name: string): Promise<boolean> {
  const groups = await getContextGroups();
  
  if (!groups[name]) {
    return false;
  }
  
  delete groups[name];
  
  await ensureContextConfigDir();
  const configPath = getContextGroupsPath();
  await fs.writeFile(configPath, JSON.stringify(groups, null, 2), 'utf8');
  
  return true;
}

/**
 * Add a context group to active context
 */
export async function addGroupToActiveContext(groupName: string): Promise<boolean> {
  const groups = await getContextGroups();
  
  if (!groups[groupName]) {
    return false;
  }
  
  await addModulesToActiveContext(groups[groupName].modules);
  return true;
}

/**
 * Get content of a context module
 */
export async function getModuleContent(modulePath: string): Promise<string> {
  const fullPath = path.join(getContextModulesPath(), modulePath);
  
  if (!await fs.pathExists(fullPath)) {
    throw new Error(`Module not found: ${modulePath}`);
  }
  
  return fs.readFile(fullPath, 'utf8');
}

/**
 * Get formatted content of all active context modules
 */
export async function getFormattedActiveContext(): Promise<string> {
  const activeContext = await getActiveContext();
  
  if (activeContext.modules.length === 0) {
    return '';
  }
  
  const moduleContents = await Promise.all(
    activeContext.modules.map(async modulePath => {
      try {
        const content = await getModuleContent(modulePath);
        return { path: modulePath, content };
      } catch (error) {
        return { path: modulePath, content: `Error loading module: ${modulePath}` };
      }
    })
  );
  
  // Format context as markdown with headers for each module
  const formattedContext = moduleContents
    .map(m => `## ${m.path}\n\n${m.content}`)
    .join('\n\n---\n\n');
  
  // Wrap in context tags for AI tools
  return `<context>\n${formattedContext}\n</context>`;
}
