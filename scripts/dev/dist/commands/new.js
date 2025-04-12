import chalk from 'chalk';
import inquirer from 'inquirer';
import fs from 'fs-extra';
import path from 'path';
import ora from 'ora';
import { execSync, spawn } from 'child_process';
// Import paths from the paths utility
import { getPaths } from '../utils/paths.js';
// Get paths
const { projectsDir: PROJECTS_DIR, templatesDir } = getPaths();
const TEMPLATES_DIR = path.join(templatesDir, 'project-types');
// Available project templates
const PROJECT_TEMPLATES = {
    'next-app': {
        description: 'Next.js application with TypeScript',
        generator: 'create-next-app',
        options: ['--typescript', '--eslint', '--tailwind', '--src-dir', '--app', '--import-alias="@/*"']
    },
    'api-service': {
        description: 'Express API service with TypeScript',
        generator: 'custom',
        source: 'api-service' // Source folder in templates/project-types
    },
    'cli-tool': {
        description: 'Command-line tool with TypeScript',
        generator: 'custom',
        source: 'cli-tool' // Source folder in templates/project-types
    }
};
/**
 * Run a command in a specific directory using Node's spawn
 * This avoids npm resolution issues by using direct execution
 */
function runCommand(command, args, cwd) {
    return new Promise((resolve, reject) => {
        const proc = spawn(command, args, {
            cwd,
            stdio: 'inherit',
            shell: true
        });
        proc.on('close', (code) => {
            if (code === 0) {
                resolve();
            }
            else {
                reject(new Error(`Command failed with exit code ${code}`));
            }
        });
        proc.on('error', (err) => {
            reject(err);
        });
    });
}
/**
 * Create a new project
 */
async function createProject(name, options) {
    // Ensure name is valid
    if (!name || !name.match(/^[a-z0-9-_]+$/i)) {
        console.error(chalk.red('Error: Project name must contain only letters, numbers, hyphens and underscores'));
        return;
    }
    const spinner = ora('Creating new project').start();
    try {
        // Determine project path
        const targetPath = options.path
            ? path.resolve(options.path, name)
            : path.join(PROJECTS_DIR, name);
        // Check if directory already exists
        if (await fs.pathExists(targetPath)) {
            spinner.fail(`Directory already exists: ${targetPath}`);
            return;
        }
        // Ensure parent directory exists
        await fs.ensureDir(path.dirname(targetPath));
        // If no template is specified, prompt for one
        let template = options.template;
        if (!template) {
            spinner.stop();
            const choices = Object.entries(PROJECT_TEMPLATES).map(([id, details]) => ({
                name: `${id} - ${details.description}`,
                value: id
            }));
            const response = await inquirer.prompt([
                {
                    type: 'list',
                    name: 'template',
                    message: 'Select a project template:',
                    choices
                }
            ]);
            template = response.template;
            spinner.start(`Creating new project using ${template} template`);
        }
        // Validate template
        if (!template || !PROJECT_TEMPLATES[template]) {
            spinner.fail(`Unknown template: ${template}`);
            console.log(`Available templates: ${Object.keys(PROJECT_TEMPLATES).join(', ')}`);
            return;
        }
        const templateConfig = PROJECT_TEMPLATES[template];
        // Create the project
        if (templateConfig.generator === 'custom') {
            // Copy from template directory
            if (!('source' in templateConfig)) {
                spinner.fail('Template configuration is missing source property');
                return;
            }
            const sourcePath = path.join(TEMPLATES_DIR, templateConfig.source);
            if (!await fs.pathExists(sourcePath)) {
                spinner.fail(`Template source not found: ${sourcePath}`);
                return;
            }
            spinner.text = 'Copying template files...';
            await fs.copy(sourcePath, targetPath);
            // Replace placeholders in package.json if it exists
            const packageJsonPath = path.join(targetPath, 'package.json');
            if (await fs.pathExists(packageJsonPath)) {
                spinner.text = 'Configuring package.json...';
                const packageJson = await fs.readJson(packageJsonPath);
                packageJson.name = name;
                await fs.writeJson(packageJsonPath, packageJson, { spaces: 2 });
            }
            // Initialize git repository
            spinner.text = 'Initializing git repository...';
            try {
                execSync('git init', { cwd: targetPath, stdio: 'ignore' });
            }
            catch (error) {
                spinner.warn('Failed to initialize git repository');
            }
        }
        else {
            // Use external generator
            spinner.text = `Running ${templateConfig.generator}...`;
            if (!('options' in templateConfig)) {
                spinner.fail('Template configuration is missing options property');
                return;
            }
            // Temporarily pause the spinner while the generator is running
            spinner.stop();
            try {
                // Run the generator directly in the projects directory
                await runCommand('npx', [
                    '--yes',
                    templateConfig.generator,
                    name,
                    ...templateConfig.options
                ], PROJECTS_DIR);
                // Restart the spinner
                spinner.start('Project created successfully');
            }
            catch (error) {
                spinner.fail(`Failed to run generator: ${templateConfig.generator}`);
                console.error(error);
                return;
            }
        }
        // Create .superstack.json file to mark it as a Superstack project
        await fs.writeJson(path.join(targetPath, '.superstack.json'), {
            name,
            template,
            created: new Date().toISOString()
        }, { spaces: 2 });
        spinner.succeed(`Project created successfully: ${chalk.green(name)}`);
        console.log('\nNext steps:');
        console.log(`  1. cd ${targetPath}`);
        console.log('  2. dev context init');
        console.log('  3. npm install (or yarn)');
        console.log('  4. npm run dev (or yarn dev)');
    }
    catch (error) {
        spinner.fail('Failed to create project');
        console.error(chalk.red('Error:'), error);
    }
}
export default function (program) {
    const newCommand = program
        .command('new')
        .description('Create a new project')
        .argument('<name>', 'Project name')
        .option('-t, --template <template>', 'Project template')
        .option('-p, --path <path>', 'Custom project location')
        .action(createProject);
    return newCommand;
}
//# sourceMappingURL=new.js.map