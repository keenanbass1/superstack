# Cursor AI Prompts for Context Module Updates

This document provides a sequence of carefully crafted prompts for Cursor AI to help you systematically update your existing AI context modules to the new MCP-compatible format.

## Initial Prompts for Getting Started

### 1. Module Analysis Prompt

```
I'm updating my AI context modules to follow an MCP-compatible structure with proper context tags and priority attributes. Please analyze this module and identify:

1. The main concept being covered
2. Key principles, implementation patterns, and code examples
3. Any missing sections based on our new format:
   - Metadata (priority, domain, target models, related modules)
   - Module overview
   - Contextual chunks with priority tags
   - Anti-patterns section
   - Model-specific implementation notes
   - Practical examples

Outline a transformation plan for converting this to the new format.
```

### 2. Metadata Generation Prompt

```
Create a metadata section for this module with:

- Priority level (high/medium/low based on concept importance)
- Domain classification (design/development/system)
- Target models (claude, gpt, cursor-ai)
- Related modules

Then write a 2-3 sentence module overview that clearly explains what this module covers and why it's valuable for AI-assisted development.
```

## Section-Specific Prompts

### 3. Core Concept Transformation Prompt

```
Transform the core concept explanation into an MCP-compatible format using:

<context name="[concept_name]_definition" priority="high">
## Conceptual Foundation

[Content here]
</context>

Make sure the definition is clear, comprehensive, and technically precise.
```

### 4. Core Principles Transformation Prompt

```
Convert the principles section into an MCP-compatible format:

<context name="[concept_name]_core_principles" priority="high">
## Core Principles

### 1. [First Principle]
[Explanation]

**Implementation Guidelines:**
- [Guideline details]

**Example:**
[Example application]

### 2. [Second Principle]
[...]
</context>

Ensure each principle includes:
- Clear explanation of the concept
- Implementation guidelines
- Concrete examples
```

### 5. Implementation Patterns Prompt

```
Create or transform the implementation patterns section:

<context name="[concept_name]_implementation_patterns" priority="medium">
## Implementation Patterns

[Content organized by pattern types, with examples]
</context>

Focus on practical, technical implementations showing how to apply the principles in real-world scenarios.
```

### 6. Decision Logic Prompt

```
Develop a clear decision framework section:

<context name="[concept_name]_decision_logic" priority="medium">
## Decision Logic for Implementation

When implementing [concept], follow this decision framework:

### Step 1: [First Decision Point]
```
Decision tree or process
```

### Step 2: [Second Decision Point]
[...]
</context>

Create step-by-step guidance that helps developers make implementation decisions.
```

### 7. Code Implementation Prompt

```
Format the code implementation examples properly:

<context name="[concept_name]_code_implementation" priority="medium">
## Code Implementation

### [Implementation Aspect 1]
```code
// Code example with detailed comments
```

### [Implementation Aspect 2]
```code
// Second example
```
</context>

Ensure code examples:
- Follow modern best practices
- Include thorough comments explaining implementation
- Demonstrate all key principles
- Show practical variations if applicable
```

### 8. Anti-Patterns Section Prompt

```
Create a comprehensive anti-patterns section:

<context name="[concept_name]_anti_patterns" priority="medium">
## Anti-Patterns and Common Mistakes

### 1. [Anti-Pattern Name]

**Problem:**
[Clear description]

**Example:**
[Concrete example]

**Why It Fails:**
- [Failure reason 1]
- [Failure reason 2]

**Better Approach:**
[Correct implementation]

### 2. [Second Anti-Pattern]
[...]
</context>

Include 4-6 realistic anti-patterns with concrete examples and solutions.
```

### 9. Model-Specific Notes Prompt

```
Add implementation notes for different AI models:

<context name="[concept_name]_model_specific_notes" priority="low">
## Model-Specific Implementation Notes

### For Claude (Anthropic)
[Specific considerations and approaches]

### For GPT (OpenAI)
[Specific considerations and approaches]

### For Local Models
[Adaptation considerations]
</context>

Focus on practical differences in how to use this knowledge with different AI systems.
```

### 10. Related Concepts Prompt

```
Create a related concepts section:

<context name="[concept_name]_related_concepts" priority="low">
## Related Concepts

- **[Related Concept 1]** - [Brief description and relationship]
- **[Related Concept 2]** - [Brief description and relationship]
[...]
</context>

Identify 5-8 related concepts that developers should consider alongside this topic.
```

## Final Integration Prompts

### 11. Practical Examples Prompt

```
Create a practical examples section with before/after scenarios:

<context name="[concept_name]_practical_examples" priority="medium">
## Practical Examples

### Example 1: [Scenario Name]

**Before**: [Problematic implementation]
```
[Visual or code representation]
```

**After**: [Improved implementation]
```
[Visual or code representation]
```

[Explanation of improvements]

### Example 2: [Second Scenario]
[...]
</context>

Develop 2-3 realistic examples that clearly demonstrate application of the principles.
```

### 12. Module Usage Prompt

```
Add a final "Using This Module" section:

## Using This Module

This module can be referenced when:
- [Usage scenario 1]
- [Usage scenario 2]
- [Usage scenario 3]
[...]

[Closing advice on application]

Last Updated: April 13, 2025
```

### 13. Complete Module Review Prompt

```
Review the complete updated module and verify:

1. All sections are wrapped in appropriate <context> tags with name and priority attributes
2. Content flows logically from most to least important information
3. All examples are technically precise and implementation-focused
4. Anti-patterns provide clear problems and solutions
5. Code examples follow best practices with helpful comments
6. The overall organization follows our new structure: metadata, overview, core concepts (high priority), implementation details (medium priority), and supporting information (low priority)

Identify any remaining issues or inconsistencies to address.
```

## Batch Processing Strategy

For efficiently updating multiple modules:

```
I have [X] modules to update to our new MCP-compatible format. Let's create a systematic approach:

1. For each module, we'll follow the 13-step prompt sequence
2. We'll prioritize updating the most frequently used modules first:
   - [Module 1]
   - [Module 2]
   - [Module 3]

For this session, let's start with [Module Name]. Here's the current content:

[Paste module content]
```

## Anti-Patterns Integration Prompt

Based on our recent work on anti-patterns, here's a specialized prompt for that section:

```
Integrate our anti-patterns capture system into this module by:

1. Creating a comprehensive anti-patterns section that includes:
   - Common mistakes in implementing [concept]
   - Clear problem/solution pairs
   - Examples showing both problematic and improved approaches
   - Technical explanations of why certain approaches fail

2. Linking to our broader anti-patterns system:
   - Reference the anti-patterns collection where appropriate
   - Use consistent naming conventions (AP-[DOMAIN]-[NUMBER])
   - Include severity levels (high/medium/low)
   - Flag AI-specific anti-patterns that are particularly relevant for AI-assisted development

Format this as a proper <context> block with medium priority.
```

## Additional Tips for Effective Cursor Assistance

1. **Provide Context First**: Before starting updates, give Cursor a quick overview of the MCP system and your goals
2. **Work Incrementally**: Update section by section rather than the entire module at once
3. **Review and Refine**: After each section update, review and ask Cursor to refine as needed
4. **Focus on Technical Precision**: Emphasize that examples should be technically sound and implementable
5. **Validate Structure**: Periodically ask Cursor to verify the correct use of context tags and priorities

By following these prompts sequentially, you can systematically update all your AI context modules to the new MCP-compatible format while maintaining high technical quality and consistency across the system.
