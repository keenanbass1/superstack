# 🚀 Superstack Workflow Guide

> A practical reference guide for common commands and workflows in the Superstack development system

This guide serves as a quick reference for essential commands, patterns, and workflows you'll need while working with the Superstack system. It consolidates practical knowledge in one place for easy reference.

## 📋 Table of Contents

- [Git Workflow](#git-workflow)
- [Dev CLI Commands](#dev-cli-commands)
- [AI Context System](#ai-context-system)
- [Project Scaffolding](#project-scaffolding)
- [Common Terminal Commands](#common-terminal-commands)

---

## Git Workflow

### Core Git Commands

```bash
# Clone the repository
git clone https://github.com/yourusername/superstack.git ~/dev/superstack

# Check status of your working directory
git status

# Stage modified files
git add <file>           # Stage specific file
git add .                # Stage all changed files

# Commit changes with a descriptive message
git commit -m "feat(component): add user profile card"

# Push changes to remote
git push origin <branch>

# Pull latest changes
git pull --rebase origin main  # Rebase prevents unnecessary merge commits
```

### Branch Management

```bash
# List all branches
git branch -a

# Create and switch to a new branch
git checkout -b feature/new-feature

# Switch to an existing branch
git checkout main

# Delete a branch (after merging)
git branch -d feature/completed
```

### Effective Commit Messages

Follow the **Conventional Commits** format:

```
<type>(<scope>): <description>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting changes (no code change)
- `refactor`: Code changes that neither fix bugs nor add features
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(context): add typography principles module
fix(cli): resolve path issues in context push command
docs(readme): update installation instructions
refactor(scripts): improve error handling in setup
```

### Pull Request Workflow

1. Create a feature branch from `main`
2. Make changes and commit with descriptive messages
3. Push your branch to GitHub
4. Create a Pull Request with:
   - Clear title following conventional commit format
   - Description of changes
   - Reference to related issues
5. Request reviews and address feedback
6. Merge only when tests pass and reviews are approved

### Git Tips & Tricks

```bash
# View commit history
git log --oneline --graph --decorate

# Amend the most recent commit (before pushing)
git commit --amend

# Temporarily store changes without committing
git stash
git stash pop  # Apply and remove the stashed changes

# Discard uncommitted changes to a file
git checkout -- <file>

# Create a tag for release versions
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0
```

---

## Dev CLI Commands

The `dev` CLI is Superstack's custom command tool for workflow operations.

### Context Management

```bash
# Initialize project context
dev context init

# Push context to AI assistants
dev context push

# Validate context
dev context validate

# Edit context
dev context edit
```

### AI Assistance

```bash
# Ask a general question
dev ai query "How should I structure the user authentication flow?"

# Get assistance on a specific problem
dev ai solve "Implement a pagination component for the user list"

# Generate a code component
dev ai generate component UserProfile

# Review code with AI
dev ai review feature/user-management
```

### Project Management

```bash
# Create a new project from template
dev new my-project --template=next-app

# Start a development session log
dev log start "Implementing user authentication"

# End a session with a summary
dev log end --summary

# Create a project retrospective
dev retro create my-project
```

---

## AI Context System

The AI Context System enhances AI tools with structured knowledge modules.

### Using Context Modules with Cursor

Add AI-Context headers at the top of your file:

```typescript
// AI-Context: design/principles/spacing-systems
// AI-Context: design/ui-patterns/cards

function ProfileCard() {
  // Your component code
}
```

### Prompt Patterns for Cursor

```
# Component Creation
"Using the cards UI pattern from our context system, create a user profile component."

# Code Review
"Review this code against our spacing-systems principles."

# Refactoring
"Refactor this component to follow our design system's visual hierarchy guidelines."
```

### Creating New Context Modules

1. Choose the appropriate location in `docs/ai-context/`
2. Use the standard format (see template in `templates/`)
3. Follow the module structure:
   - Conceptual Foundation
   - Core Principles
   - Implementation Patterns
   - Decision Logic
   - Code Translation
   - Anti-Patterns
   - Reasoning Principles

---

## Project Scaffolding

### Creating New Projects

```bash
# Using the CLI
dev new my-app --template=next-app

# Manually
mkdir my-project
cd my-project
cp -r ~/dev/superstack/templates/project-types/next-app/template/* .
```

### Project Structure Best Practices

For a typical Next.js app:

```
my-app/
├── components/          # Reusable UI components
│   ├── ui/              # Generic UI elements
│   └── features/        # Feature-specific components
├── lib/                 # Utility functions and shared logic
├── pages/               # Next.js pages and API routes
├── public/              # Static assets
├── styles/              # Global styles and themes
├── contexts/            # React context providers
├── hooks/               # Custom React hooks
└── project-context.md   # AI context document
```

---

## Common Terminal Commands

### WSL Environment

```bash
# Update package lists
sudo apt update

# Install packages
sudo apt install <package-name>

# Navigate to Windows user directory from WSL
cd /mnt/c/Users/<username>

# Create symbolic link to Windows directory
ln -s /mnt/c/Users/<username>/Desktop/dev ~/dev
```

### Node.js & npm

```bash
# Install package globally
npm install -g <package>

# Install project dependencies
npm install

# Run development server
npm run dev

# Build project
npm run build

# Run tests
npm run test
```

### File Operations

```bash
# Create directory
mkdir -p path/to/directory

# Copy files or directories
cp -r source destination

# Move or rename files/directories
mv source destination

# Find files
find . -name "*.md" -type f

# Search file content
grep -r "searchterm" .
```

---

## Troubleshooting Common Issues

### Git Problems

- **Merge Conflicts**: Run `git status` to see affected files, then edit to resolve conflicts
- **Detached HEAD**: Run `git checkout main` to get back to the main branch
- **Accidental Commits**: Use `git reset HEAD~1` to undo the last commit (before pushing)

### Dev CLI Issues

- **Command Not Found**: Run `npm link` in the `scripts/dev` directory
- **Context Push Failing**: Check if you have a valid `project-context.md` file
- **Permission Errors**: Make sure you have write access to the config directory

### WSL Environment

- **Path Issues**: Use `/mnt/c/Users/...` to access Windows files from WSL
- **Node/npm Version**: Use `nvm` to manage Node.js versions
- **Terminal Performance**: Use Windows Terminal instead of legacy console

---

> This guide is a living document. Add to it as you discover useful commands and workflows, and it will grow into a valuable resource tailored to your needs. 