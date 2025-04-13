# Electron

> A framework for building cross-platform desktop applications using web technologies (HTML, CSS, and JavaScript).

## Metadata
- **Priority:** high
- **Domain:** development
- **Target Models:** claude, gpt, cursor-ai
- **Related Modules:** web-development, node-js, desktop-applications, security

## Module Overview
This module provides comprehensive guidance on developing desktop applications with Electron, including architecture patterns, security best practices, and performance optimization techniques.

<context name="electron_definition" priority="high">
## Conceptual Foundation

Electron is an open-source framework developed by GitHub (now part of Microsoft) that enables developers to build cross-platform desktop applications using web technologies. It combines:

1. **Chromium** - For rendering web content (the same engine that powers Google Chrome)
2. **Node.js** - For accessing the filesystem and operating system APIs
3. **Native APIs** - For OS-level integration

Through this combination, Electron allows developers to:
- Write once and deploy across Windows, macOS, and Linux
- Use familiar web technologies (HTML, CSS, JavaScript) for UI development
- Access both web APIs and Node.js modules in the same application
- Integrate with native OS features through Electron's APIs

Electron powers many popular desktop applications including Visual Studio Code, Slack, Discord, WhatsApp Desktop, Skype, and many others.
</context>

<context name="electron_process_model" priority="high">
## Process Model and Architecture

### Multi-Process Architecture

Electron inherits Chromium's multi-process architecture, which provides stability and security. Every Electron application consists of:

