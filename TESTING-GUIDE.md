# Superstack Testing Guide

> A comprehensive guide to testing the functionality of the Superstack developer workflow system

This document provides step-by-step instructions for testing each component of the Superstack system. As new features are added, this guide will be updated to ensure you can verify functionality and keep the project on track.

## Table of Contents

- [Setup and Installation](#setup-and-installation)
- [Context Management](#context-management)
  - [Listing Available Modules](#listing-available-modules)
  - [Adding Modules to Active Context](#adding-modules-to-active-context)
  - [Viewing Module Content](#viewing-module-content)
  - [Removing Modules](#removing-modules)
  - [Clearing Active Context](#clearing-active-context)
  - [Pushing Context to Clipboard](#pushing-context-to-clipboard)
- [Context Group Management](#context-group-management)
  - [Creating Context Groups](#creating-context-groups)
  - [Listing Groups](#listing-groups)
  - [Adding Groups to Active Context](#adding-groups-to-active-context)
  - [Deleting Groups](#deleting-groups)
- [Project Context Management](#project-context-management)
  - [Initializing Project Context](#initializing-project-context)
  - [Validating Project Context](#validating-project-context)
- [Development Logging](#development-logging)
  - [Session Management](#session-management)
  - [Adding Log Entries](#adding-log-entries)
  - [Viewing Logs](#viewing-logs)
  - [Searching Logs](#searching-logs)
- [Troubleshooting](#troubleshooting)

## Setup and Installation

Before testing, ensure you have the CLI tool properly installed:

```bash
# Navigate to the CLI directory
cd ~/dev/superstack/scripts/dev

# Install dependencies
npm install

# Build the CLI
npm run build

# Create a global symlink
npm link
```

Verify the installation:

```bash
dev --help
```

You should see the main help menu with available commands.

## Context Management

### Listing Available Modules

Test the ability to list available context modules:

```bash
# List all modules
dev context list

# List modules with domain filter
dev context list --domain design

# List modules with type filter
dev context list --type principles

# List only active modules
dev context list --active

# Output as JSON
dev context list --json
```

**Success criteria**: 
- Command displays available modules organized by domain and type
- Filters correctly limit results
- Active modules are indicated if using --active flag
- JSON output is properly formatted

### Adding Modules to Active Context

Test adding modules to active context:

```bash
# Add a single module
dev context add design/principles/typography

# Add multiple modules
dev context add design/principles/spacing design/ui-patterns/cards

# Try adding an invalid module
dev context add invalid/module/path

# Try adding a module that's already in context
dev context add design/principles/typography
```

**Success criteria**:
- Valid modules are added to active context
- Multiple modules can be added at once
- Error is shown for invalid modules
- No error when adding already-active modules (just adds once)
- Current active context is displayed after adding

### Viewing Module Content

Test viewing module content:

```bash
# View a specific module
dev context show design/principles/typography

# View all active modules
dev context show --active

# Try viewing an invalid module
dev context show invalid/module
```

**Success criteria**:
- Module content is correctly displayed
- All active modules are shown when using --active flag
- Error is shown for invalid modules

### Removing Modules

Test removing modules from active context:

```bash
# First add some modules
dev context add design/principles/typography design/ui-patterns/cards

# Remove a single module
dev context remove design/principles/typography

# Try removing a module that's not in context
dev context remove design/principles/spacing

# Remove multiple modules at once
dev context add design/principles/typography design/ui-patterns/cards
dev context remove design/principles/typography design/ui-patterns/cards
```

**Success criteria**:
- Modules are successfully removed from active context
- Error is shown when trying to remove inactive modules
- Multiple modules can be removed at once
- Current active context is displayed after removal

### Clearing Active Context

Test clearing all active context:

```bash
# First add some modules
dev context add design/principles/typography design/ui-patterns/cards

# Clear all context
dev context clear

# Check that context is empty
dev context list --active
```

**Success criteria**:
- All modules are removed from active context
- Confirmation is requested before clearing
- No active modules remain after clearing

### Pushing Context to Clipboard

Test pushing context to clipboard:

```bash
# First add some modules
dev context add design/principles/typography design/ui-patterns/cards

# Push to clipboard
dev context push

# Try pushing with empty context
dev context clear
dev context push
```

**Success criteria**:
- Context is formatted and copied to clipboard
- Content can be pasted into a text editor
- Format includes module headers and content
- Error is shown when pushing empty context

## Context Group Management

### Creating Context Groups

Test creating context groups:

```bash
# Create a group with multiple modules
dev context group-create ui-basics design/principles/typography design/principles/spacing

# Create a group with description
dev context group-create components design/ui-patterns/cards design/ui-patterns/buttons --description "Common UI components"

# Try creating a group with invalid modules
dev context group-create invalid-group invalid/module

# Try creating a group with existing name
dev context group-create ui-basics design/principles/typography
```

**Success criteria**:
- Groups are created with the specified modules
- Descriptions are saved with the group
- Error is shown for invalid modules
- Error is shown when using an existing group name

### Listing Groups

Test listing available groups:

```bash
# List all groups
dev context group-list

# List as JSON
dev context group-list --json
```

**Success criteria**:
- All created groups are listed
- Group details (modules, creation date) are shown
- JSON output is properly formatted

### Adding Groups to Active Context

Test adding groups to active context:

```bash
# First clear existing context
dev context clear

# Add a group to active context
dev context group-add ui-basics

# Check active modules
dev context list --active

# Try adding an invalid group
dev context group-add non-existent-group
```

**Success criteria**:
- All modules in the group are added to active context
- Current active context is displayed after adding
- Error is shown for invalid group names

### Deleting Groups

Test deleting context groups:

```bash
# Delete a group
dev context group-delete components

# Try deleting a non-existent group
dev context group-delete non-existent-group

# Force delete without confirmation
dev context group-delete ui-basics --force
```

**Success criteria**:
- Group is successfully deleted
- Confirmation is requested before deletion
- Error is shown for non-existent group names
- Force option skips confirmation

## Project Context Management

### Initializing Project Context

Test initializing project context:

```bash
# Create a test directory
mkdir ~/dev/test-project
cd ~/dev/test-project

# Initialize project context
dev context init

# Check that context file was created
ls -la

# Try reinitializing (should prompt for overwrite)
dev context init
```

**Success criteria**:
- Project context file is created
- File contains template with project name
- Overwrite confirmation is shown on reinitialize

### Validating Project Context

Test validating project context:

```bash
# Check unedited context (should show placeholders)
dev context validate

# Edit context to fill in some values
nano project-context.md
# (Edit some values but leave some placeholders)

# Validate again
dev context validate

# Fill in all placeholders and validate again
nano project-context.md
# (Fill in all placeholders)
dev context validate
```

**Success criteria**:
- Validation identifies unfilled placeholders
- Placeholders are correctly listed
- Success message when all placeholders are filled

## Development Logging

### Session Management

Test starting and ending log sessions:

```bash
# Start a new log session
dev log start "Implementing feature X"

# Start with project and tags
dev log start "Bug fixes for API" --project=backend-api --tags=bug,api,fix

# Try starting a second session (should fail)
dev log start "Another session"

# End the current session
dev log end

# End with summary
dev log start "Testing authentication flow"
dev log end --summary
```

**Success criteria**:
- Session is created with correct metadata
- Project name is captured correctly
- Tags are stored and displayed
- Error when starting a session while one is active
- Session is properly ended
- Summary option opens editor and saves summary

### Adding Log Entries

Test adding various types of log entries:

```bash
# Start a session first
dev log start "Testing log entries"

# Add a generic entry
dev log add "This is a general note" --type=note

# Add a challenge entry
dev log challenge "Having trouble with the database connection"

# Add a solution
dev log solution "Fixed by updating the connection string"

# Add a decision
dev log decision "Will use PostgreSQL instead of MySQL"

# Add a discovery
dev log discovery "Found that the framework has built-in caching"

# Add entries with tags
dev log note "Important configuration detail" --tags=config,important
```

**Success criteria**:
- Entries are added to the current session
- Different entry types are properly formatted
- Tags are associated with entries
- Error if no active session exists

### Viewing Logs

Test viewing log sessions:

```bash
# Show current/active session
dev log show

# Show a specific session (ID from previous commands)
dev log show --session=session-20250412-123456

# Show recent sessions
dev log show --recent=3

# Show logs for a specific project
dev log show --project=backend-api

# Output as JSON
dev log show --session=session-20250412-123456 --json
```

**Success criteria**:
- Active session details are displayed
- Session details include metadata and entries
- Recent sessions are listed correctly
- Project filtering works
- JSON output is properly formatted

### Searching Logs

Test searching through logs:

```bash
# Search for a term
dev log search "database"

# Search with project filter
dev log search "API" --project=backend-api

# Search with date range
dev log search "bug" --start-date=2025-01-01 --end-date=2025-04-12

# Limit search results
dev log search "feature" --limit=5
```

**Success criteria**:
- Search results show matching sessions/entries
- Context around matches is displayed
- Filters limit results appropriately
- Search is case-insensitive

## Troubleshooting

If you encounter issues during testing:

1. **Command not found**:
   - Check that the CLI was built successfully with `npm run build`
   - Verify the global link with `which dev`
   - Try reinstalling with `npm unlink` followed by `npm link`

2. **Missing modules**:
   - Confirm that the ai-context directory exists and contains modules
   - Check path references in `contextModules.ts`

3. **Permission errors**:
   - Check permissions on ~/.config/superstack directory
   - Ensure you have write access to configuration files

4. **Configuration files**:
   - Examine ~/.config/superstack/active-context.json
   - Examine ~/.config/superstack/context-groups.json
   - Examine ~/.config/superstack/session-state.json

5. **Log not being created**:
   - Check that the logs directory exists
   - Ensure you have write permissions for the logs directory
   - Check that required directories are being created in ensureLogDirectories()

---

This testing guide will be updated as new features are added to the Superstack system. Use it to verify functionality and keep the project on track.

*Last Updated: April 2025*
