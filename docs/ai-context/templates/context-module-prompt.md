# Context Module Creation Prompt

Use this prompt to guide Claude in creating a comprehensive MCP-compatible context module for any technical topic.

## Prompt Template

```
I need to create a comprehensive context module about [TOPIC] following the Model Context Protocol (MCP) format. The module will be used to provide structured knowledge to AI assistants like yourself.

Please research [TOPIC] thoroughly and create a complete context module following these requirements:

1. Follow the MCP format with proper <context> tags and priority attributes (high/medium/low)
2. Include all standard sections:
   - Metadata (priority, domain, target models, related modules)
   - Module overview
   - Conceptual foundation (high priority)
   - Core principles (high priority)
   - Implementation patterns (medium priority)
   - Decision logic (medium priority)
   - Code implementation (medium priority)
   - Anti-patterns (medium priority)
   - Reasoning principles (low priority)
   - Model-specific notes (low priority)
   - Related concepts (low priority)
   - Practical examples with before/after scenarios (medium priority)
   - "Using This Module" section with use cases

3. For the anti-patterns section:
   - Assign proper IDs (AP-[DOMAIN]-[NUM])
   - Include severity levels and AI-specific flags
   - Provide concrete examples of both problematic and correct implementations

4. Make all code examples complete, technically precise, and following best practices

5. Focus on making the module practical for real-world implementation

Here's some additional context about [TOPIC] that might be helpful:
[ADD ANY SPECIFIC DETAILS, URLS, OR RESOURCES ABOUT THE TOPIC]

Please create a comprehensive MCP-compatible context module about [TOPIC] that would be valuable for AI-assisted development.
```

## Example Usage

Here's an example of using this prompt to create a context module about GraphQL:

```
I need to create a comprehensive context module about GraphQL following the Model Context Protocol (MCP) format. The module will be used to provide structured knowledge to AI assistants like yourself.

Please research GraphQL thoroughly and create a complete context module following these requirements:

1. Follow the MCP format with proper <context> tags and priority attributes (high/medium/low)
2. Include all standard sections:
   - Metadata (priority, domain, target models, related modules)
   - Module overview
   - Conceptual foundation (high priority)
   - Core principles (high priority)
   - Implementation patterns (medium priority)
   - Decision logic (medium priority)
   - Code implementation (medium priority)
   - Anti-patterns (medium priority)
   - Reasoning principles (low priority)
   - Model-specific notes (low priority)
   - Related concepts (low priority)
   - Practical examples with before/after scenarios (medium priority)
   - "Using This Module" section with use cases

3. For the anti-patterns section:
   - Assign proper IDs (AP-[DOMAIN]-[NUM])
   - Include severity levels and AI-specific flags
   - Provide concrete examples of both problematic and correct implementations

4. Make all code examples complete, technically precise, and following best practices

5. Focus on making the module practical for real-world implementation

Here's some additional context about GraphQL that might be helpful:
- Official documentation: https://graphql.org/
- Apollo GraphQL implementation: https://www.apollographql.com/
- Common use cases include API development for web and mobile applications
- Key considerations should include schema design, resolver implementation, and performance optimization
```

## Tips for Effective Module Creation

1. **Research First**: Provide links to official documentation and high-quality resources when possible
   
2. **Be Specific**: Instead of just asking for a general module, specify any particular aspects you want emphasized
   
3. **Provide Examples**: If you have examples of good implementations or anti-patterns, include them in your prompt
   
4. **Specify Technical Level**: Indicate whether the module should be beginner-friendly or assume advanced knowledge
   
5. **Request Practical Focus**: Emphasize that the module should contain actionable, practical guidance rather than just theory
   
6. **Specify Language/Framework**: If the topic relates to programming, specify which languages or frameworks to focus on
   
7. **Indicate Size**: Suggest how comprehensive the module should be (e.g., "create a detailed module with 5-6 core principles")
   
8. **Request Verification**: Ask for internal consistency checks and technical accuracy verification

## Follow-up Prompts for Refinement

After receiving an initial module draft, you can use these follow-up prompts to refine it:

1. **Expand a section**:
   ```
   Please expand the [SECTION_NAME] section to include more detailed information about [SPECIFIC_ASPECT].
   ```

2. **Add more examples**:
   ```
   The module needs more practical examples. Please add 2-3 additional before/after examples focusing on [SPECIFIC_SCENARIOS].
   ```

3. **Improve code examples**:
   ```
   The code examples in the [SECTION_NAME] section could be improved. Please enhance them with better comments, error handling, and following the [SPECIFIC] best practices.
   ```

4. **Add missing anti-patterns**:
   ```
   Please add these additional anti-patterns to the module: [LIST_ANTI_PATTERNS]. Follow the same format as the existing ones.
   ```

5. **Request technical verification**:
   ```
   Please review the technical accuracy of the module, particularly the code examples and implementation patterns. Fix any issues you find.
   ```
