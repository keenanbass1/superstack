# 📗 Superstack CLI Documentation

> The `dev` command-line interface is the primary tool for interacting with the Superstack developer workflow system.

## 🚀 Getting Started

### Installation

```bash
# Install globally
npm install -g @superstack/cli

# Or install locally in a project

```

### Basic Usage

```bash
# Get help
dev --help

# Create a new project
dev new my-awesome-app

# Initialize project context
dev context init

# Push context to AI assistants
dev context push
```

## 📋 Command Reference

### Project Management

#### `dev new <n>`

Creates a new project from a template.

```bash
# Create a new Next.js project
dev new my-next-app

# Use a specific template
dev new my-api --template=express

# Create in a specific directory
dev new my-app --directory=/path/to/dir

# Skip git initialization
dev new my-app --no-git

# Skip dependency installation
dev new my-app --no-install
```

Options:
- `-t, --template <template>`: Project template to use (default: from config)
- `-d, --directory <directory>`: Directory to create the project in
- `--no-git`: Skip git initialization
- `--no-install`: Skip dependency installation

### Context Management

#### `dev context init`

Initializes project context for AI assistants.

```bash
dev context init
```

This command:
1. Creates a `.superstack/context` directory in your project
2. Generates a `project-context.md` file with project details
3. Populates it with information from package.json and git

#### `dev context push`

Pushes project context to AI assistants.

```bash
# Push to all configured assistants
dev context push

# Push to a specific assistant
dev context push --target=claude
```

Options:
- `-t, --target <target>`: Target AI assistant (claude, gpt, cursor)

#### `dev context validate`

Validates project context against the schema.

```bash
dev context validate
```

#### `dev context edit`

Opens the project context file in your default editor.

```bash
dev context edit
```

### Development Logging

#### `dev log add <message>`

Adds a log entry to the daily development log.

```bash
# Add a simple log entry
dev log add "Fixed navbar styling issues"

# Add with tags
dev log add "Implemented user authentication" --tags=feature,auth

# Specify project (if not in project directory)
dev log add "Updated API docs" --project=backend-api
```

Options:
- `-t, --tags <tags>`: Comma-separated tags for the log entry
- `-p, --project <project>`: Project name (defaults to current directory)

#### `dev log start [description]`

Starts a new development session log.

```bash
# Start a session with description
dev log start "Implementing user dashboard"

# Start a session for a specific project
dev log start "API refactoring" --project=backend-api
```

Options:
- `-p, --project <project>`: Project name (defaults to current directory)

#### `dev log end`

Ends the current development session log.

```bash
# End session
dev log end

# End and generate an AI summary
dev log end --summary
```

Options:
- `--summary`: Generate an AI summary of the session

#### `dev log note <message>`

Adds a note to the current development session.

```bash
dev log note "Discovered a bug in the authentication flow"
```

#### `dev log show`

Shows development logs.

```bash
# Show the current session
dev log show

# Show logs for a specific date
dev log show --date=2025-04-09

# Show logs for a specific project
dev log show --project=frontend

# Show recent logs
dev log show --recent=3

# Show a specific session
dev log show --session=session-20250409-123456
```

Options:
- `-d, --date <date>`: Show logs for a specific date (YYYY-MM-DD)
- `-p, --project <project>`: Filter logs by project
- `-t, --tag <tag>`: Filter logs by tag
- `--recent [days]`: Show recent logs (default: 7 days)
- `--session <sessionId>`: Show a specific session log

### AI Assistance

#### `dev ai solve <problem>`

Gets AI help to solve a development problem.

```bash
# Get help with a coding problem
dev ai solve "How do I implement infinite scrolling in React?"

# Use a specific AI model
dev ai solve "How should I structure my API?" --model=gpt

# Skip including project context
dev ai solve "How do I optimize this query?" --no-context
```

Options:
- `-m, --model <model>`: AI model to use (claude, gpt)
- `-c, --context`: Include project context (default: true)
- `-n, --no-context`: Exclude project context

#### `dev ai generate <type>`

Generates code or content using AI.

```bash
# Generate a React component
dev ai generate component --description="User profile card with avatar"

# Generate an API endpoint
dev ai generate endpoint --description="User registration with email verification"

# Use a specific model
dev ai generate schema --description="Blog post data model" --model=gpt
```

