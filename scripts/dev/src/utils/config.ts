import fs from 'fs-extra';
import path from 'path';
import os from 'os';
import { getPaths } from './paths.js';

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

// Default configuration
const defaultConfig: SuperstackConfig = {
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
function getConfigPath(): string {
  const { configDir } = getPaths();
  fs.ensureDirSync(configDir);
  return path.join(configDir, 'config.json');
}

/**
 * Load the Superstack configuration
 */
export function loadConfig(): SuperstackConfig {
  const configPath = getConfigPath();
  
  if (!fs.existsSync(configPath)) {
    // Initialize with default config
    saveConfig(defaultConfig);
    return defaultConfig;
  }
  
  try {
    const config = fs.readJSONSync(configPath);
    return { ...defaultConfig, ...config };
  } catch (error) {
    console.error('Error loading config:', error);
    return defaultConfig;
  }
}

/**
 * Save the Superstack configuration
 */
export function saveConfig(config: Partial<SuperstackConfig>): void {
  const configPath = getConfigPath();
  const currentConfig = loadConfig();
  const updatedConfig = { ...currentConfig, ...config };
  
  try {
    fs.ensureFileSync(configPath);
    fs.writeJSONSync(configPath, updatedConfig, { spaces: 2 });
  } catch (error) {
    console.error('Error saving config:', error);
  }
}

/**
 * Get a specific config value
 */
export function getConfig<K extends keyof SuperstackConfig>(key: K): SuperstackConfig[K] {
  const config = loadConfig();
  return config[key];
}

/**
 * Set a specific config value
 */
export function setConfig<K extends keyof SuperstackConfig>(key: K, value: SuperstackConfig[K]): void {
  const config = loadConfig();
  config[key] = value;
  saveConfig(config);
}

/**
 * Get the current version
 */
export function getVersion(): string {
  return loadConfig().version;
}