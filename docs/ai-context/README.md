# AI Context System

> A bombproof context scaffolding to enhance AI tools with structured, modular knowledge

This directory contains AI-optimized knowledge modules designed to improve the capabilities of AI assistants like Cursor AI, Claude, and GPT. The system is built to be modular, extensible, and focused on providing high-quality context for AI-augmented development workflows.

## System Purpose

The AI Context System serves to:

1. **Enhance AI Understanding** - Provide structured knowledge that helps AI models make better decisions
2. **Ensure Consistency** - Create shared understanding between developers and AI assistants
3. **Reduce Hallucinations** - Give AI concrete, accurate information to work from
4. **Accelerate Workflows** - Create reusable knowledge modules for common tasks
5. **Improve Quality** - Guide AI toward established best practices and patterns

## Directory Structure

```
ai-context/
├── README.md                      # This guide
├── design/                        # Design knowledge domain
│   ├── principles/                # Fundamental design concepts
│   ├── ui-patterns/               # Interface component patterns
│   └── ux-patterns/               # Experience design patterns
├── development/                   # Development knowledge domain
│   ├── patterns/                  # Code patterns and architectures
│   ├── practices/                 # Development methodologies
│   └── tech-specific/             # Framework/language specifics
├── system/                        # Workflow system knowledge
│   ├── cli/                       # CLI tool usage and patterns
│   ├── ai/                        # AI interaction patterns
│   └── workflow/                  # Development workflow patterns
├── guides/                        # System process documentation
│   └── CONTEXT-MODULE-WORKFLOW.md # Module creation workflow
├── templates/                     # Module templates
└── schemas/                       # Knowledge structure definitions
```

## Module Format

Each knowledge module follows a consistent structure designed for AI consumption:

1. **Conceptual Definition** - Clear explanation of the concept
2. **Core Principles** - Fundamental rules and guidelines
3. **Implementation Patterns** - Practical application examples
4. **Decision Logic** - How to make choices about this concept
5. **Code Translation** - How the concept maps to implementation
6. **Anti-Patterns** - Common mistakes to avoid
7. **Reasoning Principles** - The "why" behind the guidelines

## Usage

### With Cursor AI

```typescript
// At the top of your file or in a comment block, add:
// AI-Context: design/principles/visual-hierarchy
// AI-Context: design/ui-patterns/cards

function ProductCard() {
  // Implementation here
}
```

### With Claude/GPT

```
I'd like you to help me with a design task. Please use the following context:

<context>
[Paste relevant context module content here]
</context>
```

### With the Dev CLI

```bash
# Add context to current session
dev context add design/principles/spacing

# Add multiple context modules
dev context add-group ui-components

# List available context modules
dev context list
```

## Contributing Guidelines

When adding new context modules:

1. **Follow the established structure** for consistency
2. **Focus on universal principles** rather than tool-specific details
3. **Include concrete examples** that demonstrate concepts
4. **Document the reasoning** behind guidelines ("why" not just "what")
5. **Keep modules modular** and focused on single concerns
6. **Test with AI tools** to verify effectiveness

For a detailed process on creating high-quality modules, see the [Context Module Workflow Guide](./guides/CONTEXT-MODULE-WORKFLOW.md).

## Available Knowledge Modules

The system currently includes modules covering:

### Design Principles
- [Visual Hierarchy](./design/principles/visual-hierarchy.md)
- [Spacing Systems](./design/principles/spacing-systems.md)
- [Typography](./design/principles/typography.md)

### UI Patterns
- [Buttons](./design/ui-patterns/buttons.md)
- [Cards](./design/ui-patterns/cards.md)

See individual directories for complete module listings.
