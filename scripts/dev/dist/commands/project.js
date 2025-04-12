import chalk from 'chalk';
import ora from 'ora';
import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';
import { getPaths } from '../utils/paths.js';
import { logger } from '../utils/logger.js';
// Get directory name
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
/**
 * List all projects
 */
async function listProjects(options) {
    const spinner = ora('Finding projects').start();
    try {
        const { projectsDir } = getPaths();
        // Check if directory exists
        if (!await fs.pathExists(projectsDir)) {
            spinner.fail(`Projects directory not found: ${projectsDir}`);
            return;
        }
        // List all directories in the projects directory
        const files = await fs.readdir(projectsDir);
        const projects = [];
        for (const file of files) {
            const projectPath = path.join(projectsDir, file);
            // Use fs.lstat instead which returns a Stats object without using the constructor
            const stats = await fs.lstat(projectPath);
            if (stats.isDirectory()) {
                // Check if it has a .superstack.json file to confirm it's a project
                const isSuperstackProject = await fs.pathExists(path.join(projectPath, '.superstack.json'));
                projects.push({
                    name: file,
                    path: projectPath,
                    isSuperstackProject
                });
            }
        }
        if (projects.length === 0) {
            spinner.info('No projects found');
            logger.command('dev new my-project', 'Create a new project');
            return;
        }
        spinner.succeed(`Found ${projects.length} projects`);
        // Output as JSON if requested
        if (options.json) {
            console.log(JSON.stringify(projects, null, 2));
            return;
        }
        // Display projects
        console.log(chalk.cyan('\nProjects:'));
        for (const project of projects) {
            console.log(`\n${chalk.green(project.name)}`);
            console.log(`  Path: ${project.path}`);
            if (project.isSuperstackProject) {
                console.log(`  ${chalk.yellow('[Superstack Project]')}`);
            }
        }
        // Suggest next steps
        logger.info('');
        logger.command('dev new [project-name]', 'Create a new project');
    }
    catch (error) {
        spinner.fail('Failed to list projects');
        logger.error('Error listing projects', error);
    }
}
export default function (program) {
    const projectCommand = program
        .command('project')
        .description('Manage projects');
    // List projects
    projectCommand
        .command('list')
        .description('List all projects')
        .option('-j, --json', 'Output as JSON', false)
        .action(listProjects);
    return projectCommand;
}
//# sourceMappingURL=project.js.map