1. **Main Process:**
   - Entry point to the application (defined in the package.json's "main" field)
   - Controls application lifecycle (start, quit, etc.)
   - Creates and manages application windows via `BrowserWindow`
   - Can access native OS APIs
   - Has full Node.js integration
   - Only one main process exists per application

2. **Renderer Processes:**
   - Each application window (or `BrowserWindow` instance) runs in its own renderer process
   - Renders web content using Chromium
   - Can be configured to have Node.js integration (disabled by default for security)
   - Multiple renderer processes can exist simultaneously
   - Process isolation helps contain crashes to individual windows

3. **Utility Processes:**
   - Optional additional processes for CPU-intensive tasks
   - Created using the `UtilityProcess` API
   - Helps improve application stability and organization

### Process Communication

Since Electron uses multiple processes, communication between them is essential:

1. **IPC (Inter-Process Communication):**
   - `ipcMain` module in the main process
   - `ipcRenderer` module in renderer processes
   - Asynchronous messaging: `ipcRenderer.send()` and `ipcMain.on()`
   - Request-response pattern: `ipcRenderer.invoke()` and `ipcMain.handle()`
   - Synchronous messaging: `ipcRenderer.sendSync()` (avoid when possible as it blocks the UI)

2. **Context Bridges:**
   - `contextBridge` module for safely exposing APIs from preload scripts to renderers
   - Helps maintain security boundary between Node.js and web content

3. **Remote Module (Deprecated):**
   - Previously allowed direct access to main process modules from renderers
   - Removed for security reasons in newer Electron versions

### Preload Scripts

Preload scripts execute in a renderer process before web content begins loading:
- Have access to both Node.js APIs and DOM APIs
- Run in an "isolated world" separate from the main renderer context
- Used to safely expose custom APIs to renderer processes via `contextBridge`
- Loaded via the `webPreferences.preload` option when creating a `BrowserWindow`

```javascript
// main.js
const win = new BrowserWindow({
  webPreferences: {
    preload: path.join(__dirname, 'preload.js'),
    contextIsolation: true,
    nodeIntegration: false
  ## Using This Module

This Electron context module can be referenced when:
- Starting a new Electron project from scratch
- Evaluating security practices in existing Electron applications
- Planning IPC communication between processes
- Implementing cross-platform desktop features
- Debugging process communication issues
- Optimizing application performance
- Creating proper window management systems

The core concepts to focus on when developing Electron applications are:
1. Process separation and appropriate responsibility allocation
2. Secure communication between processes
3. Protection against common security vulnerabilities
4. Platform-specific adaptations for native feel
5. Efficient application lifecycle management

Remember that Electron combines web technologies with native capabilities, providing both flexibility and power. However, this combination also creates unique security challenges that must be addressed through proper architecture and best practices.

Last Updated: April 13, 2025
});

// preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  sendMessage: (message) => ipcRenderer.send('message', message),
  onResponse: (callback) => ipcRenderer.on('response', callback)
});
```
</context>

<context name="electron_core_principles" priority="high">
## Core Principles

### 1. Web + Native Integration

**Principle:** Electron combines web technologies with native capabilities, allowing developers to leverage both ecosystems.

**Implementation Guidelines:**
- Use web technologies (HTML, CSS, JavaScript) for UI development
- Use Node.js APIs for file system access, networking, and other system functions
- Use Electron's native APIs for OS integration (notifications, menus, dialogs)
- Follow platform-specific UI/UX patterns where appropriate

**Example:**
```javascript
// Combining web UI with native dialog
document.getElementById('save-button').addEventListener('click', async () => {
  // Web API to get content
  const content = document.getElementById('editor').value;
  
  // Electron native dialog API
  const { filePath } = await window.electronAPI.showSaveDialog({
    title: 'Save document',
    filters: [{ name: 'Text Files', extensions: ['txt'] }]
  });
  
  if (filePath) {
    // Node.js API to write file
    await window.electronAPI.writeFile(filePath, content);
  }
});
```

### Native Integration Example

Integrating with native OS features:

**main.js (partial):**
```javascript
const { app, BrowserWindow, dialog, Menu, Tray, nativeTheme, shell, powerMonitor } = require('electron');

// Create system tray
function createTray() {
  const tray = new Tray(path.join(__dirname, 'assets', 'icons', 'tray.png'));
  const contextMenu = Menu.buildFromTemplate([
    { label: 'Open', click: () => mainWindow.show() },
    { type: 'separator' },
    { label: 'Settings', click: () => openSettings() },
    { type: 'separator' },
    { label: 'Quit', role: 'quit' }
  ]);
  
  tray.setToolTip('My Electron App');
  tray.setContextMenu(contextMenu);
  
  return tray;
}

// Native file dialog example
async function showOpenDialog() {
  const { canceled, filePaths } = await dialog.showOpenDialog({
    title: 'Select a file',
    filters: [
      { name: 'Text Files', extensions: ['txt', 'md'] },
      { name: 'All Files', extensions: ['*'] }
    ],
    properties: ['openFile']
  });
  
  if (!canceled && filePaths.length > 0) {
    return filePaths[0];
  }
  
  return null;
}

// Native theme handling
function setupNativeTheme() {
  // Listen for theme changes
  nativeTheme.on('updated', () => {
    const isDark = nativeTheme.shouldUseDarkColors;
    broadcastThemeChange(isDark);
  });
  
  // Allow renderer to request theme
  ipcMain.handle('get-native-theme', () => {
    return {
      shouldUseDarkColors: nativeTheme.shouldUseDarkColors,
      shouldUseHighContrastColors: nativeTheme.shouldUseHighContrastColors,
      shouldUseInvertedColorScheme: nativeTheme.shouldUseInvertedColorScheme
    };
  });
  
  // Allow renderer to set theme
  ipcMain.handle('set-native-theme', (event, themeName) => {
    if (['light', 'dark', 'system'].includes(themeName)) {
      nativeTheme.themeSource = themeName;
      return true;
    }
    return false;
  });
}

// Power monitor example
function setupPowerMonitor() {
  powerMonitor.on('suspend', () => {
    // Save application state
    saveAppState();
  });
  
  powerMonitor.on('resume', () => {
    // Refresh data that might be stale
    refreshAppData();
  });
  
  powerMonitor.on('on-battery', () => {
    // Switch to power saving mode
    enablePowerSaving();
  });
  
  powerMonitor.on('on-ac', () => {
    // Switch to normal mode
    disablePowerSaving();
  });
}

// Open external links
function openExternalLink(url) {
  // Validate URL to prevent security issues
  if (url.startsWith('https://') || url.startsWith('http://')) {
    shell.openExternal(url);
  }
}
```

</context>

<context name="electron_reasoning_principles" priority="low">
## Reasoning Principles

### Security-First Approach

Electron combines web technologies with powerful native capabilities, creating a unique security environment that differs from both web browsers and traditional desktop applications. The core security reasoning principles are:

1. **Principle of Least Privilege**
   - Only expose APIs and capabilities that are absolutely necessary
   - Use context isolation and preload scripts to create secure bridges
   - Each component should have only the permissions it needs

2. **Defense in Depth**
   - Multiple security layers provide better protection
   - Process separation creates natural security boundaries
   - Context isolation prevents privilege escalation

3. **Trust Boundaries**
   - Remote content should never be trusted with system access
   - User-provided content requires validation and sanitization
   - Even local content should follow a secure architecture

These principles lead to specific implementation decisions:
- Node.js integration is disabled by default in renderer processes
- Context isolation creates a separate JavaScript world for preload scripts
- IPC is the recommended way to communicate between processes

### Performance Optimization

Performance in Electron applications is governed by these principles:

1. **Process Appropriateness**
   - UI operations belong in renderer processes
   - Heavy computation belongs in the main process or utility processes
   - Background tasks should not block the UI

2. **Resource Management**
   - Memory usage grows with each BrowserWindow
   - Chromium and Node.js both consume significant resources
   - Unused windows should be closed or hidden

3. **Startup Optimization**
   - Defer non-essential tasks until after app is visible
   - Use lazy loading for features not needed immediately
   - Consider showing a splash screen for perceived performance

### Cross-Platform Consistency

Creating a consistent experience across platforms involves:

1. **Platform Adaptation**
   - Respect platform conventions (menus, shortcuts, UI patterns)
   - Use conditional code for platform-specific features
   - Test thoroughly on all target platforms

2. **Graceful Degradation**
   - Features unavailable on some platforms should gracefully fall back
   - Core functionality should work everywhere
   - Platform-specific enhancements should be optional

3. **Interface Guidelines**
   - Follow each platform's interface guidelines where appropriate
   - Maintain consistent internal application logic
   - Create a cohesive experience that feels native everywhere

### Update and Distribution Strategy

For application updates and distribution:

1. **Seamless Updates**
   - Automatic updates improve security and user experience
   - Background downloading minimizes disruption
   - Staged rollouts mitigate risk

2. **Distribution Channels**
   - App stores provide visibility but have restrictions
   - Direct distribution offers more control but requires code signing
   - Web-based distribution must consider download size and experience

3. **Platform-Specific Packaging**
   - Each platform has different installation conventions
   - Package formats vary (DMG/PKG for macOS, MSI/NSIS for Windows, various for Linux)
   - Signing requirements differ by platform
</context>

<context name="electron_model_specific_notes" priority="low">
## Model-Specific Implementation Notes

### For Claude (Anthropic)

When working with Electron through Claude, consider these approaches:

- Claude excels at understanding complex architecture explanations, so focus on clearly describing the relationships between components
- Provide specific code patterns rather than expecting Claude to write complete Electron applications
- Use visual aids like process diagrams or flow charts to explain IPC communication or the process model
- Claude understands security concerns well, so explicitly highlight security implications when requesting code

Example prompt:
```
Explain how I should structure the IPC communication in my Electron app 
that has a main window and multiple child windows, ensuring secure 
data transfer between processes while avoiding race conditions.
```

### For GPT (OpenAI)

When working with Electron through GPT models, consider:

- GPT models often generate more complete code solutions for Electron apps
- Specify version numbers explicitly, as GPT might reference outdated or future APIs
- Use step-by-step guidance when requesting implementation help
- Be explicit about security requirements, as GPT might optimize for convenience over security
- Verify code for security issues, especially around Node.js integration and remote content loading

Example prompt:
```
I need to create an Electron app using version 25.0.0 that securely loads 
local content with a preload script, and implements secure IPC communication 
for file operations. Please show me the main.js, preload.js, and renderer code, 
highlighting security best practices.
```

### For Cursor AI

When working with Electron through Cursor AI, consider:

- Cursor AI is optimized for code-focused interactions
- Provide context about your existing project structure
- Ask for specific code completion or modifications
- Use comments to guide the model toward your specific needs
- Request explanations for complex patterns like IPC communication

Example prompt:
```
// I'm building an Electron app with the following structure:
// - main.js - Main process entry point
// - preload.js - Preload script for IPC
// - src/renderer - Renderer code

// I need to implement a secure way to handle the following:
// 1. Save user preferences
// 2. Perform file operations
// 3. Update the UI based on background process events

// Please help me implement this with proper IPC handling and security
```

### For Local Models

When working with Electron through local code models:

- Smaller models may not fully understand the security implications of Electron
- Break down requests into smaller, focused parts
- Provide more context about Electron's architecture
- Verify security aspects carefully
- Focus on simpler patterns first

Example prompt:
```
I need help with Electron IPC between main and renderer processes.
Specifically, I want to:
1. Send a message from renderer to main
2. Process data in the main process
3. Send a response back to the renderer

Please show me code for each part separately.
```
</context>

<context name="electron_related_concepts" priority="low">
## Related Concepts

- **Node.js** - The JavaScript runtime that powers Electron's main process, providing system access capabilities.

- **Chromium** - The open-source browser engine that powers Electron's renderer processes, providing modern web standards support.

- **V8** - The JavaScript engine that powers both Node.js and Chromium, interpreting JavaScript into machine code.

- **Desktop UI Frameworks** - UI libraries like React, Vue, Angular, etc., that can be used within Electron's renderer process.

- **Inter-Process Communication (IPC)** - The mechanism used for communication between Electron's main and renderer processes.

- **Context Isolation** - Security feature that isolates preload scripts from renderer content to prevent privilege escalation.

- **Content Security Policy (CSP)** - Web security standard that helps prevent various attacks like XSS.

- **Progressive Web Apps (PWAs)** - An alternative to Electron for some use cases, offering web apps with limited native capabilities.

- **Web Workers** - Background threads for web content that can be used in Electron's renderer processes for performance optimization.

- **Native Modules** - C/C++ modules that can be used with Node.js in Electron to access system capabilities or improve performance.

- **App Distribution** - Process of packaging and distributing desktop applications, including code signing and update mechanisms.

- **Code Signing** - Process of digitally signing applications to verify the publisher's identity and ensure the code hasn't been tampered with.

- **Auto-Updates** - Mechanisms for automatically updating applications with new versions.

- **Cross-Platform Development** - Practices for developing applications that work consistently across multiple operating systems.
</context>

<context name="electron_practical_examples" priority="medium">
## Practical Examples

### Example 1: Secure File Access

**Before**: Insecure implementation with direct Node.js access in renderer.

```javascript
// main.js
const win = new BrowserWindow({
  webPreferences: {
    nodeIntegration: true,
    contextIsolation: false
  }
});

// renderer.js
const fs = require('fs');

document.getElementById('save-button').addEventListener('click', () => {
  const content = document.getElementById('editor').value;
  fs.writeFileSync('/path/to/file.txt', content);
});
```

**After**: Secure implementation with proper IPC handling.

```javascript
// main.js
const win = new BrowserWindow({
  webPreferences: {
    preload: path.join(__dirname, 'preload.js'),
    contextIsolation: true,
    nodeIntegration: false
  }
});

ipcMain.handle('save-file', async (event, { path, content }) => {
  // Validate path to prevent directory traversal
  const safePath = validateAndSanitizePath(path);
  if (!safePath) {
    throw new Error('Invalid file path');
  }
  
  try {
    await fs.promises.writeFile(safePath, content);
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('fileApi', {
  saveFile: (path, content) => ipcRenderer.invoke('save-file', { path, content })
});

// renderer.js
document.getElementById('save-button').addEventListener('click', async () => {
  const content = document.getElementById('editor').value;
  try {
    const result = await window.fileApi.saveFile('/path/to/file.txt', content);
    if (result.success) {
      showSuccess('File saved successfully');
    } else {
      showError(`Failed to save file: ${result.error}`);
    }
  } catch (error) {
    showError('Failed to communicate with main process');
  }
});
```

Key improvements:
- Disabled Node.js integration in renderer
- Enabled context isolation
- Used preload script with contextBridge
- Implemented proper error handling
- Added path validation in main process
- Provided feedback to the user

### Example 2: Window Management

**Before**: Poor window management with potential memory leaks.

```javascript
// Opening new windows without tracking them
function openSettingsWindow() {
  const settingsWindow = new BrowserWindow({
    width: 600,
    height: 400,
    title: 'Settings'
  });
  
  settingsWindow.loadFile('settings.html');
  
  // No reference kept, window not properly managed
}

document.getElementById('settings-button').addEventListener('click', () => {
  openSettingsWindow();
});
```

**After**: Proper window management with references and cleanup.

```javascript
// main.js
const windowManager = {
  windows: new Map(),
  
  create(id, options, contentPath) {
    // If window already exists, focus it instead of creating a new one
    if (this.windows.has(id)) {
      const existingWindow = this.windows.get(id);
      if (existingWindow.isMinimized()) {
        existingWindow.restore();
      }
      existingWindow.focus();
      return existingWindow;
    }
    
    // Create new window with defaults merged with options
    const defaultOptions = {
      width: 800,
      height: 600,
      webPreferences: {
        preload: path.join(__dirname, 'preload.js'),
        contextIsolation: true,
        nodeIntegration: false
      }
    };
    
    const win = new BrowserWindow({
      ...defaultOptions,
      ...options
    });
    
    // Load content
    if (contentPath.startsWith('http')) {
      win.loadURL(contentPath);
    } else {
      win.loadFile(contentPath);
    }
    
    // Store reference and clean up on close
    this.windows.set(id, win);
    
    win.on('closed', () => {
      this.windows.delete(id);
    });
    
    return win;
  },
  
  get(id) {
    return this.windows.get(id);
  },
  
  close(id) {
    if (this.windows.has(id)) {
      this.windows.get(id).close();
      return true;
    }
    return false;
  }
};

// Handle IPC for window management
ipcMain.handle('open-window', (event, { id, options, contentPath }) => {
  windowManager.create(id, options, contentPath);
  return true;
});

// preload.js
contextBridge.exposeInMainWorld('windowApi', {
  openWindow: (id, options, contentPath) => 
    ipcRenderer.invoke('open-window', { id, options, contentPath })
});

// renderer.js
document.getElementById('settings-button').addEventListener('click', async () => {
  await window.windowApi.openWindow('settings', 
    { 
      width: 600, 
      height: 400,
      title: 'Settings',
      parent: window // Make it a child window
    }, 
    'settings.html'
  );
});
```

Key improvements:
- Centralized window management
- Prevention of duplicate windows
- Proper reference tracking to prevent memory leaks
- Cleanup on window close
- Consistent window creation pattern
- Parent/child window relationships

### Example 3: Theme Switching

**Before**: Theme implementation that doesn't respect OS settings.

```javascript
// Hard-coded theme without OS integration
let isDarkMode = false;

function toggleTheme() {
  isDarkMode = !isDarkMode;
  document.body.classList.toggle('dark-theme', isDarkMode);
}

document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
```

**After**: Theme implementation that respects OS preferences with Electron.

```javascript
// main.js
const { nativeTheme } = require('electron');

// Listen for native theme changes
nativeTheme.on('updated', () => {
  broadcastThemeChange();
});

// Handle theme-related IPC
ipcMain.handle('get-theme-source', () => {
  return nativeTheme.themeSource;
});

ipcMain.handle('get-should-use-dark-colors', () => {
  return nativeTheme.shouldUseDarkColors;
});

ipcMain.handle('set-theme-source', (event, source) => {
  if (['system', 'light', 'dark'].includes(source)) {
    nativeTheme.themeSource = source;
    return true;
  }
  return false;
});

// Broadcast theme changes to all windows
function broadcastThemeChange() {
  BrowserWindow.getAllWindows().forEach(window => {
    if (!window.isDestroyed()) {
      window.webContents.send('theme-updated', {
        shouldUseDarkColors: nativeTheme.shouldUseDarkColors,
        themeSource: nativeTheme.themeSource
      });
    }
  });
}

// preload.js
contextBridge.exposeInMainWorld('themeApi', {
  getThemeSource: () => ipcRenderer.invoke('get-theme-source'),
  getShouldUseDarkColors: () => ipcRenderer.invoke('get-should-use-dark-colors'),
  setThemeSource: (source) => ipcRenderer.invoke('set-theme-source', source),
  onThemeUpdated: (callback) => {
    // Wrap callback to avoid exposing event object
    const themeUpdateListener = (event, themeInfo) => callback(themeInfo);
    ipcRenderer.on('theme-updated', themeUpdateListener);
    
    // Return cleanup function
    return () => {
      ipcRenderer.removeListener('theme-updated', themeUpdateListener);
    };
  }
});

// renderer.js
// Initialize theme
async function initTheme() {
  const themeSource = await window.themeApi.getThemeSource();
  const isDark = await window.themeApi.getShouldUseDarkColors();
  
  updateThemeUI(themeSource, isDark);
  
  // Set up theme change listener
  window.themeApi.onThemeUpdated(({ themeSource, shouldUseDarkColors }) => {
    updateThemeUI(themeSource, shouldUseDarkColors);
  });
  
  // Set up theme toggle buttons
  document.getElementById('theme-system').addEventListener('click', () => {
    window.themeApi.setThemeSource('system');
  });
  
  document.getElementById('theme-light').addEventListener('click', () => {
    window.themeApi.setThemeSource('light');
  });
  
  document.getElementById('theme-dark').addEventListener('click', () => {
    window.themeApi.setThemeSource('dark');
  });
}

// Update UI based on theme
function updateThemeUI(themeSource, isDark) {
  // Update body class
  document.body.classList.toggle('dark-theme', isDark);
  
  // Update active theme button
  document.querySelectorAll('.theme-button').forEach(button => {
    button.classList.toggle('active', button.dataset.theme === themeSource);
  });
  
  // Update theme-specific elements
  document.querySelectorAll('[data-theme-mode]').forEach(element => {
    const showIn = element.dataset.themeMode;
    element.style.display = 
      (showIn === 'both' || 
      (showIn === 'dark' && isDark) || 
      (showIn === 'light' && !isDark)) ? 'block' : 'none';
  });
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', initTheme);
```

Key improvements:
- Integration with OS theme preferences
- Real-time updates when system theme changes
- Multiple theme options (system, light, dark)
- Proper IPC communication pattern
- Clean event listener management
- Responsive UI updates



### 2. Process Separation

**Principle:** Maintain clear separation between main and renderer processes for security and stability.

**Implementation Guidelines:**
- Keep process-specific code in appropriate files/modules
- Use IPC for communication between processes
- Keep UI logic in renderer processes
- Keep system-level operations in the main process
- Use preload scripts to expose only necessary APIs to renderers

**Example:**
```javascript
// main.js (main process)
ipcMain.handle('read-file', async (event, filePath) => {
  try {
    return await fs.promises.readFile(filePath, 'utf8');
  } catch (error) {
    return { error: error.message };
  }
});

// preload.js
contextBridge.exposeInMainWorld('fileAPI', {
  readFile: (path) => ipcRenderer.invoke('read-file', path)
});

// renderer.js (renderer process)
async function openFile(path) {
  const content = await window.fileAPI.readFile(path);
  document.getElementById('content').textContent = content;
}
```

### 3. Security-First Design

**Principle:** Prioritize security at all stages of application development.

**Implementation Guidelines:**
- Disable Node.js integration in renderer processes
- Enable context isolation
- Sanitize all user inputs
- Validate IPC messages
- Load remote content in sandboxed processes
- Apply Content Security Policy (CSP)
- Use HTTPS for remote resources

**Example:**
```javascript
// Secure BrowserWindow configuration
const win = new BrowserWindow({
  webPreferences: {
    preload: path.join(__dirname, 'preload.js'),
    contextIsolation: true,
    nodeIntegration: false,
    sandbox: true,
    webSecurity: true
  }
});

// Set CSP header
win.webContents.session.webRequest.onHeadersReceived((details, callback) => {
  callback({
    responseHeaders: {
      ...details.responseHeaders,
      'Content-Security-Policy': ["default-src 'self'"]
    }
  });
});
```

### 4. Platform Adaptability

**Principle:** Adapt to the platform the application is running on for a native-like experience.

**Implementation Guidelines:**
- Detect the platform using `process.platform`
- Use platform-specific behaviors and UI elements
- Support platform-specific features
- Adjust layouts for different operating systems
- Use responsive design principles

**Example:**
```javascript
// Adapt application menu based on platform
const template = [];

// Application menu (macOS only)
if (process.platform === 'darwin') {
  template.unshift({
    label: app.name,
    submenu: [
      { role: 'about' },
      { type: 'separator' },
      { role: 'services' },
      { type: 'separator' },
      { role: 'hide' },
      { role: 'hideOthers' },
      { role: 'unhide' },
      { type: 'separator' },
      { role: 'quit' }
    ]
  });
}

// Edit menu for all platforms
template.push({
  label: 'Edit',
  submenu: [
    { role: 'undo' },
    { role: 'redo' },
    { type: 'separator' },
    { role: 'cut' },
    { role: 'copy' },
    { role: 'paste' }
  ]
});

const menu = Menu.buildFromTemplate(template);
Menu.setApplicationMenu(menu);
```
</context>

<context name="electron_implementation_patterns" priority="medium">
## Implementation Patterns

### Application Lifecycle Management

A robust Electron application should properly handle its lifecycle events:

```javascript
const { app, BrowserWindow } = require('electron');
let mainWindow;

// Create the main application window
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  });

  mainWindow.loadFile('index.html');
  
  // Handle window being closed
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Initialize app when ready
app.whenReady().then(() => {
  createWindow();
  
  // On macOS, re-create window when dock icon is clicked
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

// Quit when all windows are closed, except on macOS
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
```

### Secure IPC Communication Pattern

For safe communication between processes:

```javascript
// main.js (main process)
const { app, BrowserWindow, ipcMain } = require('electron');

ipcMain.handle('perform-action', async (event, args) => {
  // Validate input
  if (!args || typeof args !== 'object' || !args.id) {
    throw new Error('Invalid arguments');
  }
  
  try {
    // Perform the action
    const result = await doSomething(args.id);
    return { success: true, data: result };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  performAction: (id) => ipcRenderer.invoke('perform-action', { id })
});

// renderer.js (renderer process)
async function handleButtonClick(id) {
  try {
    const result = await window.api.performAction(id);
    if (result.success) {
      displayData(result.data);
    } else {
      showError(result.error);
    }
  } catch (error) {
    showError('Failed to communicate with main process');
  }
}
```

### Data Persistence Pattern

For storing application data:

```javascript
// Using electron-store package
const Store = require('electron-store');

// Define schema for validation
const schema = {
  preferences: {
    type: 'object',
    properties: {
      theme: { type: 'string', enum: ['light', 'dark', 'system'] },
      fontSize: { type: 'number', minimum: 8, maximum: 32 }
    }
  },
  recentFiles: {
    type: 'array',
    maxItems: 10,
    items: { type: 'string' }
  }
};

// Create store instance
const store = new Store({ schema });

// Usage
function savePreferences(prefs) {
  store.set('preferences', prefs);
}

function getPreferences() {
  return store.get('preferences');
}

function addRecentFile(filePath) {
  let recent = store.get('recentFiles') || [];
  
  // Remove if already exists
  recent = recent.filter(path => path !== filePath);
  
  // Add to beginning
  recent.unshift(filePath);
  
  // Limit to 10 items
  if (recent.length > 10) {
    recent = recent.slice(0, 10);
  }
  
  store.set('recentFiles', recent);
}
```

### Auto-Update Pattern

For keeping applications updated:

```javascript
// Using electron-updater
const { autoUpdater } = require('electron-updater');
const { app, dialog } = require('electron');

// Configure logging
autoUpdater.logger = require('electron-log');
autoUpdater.logger.transports.file.level = 'info';

// Check for updates
function checkForUpdates() {
  autoUpdater.checkForUpdatesAndNotify();
}

// Update event handlers
autoUpdater.on('update-available', (info) => {
  dialog.showMessageBox({
    type: 'info',
    title: 'Update Available',
    message: `Version ${info.version} is available. Downloading now...`,
    buttons: ['OK']
  });
});

autoUpdater.on('update-downloaded', (info) => {
  dialog.showMessageBox({
    type: 'info',
    title: 'Update Ready',
    message: `Version ${info.version} has been downloaded. Restart to install?`,
    buttons: ['Restart', 'Later']
  }).then((result) => {
    if (result.response === 0) {
      autoUpdater.quitAndInstall();
    }
  });
});

// Check for updates on startup
app.whenReady().then(() => {
  // Wait a bit before checking for updates
  setTimeout(checkForUpdates, 3000);
});
```

### Multi-Window Management Pattern

For applications that need multiple windows:

```javascript
const { BrowserWindow, app } = require('electron');
const windowManager = {
  windows: new Map(),
  
  // Create a new window
  create(id, options, url) {
    if (this.windows.has(id)) {
      this.windows.get(id).focus();
      return this.windows.get(id);
    }
    
    const defaultOptions = {
      width: 800,
      height: 600,
      webPreferences: {
        preload: path.join(__dirname, 'preload.js'),
        contextIsolation: true,
        nodeIntegration: false
      }
    };
    
    const win = new BrowserWindow({
      ...defaultOptions,
      ...options
    });
    
    if (url.startsWith('http')) {
      win.loadURL(url);
    } else {
      win.loadFile(url);
    }
    
    win.on('closed', () => {
      this.windows.delete(id);
    });
    
    this.windows.set(id, win);
    return win;
  },
  
  // Get a window by id
  get(id) {
    return this.windows.get(id);
  },
  
  // Close a window by id
  close(id) {
    if (this.windows.has(id)) {
      this.windows.get(id).close();
      return true;
    }
    return false;
  },
  
  // Close all windows
  closeAll() {
    for (const win of this.windows.values()) {
      win.close();
    }
    this.windows.clear();
  }
};

// Usage example
app.whenReady().then(() => {
  // Main app window
  windowManager.create('main', { title: 'Main Window' }, 'index.html');
  
  // Settings window when needed
  ipcMain.on('open-settings', () => {
    windowManager.create('settings', 
      { 
        parent: windowManager.get('main'),
        modal: true,
        width: 500,
        height: 400
      }, 
      'settings.html'
    );
  });
});
```
</context>

<context name="electron_decision_logic" priority="medium">
## Decision Logic

### Choosing Between Main and Renderer Process

When deciding where to place functionality, follow these guidelines:

**Place in Main Process if:**
- It requires OS-level access (filesystem, native menus)
- It manages application lifecycle
- It handles window management
- It needs to be centralized for multiple windows
- It requires access to Node.js modules without restrictions
- It performs heavy calculations that shouldn't block the UI

**Place in Renderer Process if:**
- It's primarily UI-related
- It handles user interactions
- It manipulates the DOM
- It performs animations or visual updates
- It needs direct access to web APIs

### Node.js Integration Decision Tree

```
Does your renderer need to access Node.js APIs?
├── NO → Use default settings (nodeIntegration: false, contextIsolation: true)
└── YES → Is the content from a trusted source (local only)?
    ├── YES → Consider enabling Node.js integration (not recommended)
    └── NO → Use a preload script with contextBridge to expose only specific APIs
```

### Packaging Strategy Selection

```
What are your distribution needs?
├── Simple distribution → electron-packager
│   ├── Pros: Simpler setup, faster builds
│   └── Cons: Limited installer options, manual update handling
└── Full installer with auto-updates → electron-builder
    ├── Pros: Professional installers, auto-updates, code signing
    └── Cons: More complex setup, slower builds
```

### Process Communication Method Selection

```
What type of IPC do you need?
├── One-way message (fire and forget) → ipcRenderer.send() + ipcMain.on()
├── Request-response pattern → ipcRenderer.invoke() + ipcMain.handle()
├── Multiple responses to one request → ipcRenderer.send() + event.sender.send()
└── Synchronous response (AVOID) → ipcRenderer.sendSync()
```

### UI Framework Selection

```
What are your UI needs?
├── Simple app with few screens → Vanilla HTML/CSS/JS
├── Complex app with many components → React/Vue/Angular
│   ├── Need SEO or server-rendering → Consider Nextron (Next.js + Electron)
│   └── Desktop-focused only → Standard React/Vue with direct Electron integration
└── Native-like UI → Consider React Desktop or similar native-styled frameworks
```
</context>

<context name="electron_anti_patterns" priority="medium">
## Anti-Patterns and Common Mistakes

### 1. Disabling Security Features [AP-ELECTRON-001]

**Problem:**
Disabling security features like contextIsolation, webSecurity, or sandbox for convenience.

**Example:**
```javascript
const win = new BrowserWindow({
  webPreferences: {
    nodeIntegration: true,
    contextIsolation: false,
    webSecurity: false
  }
});
```

**Why It Fails:**
- Creates significant security vulnerabilities
- Allows potential XSS attacks to access Node.js capabilities
- Can lead to remote code execution vulnerabilities
- Makes your application a target for malicious actors

**Better Approach:**
```javascript
const win = new BrowserWindow({
  webPreferences: {
    preload: path.join(__dirname, 'preload.js'),
    contextIsolation: true,
    nodeIntegration: false
  }
});

// preload.js
const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('api', {
  // Expose only specific, safe functionalities
  readConfig: () => ipcRenderer.invoke('read-config')
});
```

**Severity:** High
**AI-Specific:** Yes - AI code generation often suggests insecure patterns

### 2. Synchronous IPC Communication [AP-ELECTRON-002]

**Problem:**
Using synchronous IPC calls (`ipcRenderer.sendSync`) which block the UI thread.

**Example:**
```javascript
// renderer.js
function saveData() {
  const result = window.ipcRenderer.sendSync('save-data', data);
  showResult(result);
}
```

**Why It Fails:**
- Blocks renderer process until main process responds
- Creates UI freezes and poor user experience
- Can lead to deadlocks if the main process is waiting for the renderer
- Performance issues in complex applications

**Better Approach:**
```javascript
// renderer.js
async function saveData() {
  try {
    const result = await window.api.saveData(data);
    showResult(result);
  } catch (error) {
    showError(error);
  }
}

// preload.js
contextBridge.exposeInMainWorld('api', {
  saveData: (data) => ipcRenderer.invoke('save-data', data)
});

// main.js
ipcMain.handle('save-data', async (event, data) => {
  // Process data asynchronously
  return await processData(data);
});
```

**Severity:** Medium
**AI-Specific:** No

### 3. Direct Remote Content Loading [AP-ELECTRON-003]

**Problem:**
Loading remote content directly in a BrowserWindow with Node.js integration enabled.

**Example:**
```javascript
const win = new BrowserWindow({
  webPreferences: {
    nodeIntegration: true
  }
});
win.loadURL('https://some-website.com');
```

**Why It Fails:**
- Remote content can execute arbitrary code with Node.js privileges
- Exposes user's system to potential attacks
- Creates a pathway for malicious code execution
- Violates basic security principles

**Better Approach:**
```javascript
// For remote content, disable Node integration and isolate content
const win = new BrowserWindow({
  webPreferences: {
    nodeIntegration: false,
    contextIsolation: true,
    sandbox: true
  }
});
win.loadURL('https://some-website.com');

// For trusted content that needs Node capabilities, use a separate window
const trustedWin = new BrowserWindow({
  webPreferences: {
    preload: path.join(__dirname, 'preload.js'),
    contextIsolation: true,
    nodeIntegration: false
  }
});
trustedWin.loadFile('trusted-content.html');
```

**Severity:** High
**AI-Specific:** Yes

### 4. Monolithic Process Architecture [AP-ELECTRON-004]

**Problem:**
Placing all application logic in either the main or renderer process instead of using appropriate process separation.

**Example:**
```javascript
// main.js with everything in the main process
app.whenReady().then(() => {
  // UI logic
  createWindow();
  
  // Database operations
  setupDatabase();
  
  // Business logic
  processBusinessRules();
  
  // File operations
  watchFileChanges();
  
  // Network requests
  setupNetworkListeners();
});
```

**Why It Fails:**
- Poor performance due to main process blocking
- Complex code that's difficult to maintain
- Inability to leverage multi-core processing
- UI freezes when heavy operations run
- Memory management issues

**Better Approach:**
```javascript
// main.js - responsible for app lifecycle and coordination
app.whenReady().then(() => {
  createWindow();
  setupIpcHandlers();
});

// Handle heavy tasks in main process or utility processes
ipcMain.handle('process-data', async (event, data) => {
  // Use worker threads or utility processes for CPU-intensive work
  return await workerPool.processTask(data);
});

// Delegate UI logic to renderer process via preload
// renderer.js handles UI updates and user interactions
```

**Severity:** Medium
**AI-Specific:** No

### 5. Excessive IPC Communication [AP-ELECTRON-005]

**Problem:**
Overusing IPC for fine-grained communication between processes.

**Example:**
```javascript
// renderer.js
function updateUI() {
  window.api.getData('user').then(user => {
    displayUser(user);
    return window.api.getData('preferences');
  }).then(prefs => {
    applyPreferences(prefs);
    return window.api.getData('notifications');
  }).then(notifications => {
    showNotifications(notifications);
    return window.api.getData('stats');
  }).then(stats => {
    updateStats(stats);
  });
}
```

**Why It Fails:**
- Creates performance overhead with many small IPC calls
- Increases complexity with callback chains
- Makes debugging difficult
- Results in poor code maintainability

**Better Approach:**
```javascript
// Batch related data requests
// renderer.js
async function updateUI() {
  try {
    const { user, preferences, notifications, stats } = 
      await window.api.getBatchData(['user', 'preferences', 'notifications', 'stats']);
    
    displayUser(user);
    applyPreferences(preferences);
    showNotifications(notifications);
    updateStats(stats);
  } catch (error) {
    handleError(error);
  }
}

// main.js
ipcMain.handle('get-batch-data', async (event, keys) => {
  const result = {};
  await Promise.all(keys.map(async key => {
    result[key] = await dataStore.get(key);
  }));
  return result;
});
```

**Severity:** Medium
**AI-Specific:** No

### 6. Ignoring Platform Differences [AP-ELECTRON-006]

**Problem:**
Writing code that doesn't account for differences between operating systems.

**Example:**
```javascript
// Assuming paths work the same on all platforms
const configPath = app.getPath('userData') + '/config.json';
fs.writeFileSync(configPath, JSON.stringify(config));

// Using platform-specific key combinations without checks
globalShortcut.register('CommandOrControl+Alt+K', () => {
  // This shortcut is problematic on some Linux distros
});
```

**Why It Fails:**
- Path separators differ between Windows and Unix-like systems
- OS-specific APIs behave differently
- UI conventions vary across platforms
- Keyboard shortcuts may conflict with OS-reserved combinations
- File permissions work differently

**Better Approach:**
```javascript
// Use path module for cross-platform path handling
const path = require('path');
const configPath = path.join(app.getPath('userData'), 'config.json');

// Check platform when necessary
if (process.platform === 'darwin') {
  // macOS-specific code
} else if (process.platform === 'win32') {
  // Windows-specific code
} else {
  // Linux/other platforms
}

// Be mindful of platform conventions for menus, shortcuts, etc.
const menuTemplate = process.platform === 'darwin' 
  ? macOSMenuTemplate 
  : windowsLinuxMenuTemplate;
```

**Severity:** Medium
**AI-Specific:** Yes
</context>

<context name="electron_code_implementation" priority="medium">
## Code Implementation

### Basic Application Structure

A well-organized Electron application typically follows this structure:

```
my-electron-app/
├── package.json
├── main.js                # Main process entry point
├── preload.js             # Preload script for secure API bridging
├── renderer/              # Renderer process code
│   ├── index.html         # Main application HTML
│   ├── app.js             # Renderer JavaScript
│   └── styles.css         # Application styles
├── src/                   # Shared source code
│   ├── constants.js       # Shared constants
│   └── utils.js           # Utility functions
├── assets/                # Application assets
│   ├── icons/             # Application icons
│   └── images/            # Application images
└── build/                 # Build configuration
    └── electron-builder.yml  # electron-builder config
```

### Minimal Electron Application

Here's a minimal Electron application with best practices:

**package.json:**
```json
{
  "name": "my-electron-app",
  "version": "1.0.0",
  "description": "A minimal Electron application",
  "main": "main.js",
  "scripts": {
    "start": "electron .",
    "build": "electron-builder",
    "test": "jest"
  },
  "author": "Your Name",
  "license": "MIT",
  "devDependencies": {
    "electron": "^25.0.0",
    "electron-builder": "^24.0.0",
    "jest": "^29.0.0"
  },
  "dependencies": {
    "electron-store": "^8.1.0"
  }
}

**main.js:**
```javascript
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const Store = require('electron-store');

// Initialize data store
const store = new Store();

// Handle creating/removing shortcuts on Windows when installing/uninstalling
if (require('electron-squirrel-startup')) {
  app.quit();
}

// Create main application window
function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false // Need to disable for preload to access Node APIs
    }
  });

  mainWindow.loadFile(path.join(__dirname, 'renderer', 'index.html'));
  
  // Open DevTools in development mode
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }
}

