import fs from 'fs-extra';
import path from 'path';
import { log, section } from '../../utils/logger.js';
import { getPaths, isSuperstackProject, getProjectRoot } from '../../utils/paths.js';
import { exec } from 'child_process';
import { promisify } from 'util';
import inquirer from 'inquirer';
const execAsync = promisify(exec);
export async function init() {
    // Check if current directory is a Superstack project
    if (!isSuperstackProject()) {
        log('Current directory is not a Superstack project.', 'error');
        log('Run this command from a Superstack project directory or create a new project with "dev new".', 'info');
        return;
    }
    section('Initializing Project Context');
    const projectRoot = getProjectRoot();
    if (!projectRoot) {
        log('Unable to find project root.', 'error');
        return;
    }
    // Create context directory
    const contextDir = path.join(projectRoot, '.superstack', 'context');
    fs.ensureDirSync(contextDir);
    // Check if context already exists
    const contextFilePath = path.join(contextDir, 'project-context.md');
    if (fs.existsSync(contextFilePath)) {
        const { overwrite } = await inquirer.prompt([{
                type: 'confirm',
                name: 'overwrite',
                message: 'Project context already exists. Overwrite?',
                default: false
            }]);
        if (!overwrite) {
            log('Context initialization canceled.', 'warning');
            return;
        }
    }
    // Get project name and details from package.json or .superstack.json
    let projectName = '';
    let projectDescription = '';
    const packageJsonPath = path.join(projectRoot, 'package.json');
    const superstackJsonPath = path.join(projectRoot, '.superstack.json');
    if (fs.existsSync(packageJsonPath)) {
        const packageJson = fs.readJSONSync(packageJsonPath);
        projectName = packageJson.name || '';
        projectDescription = packageJson.description || '';
    }
    if (fs.existsSync(superstackJsonPath)) {
        const superstackJson = fs.readJSONSync(superstackJsonPath);
        if (!projectName)
            projectName = superstackJson.name || '';
    }
    if (!projectName) {
        projectName = path.basename(projectRoot);
    }
    // Get template from templates directory
    const { templatesDir } = getPaths();
    const contextTemplatePath = path.join(templatesDir, 'project-context.md');
    if (!fs.existsSync(contextTemplatePath)) {
        log('Context template not found.', 'error');
        return;
    }
    // Read template and customize it
    let contextContent = fs.readFileSync(contextTemplatePath, 'utf8');
    // Get project stack from package.json dependencies
    let dependencies = '';
    if (fs.existsSync(packageJsonPath)) {
        const packageJson = fs.readJSONSync(packageJsonPath);
        const deps = { ...packageJson.dependencies, ...packageJson.devDependencies };
        dependencies = Object.entries(deps)
            .map(([name, version]) => `- ${name}: ${version}`)
            .join('\n');
    }
    // Get git info if available
    let gitInfo = '';
    try {
        const gitBranch = await execAsync('git branch --show-current', {
            cwd: projectRoot
        }).then(result => result.stdout.trim());
        const gitRemote = await execAsync('git remote -v', {
            cwd: projectRoot
        }).then(result => result.stdout.trim());
        gitInfo = `- Current branch: ${gitBranch}\n- Remote: ${gitRemote.split('\n')[0]}`;
    }
    catch (error) {
        gitInfo = '- No git repository found or git is not installed';
    }
    // Replace placeholders
    contextContent = contextContent
        .replace(/\{\{PROJECT_NAME\}\}/g, projectName)
        .replace(/\{\{PROJECT_DESCRIPTION\}\}/g, projectDescription || `${projectName} project`)
        .replace(/\{\{DEPENDENCIES\}\}/g, dependencies || 'No dependencies found')
        .replace(/\{\{GIT_INFO\}\}/g, gitInfo)
        .replace(/\{\{CREATION_DATE\}\}/g, new Date().toISOString().split('T')[0]);
    // Allow user to provide additional information
    const { additionalInfo } = await inquirer.prompt([{
            type: 'editor',
            name: 'additionalInfo',
            message: 'Add any additional project context (optional):',
            default: ''
        }]);
    if (additionalInfo.trim()) {
        contextContent = contextContent.replace(/\{\{ADDITIONAL_INFO\}\}/g, additionalInfo.trim());
    }
    else {
        contextContent = contextContent.replace(/\{\{ADDITIONAL_INFO\}\}/g, 'No additional information provided');
    }
    // Write context file
    fs.writeFileSync(contextFilePath, contextContent, 'utf8');
    log('Project context initialized successfully.', 'success');
    log(`Context file created at: ${contextFilePath}`, 'info');
    log('Edit this file to add more specific information about your project.', 'info');
    log('Then use "dev context push" to share it with AI assistants.', 'info');
}
//# sourceMappingURL=init.js.map