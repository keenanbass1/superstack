interface SuperstackConfig {
    version: string;
    aiProviders: {
        claude?: {
            apiKey?: string;
            model?: string;
        };
        openai?: {
            apiKey?: string;
            model?: string;
        };
    };
    editor?: string;
    logFormat?: string;
    defaultProjectTemplate?: string;
}
/**
 * Load the Superstack configuration
 */
export declare function loadConfig(): SuperstackConfig;
/**
 * Save the Superstack configuration
 */
export declare function saveConfig(config: Partial<SuperstackConfig>): void;
/**
 * Get a specific config value
 */
export declare function getConfig<K extends keyof SuperstackConfig>(key: K): SuperstackConfig[K];
/**
 * Set a specific config value
 */
export declare function setConfig<K extends keyof SuperstackConfig>(key: K, value: SuperstackConfig[K]): void;
/**
 * Get the current version
 */
export declare function getVersion(): string;
export {};