Options:
- `-d, --description <description>`: Description of what to generate
- `-m, --model <model>`: AI model to use (claude, gpt)
- `-c, --context`: Include project context (default: true)
- `-n, --no-context`: Exclude project context

#### `dev ai review <path>`

Gets an AI code review for a file or directory.

```bash
# Review a specific file
dev ai review src/components/Button.tsx

# Review with a specific model
dev ai review utils/validation.js --model=gpt

# Review without project context
dev ai review app/api/users.ts --no-context
```

Options:
- `-m, --model <model>`: AI model to use (claude, gpt)
- `-c, --context`: Include project context (default: true)
- `-n, --no-context`: Exclude project context

### Configuration

#### `dev config list`

Lists all configuration settings.

```bash
dev config list
```

#### `dev config get <key>`

Gets a specific configuration value.

```bash
dev config get editor
dev config get aiProviders.claude.model
```

#### `dev config set <key> <value>`

Sets a specific configuration value.

```bash
dev config set editor "vim"
dev config set defaultProjectTemplate "express"
dev config set aiProviders.claude.model "claude-3-opus-20240229"
```

#### `dev config init`

Initializes configuration with interactive prompts.

```bash
dev config init
```

## 📁 Directory Structure

The Superstack system uses the following directory structure:

```
~/dev/
├── superstack/             # The meta-development system
│   ├── docs/               # System documentation
│   ├── templates/          # Templates for projects and prompts
│   │   ├── project-types/  # Project templates
│   │   │   ├── next/       # Next.js template
│   │   │   └── express/    # Express template
│   │   └── prompts/        # AI prompt templates
│   ├── scripts/            # Automation scripts
│   ├── config/             # Configuration files
│   ├── llm/                # AI integration files
│   │   └── schemas/        # JSON schemas for validation
│   ├── logs/               # Development logs
│   │   └── sessions/       # Session logs
│   └── retros/             # Project retrospectives
│
├── projects/               # Active development projects
├── experiments/            # Code explorations
└── archive/                # Archived projects
```

## 🧩 Project Templates

Superstack comes with project templates for different types of applications:

- **Next.js**: Modern React framework for full-stack web applications
- **Express**: Node.js backend API service
- **CLI Tool**: Command-line interface application
- *More coming soon...*

## 🌟 Best Practices
c
### Context Management

- Update your project context regularly as the project evolves
- Include key architectural decisions and domain knowledge
- Focus on information that will help AI assistants understand your project
- Push context before starting a complex development task

### Development Logging

- Start a session at the beginning of your development day or task
- Add detailed notes as you work through problems
- End sessions with a summary of what was accomplished
- Use tags to categorize log entries for easier searching
- Review logs regularly to extract patterns and insights

### AI Assistance

- Use specific command types for different tasks (solve, generate, review)
- Provide detailed descriptions for better AI responses
- Review and adapt AI suggestions to your specific needs
- Save useful AI responses by copying them into your project's knowledge base

## 🛠️ Advanced Usage

### Creating Custom Templates

You can create your own project templates in the `~/dev/superstack/templates/project-types/` directory:

1. Create a new directory with your template name
2. Add all files needed for the template
3. Use placeholders like `{{PROJECT_NAME}}` in files to be replaced
4. Use the template with `dev new <n> --template=<your-template>`

### Extending the AI Prompt Library

Create custom AI prompts in the `~/dev/superstack/templates/prompts/` directory:

1. Create a new Markdown file for your prompt template
2. Use placeholders like `{{DESCRIPTION}}` and `{{CONTEXT}}`
3. The prompt will be automatically available in the corresponding AI commands

### Integration with External Tools

The Superstack CLI can be integrated with:

- **Git workflows**: Use with git hooks for automatic context updates
- **CI/CD pipelines**: Incorporate into build processes
- **Editor extensions**: Configure hotkeys to trigger common commands
- **Project management tools**: Link logs with issue tracking systems

## 🤔 Troubleshooting

### Common Issues

- **Command not found**: Ensure the CLI is installed globally or use npx
- **Context not found**: Run `dev context init` in your project directory
- **Template not found**: Check that the template exists in the templates directory
- **Configuration errors**: Run `dev config init` to reset your configuration

### Getting Help

For more detailed help on any command, use the `--help` flag:

```bash
dev --help
dev new --help
dev context push --help
```

## 📄 License

Superstack is licensed under the MIT License. See the LICENSE file for details.

---

*Documentation last updated: April 9, 2025*