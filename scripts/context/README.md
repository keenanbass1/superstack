# Context Management System

> A modular, AI-first context management system that makes your AI tools smarter.

## Overview

This system provides a comprehensive way to manage context information for AI tools. It allows you to:

- Organize domain knowledge in modular context files
- Manage active context for AI interactions
- Create context groups for specific tasks
- Analyze content and get context recommendations
- Push context to your clipboard or directly to AI tools
- Integrate with Wox launcher for quick access

## Core Components

### 1. Context Management

The base context management system provides fundamental functionality:

- `context-commands.js`: Core functions for context management
- `context-integration.js`: Integration utilities for AI tools

### 2. Utility Modules

Specialized utilities enhance the system capabilities:

- `utils/module-recommender.js`: Context module recommendations based on content analysis
- `utils/token-manager.js`: Token counting, optimization, and limits for different AI models
- `utils/clipboard-manager.js`: Cross-platform clipboard integration

### 3. CLI Tools

Command-line interfaces for context management:

- `cli-enhanced.js`: Advanced CLI with intelligent recommendations and token management
- `dev-prompt-launcher.sh`: Fuzzy search for prompt templates
- `context-splitter.py`: Utility to split large context into manageable chunks

### 4. Launcher Integration

Provides integration with Wox launcher:

- `wox-integration.js`: Core functionality for Wox integration

## Usage

### Basic Context Management

```bash
# List available context modules
node cli-enhanced.js list

# Add a context module
node cli-enhanced.js add accessibility/core-principles

# List active context modules
node cli-enhanced.js active

# Copy active context to clipboard
node cli-enhanced.js copy
```

### Using Context Groups

```bash
# List available context groups
node cli-enhanced.js group list

# Create a new context group
node cli-enhanced.js group create web-dev accessibility/core-principles css/responsive-design

# Apply a context group
node cli-enhanced.js group add web-dev
```

### Working with Templates

```bash
# Process a template with active context
node cli-enhanced.js prompt code-review.md --copy

# Process with variables
node cli-enhanced.js prompt code-review.md --var "FILENAME=app.js" --var "CODE=console.log('test')" --copy
```

### Content Analysis

```bash
# Analyze content in clipboard and get recommendations
node cli-enhanced.js analyze --clipboard

# Analyze file and add recommended modules
node cli-enhanced.js analyze mycode.js --add
```

### Initialize Accessibility Context Groups

```bash
# Set up pre-defined accessibility context groups
node cli-enhanced.js init-accessibility
```

## Installation

1. Clone the repository
2. Install dependencies:
```bash
npm install commander fs-extra clipboardy
```
3. Add to your PATH or create aliases for easy access

## Wox Integration 

### Setup

1. Create a Wox plugin directory:
```
SuperStackWox/
├── plugin.json           # Plugin manifest
├── main.py               # Python wrapper
├── lib/                  # JavaScript core (copy all context/ files here)
└── Images/               # Icons for the plugin
```

2. Create a `plugin.json` file:
```json
{
  "ID": "com.yourname.superstack",
  "ActionKeyword": "ctx",
  "Name": "SuperStack Context Manager",
  "Description": "AI context management for development",
  "Author": "Your Name",
  "Version": "1.0.0",
  "Language": "python",
  "Website": "https://github.com/yourusername/superstack-wox",
  "IcoPath": "Images\\context.png",
  "ExecuteFileName": "main.py"
}
```

3. Create `main.py` to interface with the JavaScript modules

4. Install in Wox plugins directory

## Directory Structure

The recommended structure for the context modules themselves:

```
~/dev/superstack/docs/ai-context/
├── README.md                  # Overview documentation
├── accessibility/             # Accessibility context domain
│   ├── core-principles.md     # Fundamental accessibility concepts
│   ├── wcag-guidelines.md     # WCAG standards and requirements
│   ├── implementation/        # Implementation patterns
│   │   ├── forms.md           # Form accessibility
│   │   └── ...                # Other implementation guides
│   └── testing/               # Testing methodologies
├── react/                     # React context domain
│   ├── component-patterns.md  # React component patterns
│   └── ...                    # Other React context
└── templates/                 # Context module templates
    └── context-module-template.md  # Template for new modules
```

## Extending The System

### Adding New Domains

1. Create a new directory in the context directory
2. Add context modules following the template structure
3. Update the module recommender with new domain keywords and patterns

### Enhancing CLI Features

1. Add new commands to `cli-enhanced.js`
2. Update integration utilities as needed
3. Test with different AI models and tools

### Improving Recommendations

1. Enhance domain definitions in `module-recommender.js`
2. Add more specific keywords and code patterns
3. Refine recommendation algorithms

## Best Practices

1. **Keep Modules Focused**: Each context module should cover a single, well-defined topic
2. **Structure Content Properly**: Use clear headings, examples, and concise explanations
3. **Include Examples**: Always provide code examples to illustrate concepts
4. **Consider Token Usage**: Be mindful of token limits when creating and using context
5. **Use Context Groups**: Create logical groups for common tasks and workflows
6. **Regularly Review and Refine**: Update content based on effectiveness
