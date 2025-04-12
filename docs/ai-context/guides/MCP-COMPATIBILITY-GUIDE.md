# Model Context Protocol (MCP) Compatibility Guide

> This guide explains how to structure context modules to be fully compatible with Anthropic's Model Context Protocol (MCP) while maintaining effectiveness across other AI models.

## What is MCP?

Model Context Protocol (MCP) is an open standard developed by Anthropic that standardizes how applications provide context to Large Language Models (LLMs). Think of MCP like a USB-C port for AI applications - it provides a standardized way to connect AI models to various data sources and tools.

Key benefits of MCP include:
- More consistent handling of context information
- Better prioritization of important information
- Improved ability to retrieve relevant context
- Standardized integration with external tools and data sources

## MCP Structure for Context Modules

Our context modules now follow MCP guidelines to ensure optimal performance with Claude and future compatibility with other models that adopt MCP.

### Basic MCP Tag Format

```markdown
<context name="descriptive_name" priority="high|medium|low">
Content goes here...
</context>
```

Each module should:
1. Begin with a module title and brief overview
2. Include a metadata section
3. Divide content into logical chunks using context tags
4. Assign appropriate priority levels
5. Use descriptive names for each chunk

### Metadata Section

At the top of each module, include a metadata section:

```markdown
## Metadata
- **Priority:** high
- **Domain:** design
- **Target Models:** claude, gpt
- **Related Modules:** typography, spacing-systems, color-theory
```

### Context Tag Priorities

MCP uses three priority levels:

| Priority | Usage | Examples |
|----------|-------|----------|
| **High** | Critical foundational information | Concept definitions, core principles, fundamental theory |
| **Medium** | Important but not essential information | Implementation details, common patterns, code examples |
| **Low** | Supplementary or advanced information | Edge cases, deep theory, model-specific notes |

### Context Chunk Naming

Use descriptive, semantic names that indicate the content's purpose:

```markdown
<context name="visual_hierarchy_definition" priority="high">
```

Name format should be:
- All lowercase
- Underscores between words
- Descriptive of content purpose
- Consistent naming pattern across modules

### Context Chunk Sizing

Balance chunk size for optimal processing:

- **Too small**: May lack sufficient context to be useful
- **Too large**: May dilute importance of key information

Guidelines:
- High-priority chunks: 200-500 words
- Medium-priority chunks: 500-1000 words
- Low-priority chunks: No strict limit, but be mindful of relevance
- Code chunks: Complete, working examples only

## Structuring Content for MCP

### Module Template with MCP Tags

```markdown
# Module Title

> Brief overview of the module

## Metadata
- **Priority:** high
- **Domain:** category
- **Target Models:** claude, gpt
- **Related Modules:** related-module-1, related-module-2

## Module Overview
Brief description of the module contents and purpose.

<context name="concept_definition" priority="high">
## Conceptual Foundation
Fundamental concept explanation...
</context>

<context name="core_principles" priority="high">
## Core Principles
Key principles that define the concept...
</context>

<context name="implementation_patterns" priority="medium">
## Implementation Patterns
Practical application examples...
</context>

<context name="decision_framework" priority="medium">
## Decision Logic
Step-by-step decision frameworks...
</context>

<context name="code_examples" priority="medium">
## Code Implementation
Example code with explanation...
</context>

<context name="anti_patterns" priority="medium">
## Anti-Patterns
Common mistakes to avoid...
</context>

<context name="reasoning_principles" priority="low">
## Reasoning Principles
Why these guidelines work...
</context>

<context name="model_specific_notes" priority="low">
## Model-Specific Implementation Notes
Guidance for different AI models...
</context>

<context name="related_concepts" priority="low">
## Related Concepts
Connections to other knowledge areas...
</context>
```

### Chunk Organization Principles

1. **Cohesion**: Each chunk should cover a cohesive topic
2. **Completeness**: Chunks should be self-contained where possible
3. **Hierarchy**: Follow a logical progression from general to specific
4. **Separation of Concerns**: Different aspects in different chunks
5. **Prioritization**: Most important information in highest priority chunks

## Cross-Model Compatibility

While optimizing for MCP, we need to maintain compatibility with other AI models:

### For Claude (Anthropic)
- Fully MCP-compatible with proper tags
- Precise, detailed information works well
- Technical explanations can be more advanced

### For GPT (OpenAI)
- MCP tags do not interfere with processing
- May benefit from more examples
- Works well with structured information

### For Cursor AI
- Primarily code-focused chunks are most valuable
- Implementation patterns should be practical
- Include IDE-specific considerations where relevant

### For Local Models
- May need simpler explanations
- More basic examples
- Less reliance on advanced reasoning

## Testing MCP Compatibility

Before finalizing a module, test its MCP compatibility:

1. **Structure Validation**:
   - Verify all content is within properly formatted context tags
   - Check that tag names are descriptive and follow conventions
   - Ensure priority levels are appropriately assigned

2. **Claude Testing**:
   - Test with Claude to verify context recognition
   - Check if specific chunks can be referenced correctly
   - Verify priority handling works as expected

3. **Cross-Model Testing**:
   - Test with GPT to ensure content is still effective
   - Test with Cursor AI for code-related modules
   - Verify no degradation with other models

## Common MCP Issues and Solutions

| Issue | Solution |
|-------|----------|
| Overlapping content between chunks | Refine chunk boundaries, eliminate redundancy |
| Inconsistent priority assignments | Review prioritization criteria and standardize |
| Tags breaking markdown formatting | Ensure proper line breaks before and after tags |
| Chunks too large for effective processing | Break into more focused, smaller chunks |
| Context reference issues | Ensure descriptive, unique chunk names |

## MCP Implementation with CLI

Our CLI tool supports MCP formatting:

```bash
# Push to Claude with MCP formatting
dev context push-claude

# Check MCP compatibility of a module
dev context validate-mcp design/principles/visual-hierarchy

# List all MCP chunks in a module
dev context list-chunks design/principles/visual-hierarchy
```

## Advanced MCP Features

As MCP evolves, we'll incorporate additional features:

- **Tool Integration**: Connecting contexts to specific tools
- **User Context**: Handling user-specific information
- **Interactive Elements**: Action buttons, form inputs
- **Visual Components**: Structured visual elements

These will be documented as they become available and stable.

## Resources

- [Official MCP Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/mcp)
- [Anthropic Claude Documentation](https://docs.anthropic.com/)
- [Sample MCP Modules](../examples/)

---

*Last Updated: April 13, 2025*
