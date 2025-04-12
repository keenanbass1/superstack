/**
 * Utility functions for managing project context
 */
export declare const contextUtils: {
    /**
     * Get the context file path for the current directory
     */
    getContextPath: (dir?: string) => string;
    /**
     * Check if a context file exists in the given directory
     */
    contextExists: (dir?: string) => Promise<boolean>;
    /**
     * Initialize a new context file in the given directory
     */
    initContext: (dir?: string, projectName?: string, overwrite?: boolean) => Promise<boolean>;
    /**
     * Read the context file from the given directory
     */
    readContext: (dir?: string) => Promise<string>;
    /**
     * Validate context against schema
     * Returns array of unfilled placeholders or empty array if all good
     */
    validateContext: (contextContent: string) => Promise<string[]>;
    /**
     * Push context to AI assistants
     * Currently a stub for future implementation
     */
    pushContext: (contextContent: string) => Promise<{
        [key: string]: boolean;
    }>;
};
