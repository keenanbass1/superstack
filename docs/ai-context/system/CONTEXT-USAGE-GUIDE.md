# Guide: Effective Context Injection for AI Tools

This guide explains how to effectively use the context modules with different AI tools to enhance their capabilities.

## Fundamentals of Context Injection

### What is Context Injection?
Context injection is the process of providing structured knowledge to AI tools to improve their understanding of specific domains and tasks. Well-structured context helps AI tools:

- Make more informed decisions
- Follow established patterns and best practices
- Apply domain-specific knowledge
- Reduce erroneous outputs and hallucinations

### When to Use Context Injection
Use context injection when:

- Working on specialized tasks requiring domain expertise
- Implementing specific patterns or components
- Needing consistent application of principles
- Seeking advice on complex decisions
- Generating code that adheres to specific standards

## Context Injection Methods

### 1. Cursor AI Integration

Cursor AI supports context via special comment blocks:

```typescript
// AI-Context: design/principles/visual-hierarchy
// AI-Context: design/ui-patterns/cards

function ProductCard() {
  // Implementation here
}
```

You can also use multi-line comments:

```typescript
/*
AI-Context: design/principles/visual-hierarchy
AI-Context: design/ui-patterns/cards
AI-Context: design/principles/spacing
*/
```

### 2. Claude Integration

For Claude, use the following format:

```
I need help designing a product page. Please use the following context information:

<context>
[Copy and paste the content of relevant context modules here]
</context>

Now, could you help me design the product card component with proper visual hierarchy?
```

### 3. GPT Integration

For GPT, use a similar approach:

```
I'd like you to act as a design system expert with the following knowledge:

[Copy and paste the content of relevant context modules here]

Based on this information, please review my navigation component design.
```

### 4. CLI-Based Context Management

The `dev` CLI tool provides commands for context management:

```bash
# Add specific context modules to your session
dev context add design/principles/visual-hierarchy
dev context add design/ui-patterns/cards

# View currently active contexts
dev context list

# Save a context group for reuse
dev context create-group ui-basics design/principles/visual-hierarchy design/principles/spacing design/ui-patterns/buttons

# Apply a saved context group
dev context add-group ui-basics

# Generate context-aware code
dev generate component ProductCard --context=design/ui-patterns/cards
```

## Context Selection Strategy

### Single-Concept Focus
For targeted assistance with a specific concept:
```
dev context add design/principles/typography
```

### Complementary Concepts
For tasks involving multiple related concepts:
```
dev context add design/ui-patterns/forms
dev context add design/principles/accessibility
```

### Full-Stack Design
For comprehensive design tasks:
```
dev context add-group ui-design-system
```

## Context Composition Patterns

### 1. Layered Context

Build context in layers of increasing specificity:

1. **Foundation Layer** - Basic principles (visual hierarchy, spacing)
2. **Pattern Layer** - Component patterns (cards, buttons)
3. **Implementation Layer** - Specific implementation details (React components)

### 2. Problem-Solution Pairing

Combine contexts that define:
1. The problem domain
2. Design approaches
3. Implementation patterns

Example:
```
dev context add design/ux-patterns/data-tables
dev context add design/principles/information-density
dev context add design/ui-patterns/pagination
```

### 3. Constraint-Focused Context

When working within specific constraints:
```
dev context add design/principles/accessibility
dev context add design/principles/performance
```

## Optimization Tips

### Keep Context Relevant
- Only include directly relevant context modules
- Avoid exceeding token limits with too much context
- Prioritize specific over general content when space is limited

### Provide Clear Instructions
- Specify how the context should be applied
- Indicate priority when multiple principles apply
- Highlight any exceptions or special considerations

### Iterate Based on Results
- Adjust context selection if AI responses aren't optimal
- Add more specific context if outputs are too generic
- Remove confusing context if outputs show misunderstanding

## Example: Complete Workflow

```bash
# Starting a new component design
cd ~/projects/my-app

# Add relevant design context
dev context add design/principles/visual-hierarchy
dev context add design/ui-patterns/cards
dev context add design/principles/accessibility

# Generate component scaffold with context
dev generate component ProductCard

# Open in editor with context available to Cursor AI
cursor src/components/ProductCard.tsx

# Implementation with context-aware assistance
# Cursor AI now has access to the design principles
```

## Troubleshooting

### Context Not Applied
- Verify correct path to context module
- Check for syntax errors in context directive
- Ensure tool supports the context injection method

### Contradictory Outputs
- Check for conflicting principles in provided contexts
- Explicitly state which principles take precedence
- Break task into smaller parts with focused context

### Excessive Token Usage
- Use more concise context modules
- Split task into sequential interactions
- Prioritize most relevant context only

## Advanced: Context Pipeline Integration

For teams integrating context into development pipelines:

1. **Document Pre-Processing**: Automatically include context in generated docs
2. **Git Hooks**: Attach context to commit/PR templates
3. **IDE Extensions**: Create snippets for quick context insertion
4. **Automated Context Selection**: Use project metadata to suggest contexts
