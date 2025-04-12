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
 * Get system paths
 */
export declare function getPaths(): SystemPaths;
/**
 * Get project templates directory
 */
export declare function getProjectTemplateDir(templateName: string): string;
/**
 * Check if current directory is a Superstack project
 */
export declare function isSuperstackProject(dir?: string): boolean;
/**
 * Get the project root directory
 * Traverses up the directory tree to find the project root
 */
export declare function getProjectRoot(startDir?: string): string | null;
/**
 * Ensure all system paths exist
 */
export declare function ensureSystemPaths(): void;
export {};
