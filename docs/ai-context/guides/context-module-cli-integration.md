# Context Module CLI Integration Guide

This guide explains how to integrate your newly created context modules with the Superstack CLI tool (`dev`) to make them fully operational in your AI-augmented development workflow.

## Directory Structure for Context Modules

Based on your uploaded documentation, context modules should follow this directory structure:

```
docs/
  ai-context/
    [domain]/
      [subdomain]/
        [module-name].md
```

For example:
```
docs/
  ai-context/
    development/
      patterns/
        electron.md
    design/
      principles/
        visual-hierarchy.md
```

## Making Modules Compatible with the CLI

To ensure your context modules work seamlessly with the CLI tool, follow these steps:

### 1. Proper File Naming and Location

- Use kebab-case for module names (e.g., `electron.md`, `visual-hierarchy.md`)
- Place modules in the correct domain and subdomain directories
- Use `.md` file extension for all modules

### 2. MCP-Compatible Format

- Follow the MCP tag structure:
  ```markdown
  <context name="descriptive_name" priority="high|medium|low">
  Content goes here...
  </context>
  ```
- Include required metadata section at the top
- Structure content from highest to lowest priority
- Use proper section headers and formatting

### 3. Required Metadata Section

Ensure each module starts with a metadata section:

```markdown
## Metadata
- **Priority:** high
- **Domain:** development
- **Target Models:** claude, gpt
- **Related Modules:** related-module-1, related-module-2
```

## Adding Modules Using the CLI

Based on your documentation, you can use the CLI to manage context modules:

### Add a New Module to Active Context

```bash
dev context add [domain]/[subdomain]/[module-name]
```

Example:
```bash
dev context add development/patterns/electron
```

### Push Context to Claude

After adding or updating modules, push them to Claude with:

```bash
dev context push-claude
```

### Create or Update Context Groups

Group related modules together:

```bash
dev context create-group [group-name] [module1] [module2] [new-module]
```

Example:
```bash
dev context create-group desktop-development development/patterns/electron development/patterns/react-desktop
```

### Edit Existing Modules

Open a module for editing:

```bash
dev context edit [domain]/[subdomain]/[module-name]
```

Example:
```bash
dev context edit development/patterns/electron
```

## Module Creation Automation

Your documentation mentions a potential CLI command for automating module creation:

```bash
dev context create-module [domain]/[subdomain]/[name]
```

This command would:
1. Create a file with the template pre-populated
2. Open it in Cursor for editing
3. Provide a checklist of steps to complete
4. Offer to test with Claude when finished

If this command exists in your CLI, you can use it to streamline the module creation process. If not, consider implementing it based on the template and guidance documents.

## Testing Your Context Modules

After creating a module, test it to ensure it works correctly:

1. **Add to Active Context**:
   ```bash
   dev context add [domain]/[subdomain]/[module-name]
   ```

2. **Push to Claude**:
   ```bash
   dev context push-claude
   ```

3. **Test with Validation Questions**:
   ```
   "Based on the context I provided, explain the key principles of [topic] and how they should be applied."
   ```

4. **Test with Implementation Scenarios**:
   ```
   "Using the context module I shared, can you provide a concrete implementation example for [specific scenario]?"
   ```

5. **Refine Based on Testing Results**:
   ```bash
   dev context edit [domain]/[subdomain]/[module-name]
   ```

## Maintaining Context Module Registry

As you add more modules, maintain a registry or index to keep track of them:

1. **Update README.md** in your context directory with new modules
2. **Maintain Lists of Modules** by domain, priority, or other groupings
3. **Document Module Relationships** to create a knowledge graph
4. **Track Module Status** (complete, in-progress, needs update)

## MCP Validation

Your documentation suggests a CLI command for validating MCP compatibility:

```bash
dev context validate-mcp [domain]/[subdomain]/[module-name]
```

Use this to check your modules for:
- Proper MCP tag format
- Consistent priority levels
- Descriptive chunk names
- Complete content structure

## CLI Integration Example Session

Here's an example workflow for creating and integrating a new Electron context module:

```bash
# 1. Create module structure
mkdir -p docs/ai-context/development/patterns

# 2. Create the module file
dev context create-module development/patterns/electron

# 3. Edit in Cursor (or use the CLI's edit command)
# (edit the module with the template and your content)

# 4. Validate MCP compatibility
dev context validate-mcp development/patterns/electron

# 5. Add to active context
dev context add development/patterns/electron

# 6. Push to Claude
dev context push-claude

# 7. Test in Claude
# (Ask Claude questions about Electron to verify module effectiveness)

# 8. Add to relevant context group
dev context create-group desktop-frameworks development/patterns/electron
```

## Troubleshooting Integration Issues

If your context modules aren't working as expected:

1. **Check File Location**: Ensure modules are in the correct directory path
2. **Verify MCP Format**: Check that all context tags are properly formatted 
3. **Validate Metadata**: Ensure metadata section is complete and correctly formatted
4. **Check File Encoding**: Files should be UTF-8 encoded
5. **Monitor CLI Logs**: Look for warnings or errors when running CLI commands
6. **Test Smaller Chunks**: If large modules fail, test with smaller content sections
7. **Verify CLI Version**: Ensure you're using the latest version of your CLI tool

## Automating Module Updates

For keeping modules current, consider setting up a regular review process:

```bash
# List all modules that haven't been updated in the last 90 days
dev context list-outdated --days 90

# Generate a report of module status
dev context report > module-status.md
```

## Conclusion

By following these integration steps, your context modules will become operational components of your AI-augmented development workflow. The CLI integration creates a smooth experience for managing, updating, and utilizing your knowledge base across projects.

Remember to periodically review and update your modules as technologies evolve and new patterns or anti-patterns emerge.
