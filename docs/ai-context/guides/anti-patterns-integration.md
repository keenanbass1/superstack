# Integrating Anti-Patterns into Context Modules

This guide explains how to effectively integrate our anti-pattern capture system into the context modules, aligning with both our MCP-compatible format and our broader anti-pattern tracking system.

## Anti-Pattern Integration Strategy

Each context module should include a dedicated anti-patterns section that follows a consistent structure while connecting to our centralized anti-pattern repository.

### Standard Anti-Pattern Section Format

```markdown
<context name="[concept]_anti_patterns" priority="medium">
## Anti-Patterns and Common Mistakes

### 1. [Anti-Pattern Name] [AP-DOMAIN-NUM]

**Problem:**
[Clear description of the issue]

**Example:**
```
[Concrete example showing the problem]
```

**Why It Fails:**
- [Reason one]
- [Reason two]
- [Reason three]

**Better Approach:**
```
[Example of correct implementation]
```

**Severity:** [High/Medium/Low]
**AI-Specific:** [Yes/No]

### 2. [Second Anti-Pattern] [AP-DOMAIN-NUM]
[...]
</context>
```

## Anti-Pattern Classification System

Each anti-pattern should be categorized using our standardized classification:

1. **ID Format**: `AP-[DOMAIN]-[NUMBER]`
   - Example: `AP-REACT-002` (The second documented React anti-pattern)

2. **Domain Categories**:
   - `DESIGN` - Visual and UX design patterns
   - `CSS` - CSS and styling issues
   - `HTML` - HTML structure and semantics
   - `JS` - JavaScript language patterns
   - `REACT` - React-specific issues
   - `TS` - TypeScript-specific issues
   - `API` - API design and implementation
   - `STATE` - State management
   - `PERF` - Performance issues
   - `ACCESS` - Accessibility concerns
   - `AI` - AI interaction patterns

3. **Severity Levels**:
   - `High` - Causes significant bugs, performance issues, or UX problems
   - `Medium` - Creates maintenance problems or minor functional issues
   - `Low` - Primarily affects code quality or developer experience

4. **AI-Specific Flag**:
   - `Yes` - Particularly relevant in AI-assisted development
   - `No` - General development anti-pattern

## Anti-Patterns Repository Connection

Each module's anti-patterns section should connect to our centralized repository:

```markdown
For more anti-patterns related to [concept], see the [full anti-patterns collection](../../anti-patterns/[domain]/[specific-file].md).
```

## Cursor Prompt for Anti-Pattern Integration

When using Cursor to update modules, use this prompt for the anti-patterns section:

```
Create a comprehensive anti-patterns section for [concept] that:

1. Follows our MCP-compatible format with <context> tags and priority="medium" attribute
2. Identifies 4-6 common mistakes when implementing [concept]
3. For each anti-pattern:
   - Assigns a proper ID (AP-[DOMAIN]-[NUM])
   - Includes a clear problem statement
   - Provides a concrete, technical example
   - Explains why it's problematic (technical consequences)
   - Offers a better implementation approach
   - Assigns appropriate severity level
   - Flags if it's particularly relevant to AI-assisted development

4. Links to our centralized anti-pattern repository

Example structure:

<context name="[concept]_anti_patterns" priority="medium">
## Anti-Patterns and Common Mistakes

### 1. [Anti-Pattern Name] [AP-DOMAIN-NUM]

**Problem:**
[Clear description]

**Example:**
```code or visual example```

**Why It Fails:**
- [Technical reasons]

**Better Approach:**
```improved implementation```

**Severity:** [High/Medium/Low]
**AI-Specific:** [Yes/No]

### 2. [Second Anti-Pattern]
[...]
</context>
```

## Example: Updated Visual Hierarchy Anti-Patterns

Here's how an updated anti-patterns section looks for the Visual Hierarchy module:

```markdown
<context name="visual_hierarchy_anti_patterns" priority="medium">
## Anti-Patterns and Common Mistakes

### 1. Competing Focal Points [AP-DESIGN-001]

**Problem:**
Multiple elements with equal visual weight compete for attention, creating confusion about where to look first.

**Example:**
```
LARGE HEADLINE       EQUALLY LARGE GRAPHIC
                     
Bold red button      Another bold red button
```

**Why It Fails:**
- Creates visual competition and indecision
- Dilutes the impact of truly important elements
- Increases cognitive load as users must determine priority

**Better Approach:**
```
LARGE HEADLINE
[Supporting image that's clearly secondary]
                     
Bold red button      [Gray secondary button]
```

**Severity:** High
**AI-Specific:** Yes - AI often generates layouts with competing elements of equal prominence

### 2. Insufficient Contrast Between Hierarchy Levels [AP-DESIGN-003]

[Additional anti-patterns following the same format...]
</context>
```

## Anti-Pattern Collection Process

As you update modules with anti-pattern sections:

1. **Extract to Repository**: Copy each anti-pattern to the central repository
2. **Cross-Reference**: Add references between modules and repository
3. **Maintain IDs**: Ensure IDs remain consistent across all locations
4. **Track New Discoveries**: Document newly discovered anti-patterns from development logs or retrospectives

## Integration with Development Workflow

Connect the anti-pattern system with your development process:

1. **Log Integration**: Use the `dev log add` command with anti-pattern tagging
   ```bash
   dev log add "Found nested ternary readability issues in AI-generated code" --anti-pattern
   ```

2. **Retro Integration**: Include anti-pattern discovery in retrospective templates
   ```markdown
   ## Anti-Patterns Discovered
   | Pattern ID | Description | Context | Solution Applied |
   |------------|-------------|---------|------------------|
   | AP-JS-012  | Nested ternaries | User profile logic | Refactored to if/else |
   ```

3. **CLI Extraction**: Use the extraction command to pull from logs and retros
   ```bash
   dev extract anti-patterns --from-logs --since="2 weeks ago"
   ```

By following this integration strategy, you'll create a comprehensive, structured approach to documenting and preventing anti-patterns while seamlessly connecting them to your broader context system.
