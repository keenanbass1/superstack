# {{TITLE}}

> {{BRIEF_DESCRIPTION}}

## Metadata
- **Priority:** {{PRIORITY}} <!-- high, medium, or low -->
- **Domain:** {{DOMAIN}} <!-- design, development, system, etc. -->
- **Target Models:** {{TARGET_MODELS}} <!-- claude, gpt, cursor, etc. -->
- **Related Modules:** {{RELATED_MODULES}} <!-- comma-separated list -->

## Module Overview

{{MODULE_OVERVIEW_PARAGRAPH}}

<!-- 
NOTE: This module is structured following optimal prompt engineering principles:
1. Each section begins with a clear conceptual foundation
2. Content is organized from most to least important
3. Examples use few-shot patterns to demonstrate application
4. Decision trees guide practical implementation
5. Anti-patterns show common mistakes to avoid
6. Model-specific notes provide tailored guidance
-->

<context name="{{CONCEPT_NAME}}_definition" priority="high">
## Conceptual Foundation

{{CONCEPT_DEFINITION}}

{{WHY_IT_MATTERS}}

{{KEY_CHARACTERISTICS}}
</context>

<context name="{{CONCEPT_NAME}}_core_principles" priority="high">
## Core Principles

### 1. {{PRINCIPLE_1_NAME}}
{{PRINCIPLE_1_DESCRIPTION}}

**Implementation Guidelines:**
- {{GUIDELINE_1}}
- {{GUIDELINE_2}}
- {{GUIDELINE_3}}

**Example: {{EXAMPLE_1_TITLE}}**
```
{{EXAMPLE_1_CONTENT}}
```

### 2. {{PRINCIPLE_2_NAME}}
{{PRINCIPLE_2_DESCRIPTION}}

**Implementation Guidelines:**
- {{GUIDELINE_1}}
- {{GUIDELINE_2}}
- {{GUIDELINE_3}}

**Example: {{EXAMPLE_2_TITLE}}**
```
{{EXAMPLE_2_CONTENT}}
```

### 3. {{PRINCIPLE_3_NAME}}
{{PRINCIPLE_3_DESCRIPTION}}

**Implementation Guidelines:**
- {{GUIDELINE_1}}
- {{GUIDELINE_2}}
- {{GUIDELINE_3}}

**Example: {{EXAMPLE_3_TITLE}}**
```
{{EXAMPLE_3_CONTENT}}
```

<!-- Add more principles as needed -->
</context>

<context name="{{CONCEPT_NAME}}_implementation_patterns" priority="medium">
## Implementation Patterns

### Common {{CONCEPT_NAME}} Patterns

#### {{PATTERN_1_NAME}}
```
{{PATTERN_1_STRUCTURE}}
```

#### {{PATTERN_2_NAME}}
```
{{PATTERN_2_STRUCTURE}}
```

### Typical Application Sequence

1. **{{APPLICATION_STEP_1}}** - {{STEP_1_DESCRIPTION}}
   - Example: {{STEP_1_EXAMPLE}}
   - Properties: {{STEP_1_PROPERTIES}}

2. **{{APPLICATION_STEP_2}}** - {{STEP_2_DESCRIPTION}}
   - Example: {{STEP_2_EXAMPLE}}
   - Properties: {{STEP_2_PROPERTIES}}

3. **{{APPLICATION_STEP_3}}** - {{STEP_3_DESCRIPTION}}
   - Example: {{STEP_3_EXAMPLE}}
   - Properties: {{STEP_3_PROPERTIES}}

### Practical Examples

#### Example 1: {{PRACTICAL_EXAMPLE_1_TITLE}}

**Before:**
```
{{BEFORE_EXAMPLE_1}}
```

**After:**
```
{{AFTER_EXAMPLE_1}}
```

**Key Improvements:**
- {{IMPROVEMENT_1}}
- {{IMPROVEMENT_2}}
- {{IMPROVEMENT_3}}

#### Example 2: {{PRACTICAL_EXAMPLE_2_TITLE}}

**Before:**
```
{{BEFORE_EXAMPLE_2}}
```

**After:**
```
{{AFTER_EXAMPLE_2}}
```

**Key Improvements:**
- {{IMPROVEMENT_1}}
- {{IMPROVEMENT_2}}
- {{IMPROVEMENT_3}}
</context>

<context name="{{CONCEPT_NAME}}_decision_logic" priority="medium">
## Decision Logic for Implementation

### Step 1: {{DECISION_STEP_1_TITLE}}
```
START
│
├─ IF {{CONDITION_1}}
│  └─ {{ACTION_1}}
│
├─ IF {{CONDITION_2}}
│  └─ {{ACTION_2}}
│
└─ OTHERWISE
   └─ {{DEFAULT_ACTION}}
```

### Step 2: {{DECISION_STEP_2_TITLE}}
```
FOR EACH {{ELEMENT}}:
│
├─ IF {{ELEMENT_CONDITION_1}}
│  └─ {{ELEMENT_ACTION_1}}
│
├─ IF {{ELEMENT_CONDITION_2}}
│  └─ {{ELEMENT_ACTION_2}}
│
└─ OTHERWISE
   └─ {{ELEMENT_DEFAULT_ACTION}}
```

### Step 3: {{DECISION_STEP_3_TITLE}}
```
VALIDATION CHECKLIST:
│
├─ {{VALIDATION_ITEM_1}}
│
├─ {{VALIDATION_ITEM_2}}
│
├─ {{VALIDATION_ITEM_3}}
│
└─ {{VALIDATION_ITEM_4}}
```

