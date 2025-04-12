/**
 * Clipboard Manager
 * 
 * Cross-platform utilities for interacting with the system clipboard
 * in different environments (Windows, macOS, Linux, WSL).
 */

const { execSync } = require('child_process');
const os = require('os');
const fs = require('fs');
const path = require('path');

/**
 * Detect the current environment for clipboard operations
 * @returns {string} Environment identifier ('win', 'mac', 'linux', 'wsl')
 */
function detectEnvironment() {
  const platform = os.platform();
  
  if (platform === 'win32') {
    return 'win';
  } else if (platform === 'darwin') {
    return 'mac';
  } else if (platform === 'linux') {
    // Check if running in WSL
    try {
      const releaseInfo = fs.readFileSync('/proc/version', 'utf8').toLowerCase();
      if (releaseInfo.includes('microsoft') || releaseInfo.includes('wsl')) {
        return 'wsl';
      }
    } catch (error) {
      // Ignore error, assume regular Linux
    }
    
    return 'linux';
  }
  
  // Default fallback
  return 'unknown';
}

/**
 * Copy text to the system clipboard
 * @param {string} text The text to copy to clipboard
 * @returns {boolean} Success status
 */
function copyToClipboard(text) {
  if (!text) {
    console.error('No text provided for clipboard');
    return false;
  }
  
  const env = detectEnvironment();
  
  try {
    switch (env) {
      case 'win':
        // Using PowerShell to set clipboard in Windows
        const tempFile = path.join(os.tmpdir(), `clipboard-${Date.now()}.txt`);
        fs.writeFileSync(tempFile, text);
        execSync(`powershell -command "Get-Content -Path '${tempFile}' -Raw | Set-Clipboard"`, { windowsHide: true });
        fs.unlinkSync(tempFile);
        break;
        
      case 'wsl':
        // Using clip.exe in WSL
        const wslTempFile = path.join(os.tmpdir(), `clipboard-${Date.now()}.txt`);
        fs.writeFileSync(wslTempFile, text);
        execSync(`cat "${wslTempFile}" | clip.exe`, { shell: '/bin/bash' });
        fs.unlinkSync(wslTempFile);
        break;
        
      case 'mac':
        // Using pbcopy on macOS
        const proc = execSync('pbcopy', { input: text });
        break;
        
      case 'linux':
        // Try multiple Linux clipboard tools
        let success = false;
        
        // Try xclip first
        try {
          execSync('which xclip', { stdio: 'ignore' });
          execSync('xclip -selection clipboard', { input: text });
          success = true;
        } catch (e) {
          // xclip not available or failed
        }
        
        // Try wl-copy (Wayland)
        if (!success) {
          try {
            execSync('which wl-copy', { stdio: 'ignore' });
            execSync('wl-copy', { input: text });
            success = true;
          } catch (e) {
            // wl-copy not available or failed
          }
        }
        
        // Try xsel
        if (!success) {
          try {
            execSync('which xsel', { stdio: 'ignore' });
            execSync('xsel --clipboard --input', { input: text });
            success = true;
          } catch (e) {
            // xsel not available or failed
          }
        }
        
        if (!success) {
          console.error('No clipboard utility found. Install xclip, wl-copy, or xsel.');
          return false;
        }
        break;
        
      default:
        console.error(`Unsupported platform: ${env}`);
        return false;
    }
    
    console.log('Content copied to clipboard');
    return true;
  } catch (error) {
    console.error('Error copying to clipboard:', error.message);
    return false;
  }
}

/**
 * Read text from the system clipboard
 * @returns {string|null} Clipboard content or null if failed
 */
function readFromClipboard() {
  const env = detectEnvironment();
  
  try {
    switch (env) {
      case 'win':
        // PowerShell to get clipboard in Windows
        return execSync('powershell -command "Get-Clipboard -Raw"', { windowsHide: true }).toString().trim();
        
      case 'wsl':
        // PowerShell through WSL
        return execSync('powershell.exe -command "Get-Clipboard -Raw"', { shell: '/bin/bash' }).toString().trim();
        
      case 'mac':
        // Using pbpaste on macOS
        return execSync('pbpaste').toString().trim();
        
      case 'linux':
        // Try multiple Linux clipboard tools
        
        // Try xclip first
        try {
          execSync('which xclip', { stdio: 'ignore' });
          return execSync('xclip -selection clipboard -o').toString().trim();
        } catch (e) {
          // xclip not available or failed
        }
        
        // Try wl-paste (Wayland)
        try {
          execSync('which wl-paste', { stdio: 'ignore' });
          return execSync('wl-paste').toString().trim();
        } catch (e) {
          // wl-paste not available or failed
        }
        
        // Try xsel
        try {
          execSync('which xsel', { stdio: 'ignore' });
          return execSync('xsel --clipboard --output').toString().trim();
        } catch (e) {
          // xsel not available or failed
        }
        
        console.error('No clipboard utility found. Install xclip, wl-paste, or xsel.');
        return null;
        
      default:
        console.error(`Unsupported platform: ${env}`);
        return null;
    }
  } catch (error) {
    console.error('Error reading from clipboard:', error.message);
    return null;
  }
}

/**
 * Copy content to clipboard with metrics
 * @param {string} content Content to copy
 * @param {Object} options Additional options
 * @returns {Object} Operation result with metrics
 */
function copyWithMetrics(content, options = {}) {
  const { showTokenEstimate = true, showPreview = true, previewLength = 100 } = options;
  
  const startTime = Date.now();
  const success = copyToClipboard(content);
  const endTime = Date.now();
  
  const result = {
    success,
    characters: content ? content.length : 0,
    lines: content ? content.split('\n').length : 0,
    operationTime: endTime - startTime
  };
  
  // Add token estimate if requested
  if (showTokenEstimate && content) {
    result.tokenEstimate = Math.ceil(content.length / 4); // Simple approximation
  }
  
  // Add content preview if requested
  if (showPreview && content) {
    const preview = content.length > previewLength 
      ? content.substring(0, previewLength) + '...' 
      : content;
    
    result.preview = preview.replace(/\n/g, ' ').trim();
  }
  
  return result;
}

module.exports = {
  detectEnvironment,
  copyToClipboard,
  readFromClipboard,
  copyWithMetrics
};
