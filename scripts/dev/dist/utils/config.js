import fs from 'fs-extra';
import path from 'path';
import { getPaths } from './paths.js';
// Default configuration
const defaultConfig = {
    version: '0.1.0',
    aiProviders: {
        claude: {
            model: 'claude-3-sonnet-20240229'
        },
        openai: {
            model: 'gpt-4o'
        }
    },
    editor: 'code',
    logFormat: 'markdown',
    defaultProjectTemplate: 'next'
};
/**
 * Get the Superstack config file path
 */
function getConfigPath() {
    const { configDir } = getPaths();
    fs.ensureDirSync(configDir);
    return path.join(configDir, 'config.json');
}
/**
 * Load the Superstack configuration
 */
export function loadConfig() {
    const configPath = getConfigPath();
    if (!fs.existsSync(configPath)) {
        // Initialize with default config
        saveConfigFile(defaultConfig);
        return defaultConfig;
    }
    try {
        const config = fs.readJSONSync(configPath);
        return { ...defaultConfig, ...config };
    }
    catch (error) {
        console.error('Error loading config:', error);
        return defaultConfig;
    }
}
/**
 * Helper function to write config directly to file without loading existing config
 */
function saveConfigFile(config) {
    const configPath = getConfigPath();
    try {
        fs.ensureFileSync(configPath);
        fs.writeJSONSync(configPath, config, { spaces: 2 });
    }
    catch (error) {
        console.error('Error saving config file:', error);
    }
}
/**
 * Save the Superstack configuration
 */
export function saveConfig(config) {
    const configPath = getConfigPath();
    // If the config file doesn't exist yet, just write the provided config
    if (!fs.existsSync(configPath)) {
        saveConfigFile({ ...defaultConfig, ...config });
        return;
    }
    // Otherwise, merge with existing config
    try {
        let currentConfig = defaultConfig;
        try {
            currentConfig = { ...defaultConfig, ...fs.readJSONSync(configPath) };
        }
        catch (e) {
            // If reading fails, use default config
        }
        const updatedConfig = { ...currentConfig, ...config };
        fs.ensureFileSync(configPath);
        fs.writeJSONSync(configPath, updatedConfig, { spaces: 2 });
    }
    catch (error) {
        console.error('Error saving config:', error);
    }
}
/**
 * Get a specific config value
 */
export function getConfig(key) {
    const config = loadConfig();
    return config[key];
}
/**
 * Set a specific config value
 */
export function setConfig(key, value) {
    const config = loadConfig();
    config[key] = value;
    saveConfig(config);
}
/**
 * Get the current version
 */
export function getVersion() {
    return loadConfig().version;
}
//# sourceMappingURL=config.js.map