### Key Questions to Consider

- {{QUESTION_1}}
- {{QUESTION_2}}
- {{QUESTION_3}}
- {{QUESTION_4}}
- {{QUESTION_5}}
</context>

<context name="{{CONCEPT_NAME}}_code_implementation" priority="medium">
## Code Implementation

### {{FRAMEWORK_1}} Implementation

```{{LANGUAGE}}
{{CODE_EXAMPLE_1}}
```

**Key Implementation Notes:**
- {{CODE_NOTE_1}}
- {{CODE_NOTE_2}}
- {{CODE_NOTE_3}}

### {{FRAMEWORK_2}} Implementation

```{{LANGUAGE}}
{{CODE_EXAMPLE_2}}
```

**Key Implementation Notes:**
- {{CODE_NOTE_1}}
- {{CODE_NOTE_2}}
- {{CODE_NOTE_3}}

### Reusable Component Example

```{{LANGUAGE}}
{{COMPONENT_CODE_EXAMPLE}}
```

**Usage Example:**

```{{LANGUAGE}}
{{USAGE_EXAMPLE}}
```
</context>

<context name="{{CONCEPT_NAME}}_anti_patterns" priority="medium">
## Anti-Patterns and Common Mistakes

### 1. {{ANTI_PATTERN_1_NAME}}

**Problem:**
{{ANTI_PATTERN_1_PROBLEM}}

**Example:**
```
{{ANTI_PATTERN_1_EXAMPLE}}
```

**Why It Fails:**
- {{REASON_1}}
- {{REASON_2}}
- {{REASON_3}}

**Better Approach:**
```
{{ANTI_PATTERN_1_SOLUTION}}
```

### 2. {{ANTI_PATTERN_2_NAME}}

**Problem:**
{{ANTI_PATTERN_2_PROBLEM}}

**Example:**
```
{{ANTI_PATTERN_2_EXAMPLE}}
```

**Why It Fails:**
- {{REASON_1}}
- {{REASON_2}}
- {{REASON_3}}

**Better Approach:**
```
{{ANTI_PATTERN_2_SOLUTION}}
```

### 3. {{ANTI_PATTERN_3_NAME}}

**Problem:**
{{ANTI_PATTERN_3_PROBLEM}}

**Example:**
```
{{ANTI_PATTERN_3_EXAMPLE}}
```

**Why It Fails:**
- {{REASON_1}}
- {{REASON_2}}
- {{REASON_3}}

**Better Approach:**
```
{{ANTI_PATTERN_3_SOLUTION}}
```
</context>

<context name="{{CONCEPT_NAME}}_reasoning_principles" priority="low">
## Reasoning Principles

Understanding why {{CONCEPT_NAME}} works helps create more effective implementations:

### 1. {{REASONING_PRINCIPLE_1}}
{{REASONING_PRINCIPLE_1_EXPLANATION}}

### 2. {{REASONING_PRINCIPLE_2}}
{{REASONING_PRINCIPLE_2_EXPLANATION}}

### 3. {{REASONING_PRINCIPLE_3}}
{{REASONING_PRINCIPLE_3_EXPLANATION}}

### 4. {{REASONING_PRINCIPLE_4}}
{{REASONING_PRINCIPLE_4_EXPLANATION}}

### 5. {{REASONING_PRINCIPLE_5}}
{{REASONING_PRINCIPLE_5_EXPLANATION}}
</context>

<context name="{{CONCEPT_NAME}}_model_specific_notes" priority="low">
## Model-Specific Implementation Notes

### For Claude (Anthropic)
- {{CLAUDE_NOTE_1}}
- {{CLAUDE_NOTE_2}}
- {{CLAUDE_NOTE_3}}

### For GPT (OpenAI)
- {{GPT_NOTE_1}}
- {{GPT_NOTE_2}}
- {{GPT_NOTE_3}}

### For Cursor AI
- {{CURSOR_NOTE_1}}
- {{CURSOR_NOTE_2}}
- {{CURSOR_NOTE_3}}

### For Local Models
- {{LOCAL_MODEL_NOTE_1}}
- {{LOCAL_MODEL_NOTE_2}}
- {{LOCAL_MODEL_NOTE_3}}
</context>

<context name="{{CONCEPT_NAME}}_related_concepts" priority="low">
## Related Concepts

- **{{RELATED_CONCEPT_1}}** - {{RELATED_CONCEPT_1_DESCRIPTION}}
- **{{RELATED_CONCEPT_2}}** - {{RELATED_CONCEPT_2_DESCRIPTION}}
- **{{RELATED_CONCEPT_3}}** - {{RELATED_CONCEPT_3_DESCRIPTION}}
- **{{RELATED_CONCEPT_4}}** - {{RELATED_CONCEPT_4_DESCRIPTION}}
- **{{RELATED_CONCEPT_5}}** - {{RELATED_CONCEPT_5_DESCRIPTION}}
</context>

## Using This Module

This module can be referenced when:
- {{USE_CASE_1}}
- {{USE_CASE_2}}
- {{USE_CASE_3}}
- {{USE_CASE_4}}
- {{USE_CASE_5}}

Apply these principles systematically to {{APPLICATION_SUMMARY}}.

Last Updated: {{LAST_UPDATED_DATE}}