// Initialize app
app.whenReady().then(() => {
  // Set up IPC handlers
  setupIpcHandlers();
  
  // Create main window
  createWindow();

  // Re-create window on activate (macOS)
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

// Quit when all windows are closed, except on macOS
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Set up IPC handlers
function setupIpcHandlers() {
  // Handle data storage
  ipcMain.handle('store-get', (event, key) => {
    return store.get(key);
  });
  
  ipcMain.handle('store-set', (event, key, value) => {
    store.set(key, value);
    return true;
  });
}
```

**preload.js:**
```javascript
const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // Store
  storeGet: (key) => ipcRenderer.invoke('store-get', key),
  storeSet: (key, value) => ipcRenderer.invoke('store-set', key, value),
  
  // App info
  getVersion: () => process.versions.electron
});
```

**renderer/index.html:**
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'">
  <title>My Electron App</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <h1>Hello Electron!</h1>
  <p>Electron version: <span id="electron-version"></span></p>
  
  <div class="counter-container">
    <p>Counter: <span id="counter">0</span></p>
    <button id="increment-btn">Increment</button>
  </div>
  
  <script src="app.js"></script>
</body>
</html>
```

**renderer/app.js:**
```javascript
// Wait for DOM to load
document.addEventListener('DOMContentLoaded', () => {
  // Display Electron version
  document.getElementById('electron-version').textContent = window.electronAPI.getVersion();
  
  // Initialize counter from stored value
  updateCounterDisplay();
  
  // Set up button click handler
  document.getElementById('increment-btn').addEventListener('click', async () => {
    // Get current counter value
    const currentValue = await window.electronAPI.storeGet('counter') || 0;
    
    // Increment and store new value
    await window.electronAPI.storeSet('counter', currentValue + 1);
    
    // Update display
    updateCounterDisplay();
  });
});

// Update counter display from store
async function updateCounterDisplay() {
  const counter = await window.electronAPI.storeGet('counter') || 0;
  document.getElementById('counter').textContent = counter;
}
```

