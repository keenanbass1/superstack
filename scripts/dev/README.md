# Superstack Developer CLI

A custom CLI for AI-augmented development workflow.

## Installation

### Easy Installation

Use the provided installation script which will set up everything automatically:

```bash
# Clone the repository if you haven't already
git clone https://github.com/yourusername/superstack.git
cd superstack/scripts/dev

# Run the installation script
./install.sh

# Now you can use the CLI from anywhere
dev --help
```

### Manual Installation

If you prefer to install manually:

```bash
cd superstack/scripts/dev

# Install dependencies and build
npm install
npm run build

# Install globally
npm link
```

### Environment Variables

The CLI automatically handles environment variables and will work without any manual configuration. However, you can customize the following variables if needed:

- `DEV_ROOT`: The root directory for development (default: `~/dev`)
- `PROJECTS_DIR`: The directory where projects are stored (default: `~/dev/projects`)

You can set these variables in:

1. Your shell profile (e.g., `.bashrc` or `.zshrc`)
2. A `.env` file in your home directory
3. A `.env` file in the current directory when running the CLI

## Usage

```bash
# Show help
dev --help

# Create a new project
dev new my-project

# List all projects
dev project list

# Initialize AI context for a project
dev context init
```

## Development

```bash
# Watch for changes and rebuild
npm run watch

# Run in development mode
npm run dev
```

## Architecture

The CLI has been designed with the following features:

- **Environment-agnostic execution**: Works from any directory without requiring a package.json
- **Intelligent path resolution**: Automatically finds the correct paths based on the CLI's location
- **Environment variable support**: Uses environment variables when available, with sensible defaults
- **Dotenv integration**: Can load configuration from .env files
- **Modular command structure**: Easy to add new commands and features

## Troubleshooting

### Common Issues

- **Command not found**: Make sure the CLI is properly linked with `npm link`
- **Path resolution issues**: Check that the environment variables are set correctly
- **Project creation fails**: Ensure you have write permissions in the projects directory

### Debug Mode

You can run the CLI in debug mode to see more information:

```bash
DEBUG=true dev <command>
```

## License

MIT
