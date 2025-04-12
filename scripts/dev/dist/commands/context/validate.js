import fs from 'fs-extra';
import path from 'path';
import { log, section } from '../../utils/logger.js';
import { getPaths, isSuperstackProject, getProjectRoot } from '../../utils/paths.js';
import Ajv from 'ajv';
export async function validate() {
    // Check if current directory is a Superstack project
    if (!isSuperstackProject()) {
        log('Current directory is not a Superstack project.', 'error');
        log('Run this command from a Superstack project directory or create a new project with "dev new".', 'info');
        return;
    }
    section('Validating Project Context');
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
    // Get schema
    const { schemasDir } = getPaths();
    const schemaPath = path.join(schemasDir, 'context-schema.json');
    if (!fs.existsSync(schemaPath)) {
        log('Context schema not found.', 'error');
        log(`Expected schema at: ${schemaPath}`, 'info');
        return;
    }
    // Read schema and context
    const schema = fs.readJSONSync(schemaPath);
    const contextContent = fs.readFileSync(contextFilePath, 'utf8');
    // Convert Markdown to JSON for validation
    try {
        // This is a simplified conversion process
        const contextJson = convertMarkdownToJson(contextContent);
        // Validate JSON against schema
        const ajv = new Ajv();
        const validate = ajv.compile(schema);
        const valid = validate(contextJson);
        if (valid) {
            log('Project context is valid.', 'success');
        }
        else {
            log('Project context validation failed.', 'error');
            console.log(validate.errors);
        }
    }
    catch (error) {
        log('Failed to parse context for validation.', 'error');
        console.error(error);
    }
}
/**
 * Simple conversion of markdown to JSON structure
 */
function convertMarkdownToJson(markdown) {
    const sections = {};
    let currentSection = '';
    const lines = markdown.split('\n');
    for (const line of lines) {
        if (line.startsWith('# ')) {
            // Main title, can be skipped
            continue;
        }
        else if (line.startsWith('## ')) {
            currentSection = line.substring(3).trim();
            sections[currentSection] = {};
        }
        else if (line.startsWith('### ') && currentSection) {
            const subsection = line.substring(4).trim();
            sections[currentSection][subsection] = '';
        }
        else if (line.startsWith('- ') && currentSection) {
            // Handle list items
            const content = line.substring(2).trim();
            const parts = content.split(':');
            if (parts.length >= 2) {
                const key = parts[0].trim();
                const value = parts.slice(1).join(':').trim();
                if (!sections[currentSection].items) {
                    sections[currentSection].items = {};
                }
                sections[currentSection].items[key] = value;
            }
        }
        else if (line.trim() && currentSection) {
            // Add content to current section
            if (!sections[currentSection].content) {
                sections[currentSection].content = '';
            }
            sections[currentSection].content += line + '\n';
        }
    }
    return sections;
}
//# sourceMappingURL=validate.js.map