**renderer/styles.css:**
```css
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  padding: 20px;
  color: #333;
  background-color: #f5f5f5;
}

h1 {
  color: #2c3e50;
}

.counter-container {
  margin-top: 30px;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #2980b9;
}
```

### Advanced IPC Communication Example

For more complex applications, you might need more sophisticated IPC patterns:

**main.js (partial):**
```javascript
// Set up advanced IPC handlers
function setupAdvancedIpcHandlers() {
  // Example of handling file operations
  ipcMain.handle('read-file', async (event, filePath) => {
    try {
      // Validate input to prevent directory traversal
      const normalizedPath = path.normalize(filePath);
      if (normalizedPath.includes('..')) {
        throw new Error('Invalid file path');
      }
      
      // Read file content
      const content = await fs.promises.readFile(normalizedPath, 'utf8');
      return { success: true, data: content };
    } catch (error) {
      return { success: false, error: error.message };
    }
  });
  
  // Streaming example
  ipcMain.on('start-data-stream', (event) => {
    const dataSource = getDataSource();
    
    dataSource.on('data', (chunk) => {
      // Check if the window still exists
      if (!event.sender.isDestroyed()) {
        event.sender.send('data-chunk', chunk);
      }
    });
    
    dataSource.on('end', () => {
      if (!event.sender.isDestroyed()) {
        event.sender.send('data-end');
      }
    });
    
    dataSource.on('error', (error) => {
      if (!event.sender.isDestroyed()) {
        event.sender.send('data-error', error.message);
      }
    });
  });
  
  // Example with progress reporting
  ipcMain.handle('process-files', async (event, files) => {
    const total = files.length;
    let processed = 0;
    
    for (const file of files) {
      // Process file
      await processFile(file);
      
      // Report progress
      processed++;
      event.sender.send('process-progress', { processed, total });
    }
    
    return { success: true, message: 'All files processed' };
  });
}
```

