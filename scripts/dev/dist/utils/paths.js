import path from 'path';
import os from 'os';
import fs from 'fs-extra';
/**
 * Get system paths
 */
export function getPaths() {
    const homeDir = os.homedir();
    const devDir = path.join(homeDir, 'Desktop', 'dev'); // Adjusted for actual path structure
    const superstackDir = path.join(devDir, 'superstack');
    const currentDir = process.cwd();
    return {
        homeDir,
        devDir,
        superstackDir,
        configDir: path.join(superstackDir, 'config'),
        templatesDir: path.join(superstackDir, 'templates'),
        projectsDir: path.join(devDir, 'projects'),
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
export function getProjectTemplateDir(templateName) {
    const { templatesDir } = getPaths();
    return path.join(templatesDir, 'project-types', templateName);
}
/**
 * Check if current directory is a Superstack project
 */
export function isSuperstackProject(dir = process.cwd()) {
    return fs.existsSync(path.join(dir, '.superstack.json'));
}
/**
 * Get the project root directory
 * Traverses up the directory tree to find the project root
 */
export function getProjectRoot(startDir = process.cwd()) {
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
export function ensureSystemPaths() {
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
//# sourceMappingURL=paths.js.map