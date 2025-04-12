# AI Context System CLI Guide

This guide explains how to use the AI context management system through the `dev` CLI tool. The context system helps you provide structured knowledge to AI tools to enhance their capabilities.

## Basic Usage

### Listing Available Contexts

```bash
# List all available context modules
dev context list

# List currently active contexts
dev context list-active

# List available context groups
dev context list-groups
```

### Managing Active Contexts

```bash
# Add a context module to active context
dev context add design/principles/visual-hierarchy

# Remove a context module from active context
dev context remove design/principles/visual-hierarchy

# Clear all active contexts
dev context clear
```

### Working with Context Groups

```bash
# Create a new context group
dev context create-group ui-basics design/principles/typography design/principles/spacing

# Add a context group to active context
dev context add-group ui-basics
```

### Viewing Context Content

```bash
# Show content of a specific context module
dev context show design/principles/visual-hierarchy

# Show content of all active context modules
dev context show-active
```

### Creating New Context Modules

```bash
# Create a new context module from template
dev context create design/principles/animation
```

## Advanced Usage

### Pushing Context to AI Tools

```bash
# Copy active context to clipboard for pasting into AI tools
dev context push
```

### Context-Aware AI Prompting

```bash
# Send a prompt to AI with active context (if integrated)
dev context prompt "Design a card component with proper spacing"
```

## Workflow Examples

### UI Component Development

```bash
# Add relevant design principles to context
dev context add design/principles/visual-hierarchy
dev context add design/principles/spacing-systems
dev context add design/ui-patterns/cards

# Copy context to clipboard for use with Cursor AI
dev context push

# Open file in Cursor with context available
cursor src/components/ProductCard.tsx
```

### Project Initialization

```bash
# Create a context group for project setup
dev context create-group project-init system/workflow/project-setup development/patterns/file-structure

# Apply the context group
dev context add-group project-init

# Use context with AI to scaffold project
dev context prompt "Set up a new Next.js project with Supabase integration"
```

### Code Review

```bash
# Add code quality contexts
dev context add development/practices/code-quality
dev context add development/practices/testing

# Use for code review assistance
dev context prompt "Review this component for best practices"
```

## Context Module Locations

The context modules are organized by domain:

- **design/principles/** - Design fundamentals (spacing, typography, etc.)
- **design/ui-patterns/** - UI components and patterns
- **design/ux-patterns/** - UX flows and interaction patterns
- **development/patterns/** - Code architecture patterns
- **development/practices/** - Development methodologies
- **system/workflow/** - Development workflow patterns
- **system/ai/** - AI interaction patterns

## Creating Custom Context Groups

For frequently used combinations of context modules, create custom groups:

```bash
# Create a group for React component development
dev context create-group react-component \
  design/principles/visual-hierarchy \
  design/principles/spacing-systems \
  development/patterns/react-components

# Create a group for API development
dev context create-group api-development \
  development/patterns/api-design \
  development/practices/error-handling \
  development/practices/security
```

## Integration with Development Workflow

The context system is designed to be integrated into your overall development workflow:

1. **Project Planning**: Use relevant context modules for architecture decisions
2. **Implementation**: Apply component-specific contexts during development
3. **Review**: Use quality and testing contexts during code review
4. **Documentation**: Reference context principles in project documentation

## Tips for Effective Context Usage

1. **Start Specific**: Begin with focused, relevant contexts rather than too many
2. **Combine Complementary Modules**: Mix principles with implementation patterns
3. **Create Task-Specific Groups**: Define context groups for common development tasks
4. **Refresh Context Regularly**: Update active context as your focus changes
5. **Test with Different AI Tools**: Verify context effectiveness with various AI assistants

## Troubleshooting

- **Context Not Found**: Check the path and ensure you're using the correct module name
- **Group Not Found**: Verify the group name and that it has been created
- **Context Not Applied in AI**: Ensure the context was properly pushed/pasted into the AI tool
- **Context Too Large**: If AI tools struggle with context size, reduce the number of active modules
