import fs from 'fs-extra';
import path from 'path';
import { log, section } from '../../utils/logger.js';
import { getPaths, isSuperstackProject, getProjectRoot } from '../../utils/paths.js';
import { exec } from 'child_process';
import { promisify } from 'util';
import { getConfig } from '../../utils/config.js';

const execAsync = promisify(exec);

export async function edit(): Promise<void> {
  // Check if current directory is a Superstack project
  if (!isSuperstackProject()) {
    log('Current directory is not a Superstack project.', 'error');
    log('Run this command from a Superstack project directory or create a new project with "dev new".', 'info');
    return;
  }
  
  section('Editing Project Context');
  
  const projectRoot = getProjectRoot();
  if (!projectRoot) {
    log('Unable to find project root.', 'error');
    return;
  }
  
  // Check if context exists
  const contextFilePath = path.join(projectRoot, '.superstack', 'context', 'project-context.md');
  
  if (!fs.existsSync(contextFilePath)) {
    log('Project context not found.', 'error');
    log('Initialize project context first with "dev context init".', 'info');
    return;
  }
  
  // Edit with default editor
  try {
    // Get preferred editor from config, fallback to environment variable, then to sensible defaults
    const editor = getConfig('editor') || process.env.EDITOR || process.env.VISUAL || 'code';
    
    await execAsync(`${editor} "${contextFilePath}"`, { stdio: 'inherit' } as any);
    log('Context file opened in editor.', 'success');
    log('After editing, use "dev context push" to update your AI assistants.', 'info');
  } catch (error) {
    log('Failed to open editor.', 'error');
    log(`You can manually edit the context file at: ${contextFilePath}`, 'info');
  }
}