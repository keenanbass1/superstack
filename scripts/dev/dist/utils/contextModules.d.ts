export interface ContextModule {
    path: string;
    title: string;
    description: string;
    domain: string;
    type: string;
}
export interface ActiveContext {
    modules: string[];
    timestamp: string;
    project?: string;
}
export interface ContextGroup {
    modules: string[];
    description?: string;
    created: string;
    updated: string;
}
export interface ContextGroups {
    [groupName: string]: ContextGroup;
}
/**
 * Get path to context module directory
 */
export declare function getContextModulesPath(): string;
/**
 * Get all available context modules
 */
export declare function getAllContextModules(): Promise<ContextModule[]>;
/**
 * Get active context
 */
export declare function getActiveContext(): Promise<ActiveContext>;
/**
 * Save active context
 */
export declare function saveActiveContext(context: ActiveContext): Promise<void>;
/**
 * Add modules to active context
 */
export declare function addModulesToActiveContext(modulePaths: string[]): Promise<void>;
/**
 * Remove modules from active context
 */
export declare function removeModulesFromActiveContext(modulePaths: string[]): Promise<void>;
/**
 * Clear all active context
 */
export declare function clearActiveContext(): Promise<void>;
/**
 * Get all context groups
 */
export declare function getContextGroups(): Promise<ContextGroups>;
/**
 * Create a new context group
 */
export declare function createContextGroup(name: string, modulePaths: string[], description?: string): Promise<void>;
/**
 * Delete a context group
 */
export declare function deleteContextGroup(name: string): Promise<boolean>;
/**
 * Add a context group to active context
 */
export declare function addGroupToActiveContext(groupName: string): Promise<boolean>;
/**
 * Get content of a context module
 */
export declare function getModuleContent(modulePath: string): Promise<string>;
/**
 * Get formatted content of all active context modules
 */
export declare function getFormattedActiveContext(): Promise<string>;
