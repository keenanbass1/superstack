# Development Logging Commands

This directory contains the commands for managing development logs in the Superstack developer workflow system.

## Command Structure

```
dev log                          # Base command
  |- start <description>         # Start a log session
  |- end [--summary]             # End current session with optional summary
  |- add <content>               # Add generic entry to current session
  |- note <content>              # Add a note
  |- challenge <content>         # Add a challenge entry
  |- solution <content>          # Add a solution entry
  |- decision <content>          # Add a decision entry
  |- discovery <content>         # Add a discovery entry
  |- show [options]              # Show logs
  |- search <term>               # Search logs
```

## Common Workflows

### Daily Development Session

```bash
# Start your day
dev log start "Implementing user authentication feature"

# Document challenges encountered
dev log challenge "CORS issues with the authentication API"

# Record solutions
dev log solution "Added proper CORS headers and middleware configuration"

# Note important discoveries
dev log discovery "The Auth0 SDK handles token refresh automatically"

# Document decisions
dev log decision "Using HttpOnly cookies instead of localStorage for token storage"

# End your session with a summary
dev log end --summary
```

### Viewing and Searching Logs

```bash
# Show the current or most recent session
dev log show

# View recent sessions
dev log show --recent=5

# View a specific session
dev log show --session=session-20250410-123456

# Search logs for a term
dev log search "authentication"

# Search within a specific project
dev log search "authentication" --project=user-portal

# Search with date range
dev log search "bug" --start-date=2025-01-01 --end-date=2025-03-31
```

## Log File Structure

Logs are stored in a structured format in the following locations:

```
~/dev/superstack/logs/
├── daily/                    # Daily logs aggregating sessions
│   ├── 2025-04-10.md         # Log for a specific date
│   └── ...
├── sessions/                 # Individual session logs
│   ├── session-20250410-123456.md  # Detailed session log
│   └── ...
└── projects/                 # Project-specific logs
    ├── project-a/            # Logs for project A
    │   ├── sessions/         # Sessions for project A
    │   └── summaries/        # Summaries for project A
    └── ...
```

### Log Session Format

Each log session is stored as a Markdown file with the following structure:

```markdown
# Development Log Session: session-20250410-123456

## Description
Working on user authentication feature

## Metadata
- **Start Time**: 2025-04-10 09:15:22
- **End Time**: 2025-04-10 16:30:45
- **Duration**: 435 minutes
- **Project**: user-portal
- **Tags**: authentication, security, api
- **Git Branch**: feature/user-auth

## Log Entries

### 09:30:12 - Challenge
CORS issues with the authentication API

### 10:15:45 - Solution
Added proper CORS headers and middleware configuration

### 14:22:10 - Discovery
The Auth0 SDK handles token refresh automatically

### 15:45:33 - Decision
Using HttpOnly cookies instead of localStorage for token storage

## Summary
Implemented the core authentication flow using Auth0. Resolved CORS issues
and decided on a secure token storage approach. Next steps will be to 
implement the front-end components for the login and signup flows.
```

## Integration with Knowledge System

The logs are designed to be consumed by the knowledge extraction system, which can:

1. Identify common patterns across logs
2. Extract reusable solutions
3. Generate knowledge artifacts
4. Create retrospective summaries

Use the following practices to maximize the value of your logs:

- Be specific about challenges and solutions
- Document the reasoning behind decisions
- Include relevant technical details
- Use consistent terminology
- Add tags to make logs more searchable
