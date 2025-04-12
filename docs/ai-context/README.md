# AI Context System

> A bombproof context scaffolding to enhance AI tools with structured, modular knowledge optimized for MCP compatibility

This directory contains AI-optimized knowledge modules designed to improve the capabilities of AI assistants like Claude, GPT, and Cursor AI. The system is built to be modular, extensible, and focused on providing high-quality context for AI-augmented development workflows.

## System Purpose

The AI Context System serves to:

1. **Enhance AI Understanding** - Provide structured knowledge that helps AI models make better decisions
2. **Ensure Consistency** - Create shared understanding between developers and AI assistants
3. **Reduce Hallucinations** - Give AI concrete, accurate information to work from
4. **Accelerate Workflows** - Create reusable knowledge modules for common tasks
5. **Improve Quality** - Guide AI toward established best practices and patterns
6. **Optimize for AI Models** - Format content specifically for different AI architectures

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
├── schemas/                       # Knowledge structure definitions
└── resources/                     # Additional resource references
```

## Updated Module Format

Each knowledge module now follows our enhanced structure optimized for AI consumption:

1. **Metadata Section** - Priority, domain, target models, and related modules
2. **Module Overview** - Brief summary of the module's purpose and content
3. **Contextual Chunks** - Information divided into discrete MCP-compatible blocks:
   - Each chunk wrapped in `<context>` tags with name and priority attributes
   - Information organized from highest to lowest priority
   - Chunks sized appropriately for model processing
4. **Conceptual Foundation** - Clear explanation of the concept (high priority)
5. **Core Principles** - Fundamental rules and guidelines (high priority)
6. **Implementation Patterns** - Practical application examples (medium priority)
7. **Decision Logic** - Step-by-step decision frameworks (medium priority)
8. **Code Translation** - Implementation examples with commentary (medium priority)
9. **Anti-Patterns** - Common mistakes to avoid (medium priority)
10. **Reasoning Principles** - The "why" behind the guidelines (low priority)
11. **Model-Specific Notes** - Tailored guidance for different AI models (low priority)
12. **Related Concepts** - Connections to other knowledge areas (low priority)

## MCP Compatibility

Our modules are now fully compatible with Anthropic's Model Context Protocol (MCP), which standardizes how applications provide context to LLMs. Key aspects include:

- **Context Tags**: Information wrapped in `<context>` tags
- **Priority Attributes**: Each chunk assigned high/medium/low priority
- **Naming Attributes**: Descriptive names for each context chunk
- **Chunking Strategy**: Information divided into logical, focused sections
- **Structured Format**: Consistent organization across all modules

## Usage

### With Claude (MCP-Compatible)

```
I'd like you to help me with a design task. The context will be automatically structured for Claude's MCP system.

<context name="visual_hierarchy_definition" priority="high">
# Visual Hierarchy

Visual hierarchy is the deliberate arrangement of elements to show their order of importance, guiding users through content in an intended sequence.
</context>

Based on visual hierarchy principles, please help me design a product listing page.
```

### With Other AI Models

```
I'd like you to help me with a design task. Please use the following context:

# Visual Hierarchy

Visual hierarchy is the deliberate arrangement of elements to show their order of importance, guiding users through content in an intended sequence.

[Additional content...]
```

### With the Dev CLI

```bash
# Add context to current session
dev context add design/principles/visual-hierarchy

# Add multiple context modules
dev context add-group ui-components

# Push to Claude with MCP formatting
dev context push-claude

# Push to other AI tools
dev context push-cursor
```

## Contributing Guidelines

When adding new context modules:

1. **Follow the enhanced MCP-compatible structure**
2. **Use proper context tags and priority attributes**
3. **Include model-specific guidance** where relevant
4. **Organize information in logical chunks** from highest to lowest priority
5. **Provide step-by-step decision frameworks**
6. **Include clear examples** that demonstrate principles in action
7. **Document anti-patterns** with explanations of why they fail
8. **Test with multiple AI tools** to verify effectiveness

For a detailed process on creating high-quality modules, see the [Context Module Workflow Guide](./guides/CONTEXT-MODULE-WORKFLOW.md).

## Advanced Features

### Few-Shot Learning Patterns

Modules now include explicit few-shot learning examples that demonstrate:
- Before/after comparisons
- Problem/solution pairs
- Step-by-step implementation examples

### Structured Reasoning Pathways

Decision logic sections provide explicit reasoning frameworks:
- Decision trees with branching logic
- Sequential decision steps
- Evaluation criteria for different options

### Context Management Optimization

Information is structured to maximize efficiency:
- Most critical information appears first
- Related concepts are grouped together
- Clear section breaks improve navigation

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

---

*Last Updated: April 13, 2025*
