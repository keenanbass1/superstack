# Context Management Commands

This directory contains the commands for managing AI context in the Superstack developer workflow system.

## Command Structure

```
dev context                 # Base command
  |- list                   # List available context modules
  |- show <module>          # Show content of a context module
  |- add <modules...>       # Add module(s) to active context
  |- remove <modules...>    # Remove module(s) from active context
  |- push                   # Push active context to clipboard/AI
  |- clear                  # Clear all active context
  |- init                   # Initialize project context
  |- validate               # Validate context against schema
  |- group-list             # List available context groups
  |- group-create <n> <...> # Create a new context group
  |- group-add <n>          # Add a group to active context
  |- group-delete <n>       # Delete a context group
```

## Files

- `list.ts` - Command to list available context modules
- `show.ts` - Command to show content of a context module
- `add.ts` - Command to add modules to active context
- `remove.ts` - Command to remove modules from active context
- `push.ts` - Command to push active context to clipboard/AI
- `clear.ts` - Command to clear all active context
- `group-list.ts` - Command to list available context groups
- `group-create.ts` - Command to create a new context group
- `group-add.ts` - Command to add a group to active context
- `group-delete.ts` - Command to delete a context group

## Common Workflows

### Setting up context for a task

```bash
# Clear previous context
dev context clear

# Add relevant context modules
dev context add design/principles/typography design/ui-patterns/cards

# Push to clipboard for AI tools
dev context push
```

### Using context groups

```bash
# Create a context group
dev context group-create ui-patterns design/ui-patterns/cards design/ui-patterns/buttons

# Add the group to active context
dev context group-add ui-patterns

# Push context to clipboard
dev context push
```

### Exploring available context

```bash
# List all available modules
dev context list

# Filter by domain
dev context list --domain design

# Show details of a specific module
dev context show design/principles/typography
```

## Integration with AI Tools

The context can be used with different AI tools:

1. **Clipboard Integration**: Use `dev context push` to copy formatted context to clipboard
2. **Project Context**: Use `dev context init` to create project-specific context
3. **Direct Integration**: Future implementation will support direct API integration with Claude, GPT, etc.