**preload.js (partial):**
```javascript
// Enhanced API exposure
contextBridge.exposeInMainWorld('fileAPI', {
  // File operations
  readFile: (path) => ipcRenderer.invoke('read-file', path),
  
  // Stream handling
  startDataStream: () => {
    return new Promise((resolve, reject) => {
      const chunks = [];
      
      // Start the stream
      ipcRenderer.send('start-data-stream');
      
      // Handle data chunks
      ipcRenderer.on('data-chunk', (event, chunk) => {
        chunks.push(chunk);
      });
      
      // Handle completion
      ipcRenderer.on('data-end', () => {
        resolve(chunks);
        cleanup();
      });
      
      // Handle errors
      ipcRenderer.on('data-error', (event, error) => {
        reject(new Error(error));
        cleanup();
      });
      
      // Clean up listeners
      function cleanup() {
        ipcRenderer.removeAllListeners('data-chunk');
        ipcRenderer.removeAllListeners('data-end');
        ipcRenderer.removeAllListeners('data-error');
      }
    });
  },
  
  // Process with progress
  processFiles: (files) => {
    return {
      promise: ipcRenderer.invoke('process-files', files),
      onProgress: (callback) => {
        // Wrap callback to avoid exposing event object
        const progressListener = (event, progress) => callback(progress);
        ipcRenderer.on('process-progress', progressListener);
        
        // Return cleanup function
        return () => {
          ipcRenderer.removeListener('process-progress', progressListener);
        };
      }
    };
  }
});
```
