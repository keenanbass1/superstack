# Contributing to the AI Context System

This guide explains how to create new context modules for the AI context system. Following these guidelines ensures that your modules will integrate well with existing content and provide maximum value for AI tools.

## Creating New Context Modules

### 1. Choose the Right Location

Place your module in the appropriate subdirectory:

- **design/principles/** - Fundamental design concepts
- **design/ui-patterns/** - Interface component patterns
- **design/ux-patterns/** - Experience design patterns
- **development/patterns/** - Code patterns and architectures
- **development/practices/** - Development methodologies
- **system/cli/** - CLI tool usage and patterns
- **system/ai/** - AI interaction patterns

If your module doesn't fit into an existing category, consider creating a new subdirectory after discussing with the team.

### 2. Use the Standard Format

Each context module should follow this structure:

```markdown
# Title of Concept

This context module explains [concept] in [domain], providing principles and implementation patterns for [primary purpose].

## Conceptual Foundation

[1-2 paragraphs explaining the fundamental concept, its purpose, and its importance]

## Core Principles

### 1. [First Principle]
- [Key point about this principle]
- [Another key point]
- [Additional detail]

### 2. [Second Principle]
- [Key points...]

### 3. [Third Principle]
- [Key points...]

[Continue with 4-5 core principles]

## Implementation Patterns

### [Pattern Category 1]

#### [Specific Pattern Type]
- **[Element]**: [Specification]
- **[Element]**: [Specification]
- **[Element]**: [Specification]

### [Pattern Category 2]

[Code examples or structured specifications]

## Decision Logic for Implementation

When [implementing/designing/choosing] [concept]:

1. **[Decision Step 1]**
   - [Question to consider]
   - [Another question]
   - [Additional consideration]

2. **[Decision Step 2]**
   - [Questions and considerations]

3. **[Decision Step 3]**
   - [Questions and considerations]

4. **[Decision Step 4]**
   - [Questions and considerations]

## Code Translation

### [Implementation Approach 1]
```code
[Code example with comments]
```

### [Implementation Approach 2]
```code
[Alternative implementation]
```

## Anti-Patterns

### [Anti-Pattern 1]
- [Description of problematic practice]
- [Why it's problematic]
- [How to avoid or fix]

### [Anti-Pattern 2]
- [Description and remediation]

[Continue with 3-5 anti-patterns]

## Reasoning Principles

[Concept] is effective because it:

1. **[Reasoning Principle 1]** - [Brief explanation]
2. **[Reasoning Principle 2]** - [Brief explanation]
3. **[Reasoning Principle 3]** - [Brief explanation]
4. **[Reasoning Principle 4]** - [Brief explanation]
5. **[Reasoning Principle 5]** - [Brief explanation]

## Related Concepts

- **[Related Concept 1]** - [Brief explanation of relationship]
- **[Related Concept 2]** - [Brief explanation of relationship]
- **[Related Concept 3]** - [Brief explanation of relationship]
- **[Related Concept 4]** - [Brief explanation of relationship]
- **[Related Concept 5]** - [Brief explanation of relationship]
```

### 3. Writing Effective Context Modules

#### Focus on AI Understanding
- Write for AI consumption, not just human readers
- Explain concepts clearly and explicitly
- Provide reasoning and motivation, not just facts
- Connect concepts to implementation patterns

#### Use Structured Knowledge
- Break concepts into clear, labeled sections
- Use hierarchical organization (headings, lists)
- Provide explicit decision trees when appropriate
- Include both high-level concepts and concrete examples

#### Include Code Translations
- Provide implementation examples in appropriate languages
- Comment code examples to explain the connection to concepts
- Include multiple implementation approaches when relevant
- Show how concepts map to specific code patterns

#### Document Anti-Patterns
- Explain common mistakes and misconceptions
- Provide clear reasoning for why they're problematic
- Offer better alternatives to each anti-pattern
- Include visual examples if helpful (described textually)

### 4. Reviewing and Testing Modules

Before submitting a new context module:

1. **Self-Review**: Ensure your module follows the standard format
2. **AI Test**: Test your module with AI tools to verify effectiveness
   - Try prompting Cursor AI with a task related to your module
   - Test with Claude or GPT to verify knowledge transfer
   - Check if AI correctly applies the principles you've documented

3. **Peer Review**: Have a colleague review the module
4. **Revise Based on Feedback**: Iterate based on real-world testing

### 5. Updating Existing Modules

When updating existing modules:

1. **Preserve Structure**: Maintain the consistent format
2. **Clearly Mark Updates**: Note significant changes in commit messages
3. **Update Related Modules**: Check for and update any related modules
4. **Test After Changes**: Verify the updated module still works effectively with AI tools

## Common Domain Extensions

### Design Domain
- Color theory
- Responsive design
- Accessibility
- Animation principles
- Design systems
- Information architecture

### Development Domain
- State management
- Error handling
- Performance optimization
- Testing strategies
- API design
- Security practices

### System Domain
- Workflow optimization
- Context management
- Prompt engineering
- Knowledge capture
- Tool integration

## Example: Creating a Button Component Module

1. Create file at `design/ui-patterns/buttons.md`
2. Follow the standard format
3. Include:
   - Button variants (primary, secondary, tertiary)
   - States (default, hover, active, disabled)
   - Sizing (small, medium, large)
   - Implementation examples in CSS/React/Vue
   - Decision logic for when to use each variant
   - Anti-patterns in button design

4. Test with AI tools on button implementation tasks
5. Submit for review

## Help and Support

If you need help creating context modules:

- Check existing modules for inspiration
- Review the schema definition in `schemas/context-module-schema.json`
- Use the module template in `templates/context-module-template.md`
- Ask for feedback on module drafts before finalizing
