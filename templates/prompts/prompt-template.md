# Standard Prompt Template

This document defines the standard format for all prompts in the system, designed to be compatible with MCP, DSPy, and other AI frameworks while maintaining human readability.

## Template Format

```markdown
# [Prompt Title]

## Metadata
- **Priority:** [high/medium/low]
- **Models:** [compatible models: claude, gpt-4, etc.]
- **Category:** [category1, category2]
- **Version:** [version number]

## Purpose
[1-2 sentence description of what this prompt helps accomplish]

## Template
```
[Actual prompt template with placeholders using {{VARIABLE}} notation]
```

## Variables
- **{{VARIABLE_1}}**: [Description of what should go here]
- **{{VARIABLE_2}}**: [Description of what should go here]
- **{{VARIABLE_3}}**: [Description of what should go here]

## Example Usage
[Complete example with variables filled in]

## Tips
- [Optional section with 2-3 tips for getting the most out of this prompt]
- [Another specific tip]
- [Another specific tip]

## Expected Output
[Description of what the output should look like, optionally with an example]

## Tags
#tag1 #tag2 #tag3
```

## MCP Compatibility

The format automatically converts to MCP format as follows:

```
<context name="prompt_title" priority="high">
# [Prompt Title]
</context>

<context name="prompt_purpose" priority="high">
[Purpose description]
</context>

<context name="prompt_template" priority="high">
[Template content]
</context>

<context name="prompt_variables" priority="medium">
[Variables section]
</context>

<context name="prompt_examples" priority="medium">
[Example usage section]
</context>

<context name="prompt_tips" priority="low">
[Tips section]
</context>
```

## DSPy Compatibility

The format can be easily parsed for DSPy implementation:

```python
import dspy

class PromptTitle(dspy.Signature):
    """[Purpose description]"""
    variable_1 = dspy.InputField(desc="Description of variable 1")
    variable_2 = dspy.InputField(desc="Description of variable 2")
    output = dspy.OutputField(desc="Expected output description")

# Convert the template to a DSPy prompt template
template = """
[Template content with {variable_1} and {variable_2} placeholders]
"""

prompt_module = dspy.ChainOfThought(PromptTitle)
```

## Example Implementation

```markdown
# Code Review

## Metadata
- **Priority:** high
- **Models:** claude-3, gpt-4
- **Category:** development, quality, review
- **Version:** 1.0

## Purpose
Provides a comprehensive code review with analysis of bugs, performance, security, style, and improvement opportunities.

## Template
```
# Code Review Request

## File to Review
{{FILENAME}}

## Code Content
```
{{CODE}}
```

## Project Context
{{CONTEXT}}

## Review Criteria

Please review this code for:

1. **Bugs and Potential Issues**
   - Logic errors
   - Edge cases
   - Error handling
   - Async/await usage

2. **Performance Concerns**
   - Algorithmic complexity
   - Memory usage
   - Rendering performance (if UI code)
   - Database query efficiency (if applicable)

3. **Security Vulnerabilities**
   - Injection risks
   - Authentication/authorization issues
   - Data exposure
   - Dependency risks

4. **Style and Best Practices**
   - Adherence to conventions
   - Readability and maintainability
   - Documentation quality
   - Testing considerations

5. **Potential Improvements**
   - Refactoring opportunities
   - Architecture suggestions
   - Better patterns or approaches
   - Modern language features

Please provide specific recommendations with code examples where applicable. Categorize issues by severity (Critical, Major, Minor, Suggestion).
```

## Variables
- **{{FILENAME}}**: Complete path and name of the file to be reviewed
- **{{CODE}}**: The full code content to be reviewed
- **{{CONTEXT}}**: Relevant project information (language, framework, dependencies, purpose)

## Example Usage
```
# Code Review Request

## File to Review
src/components/UserAuthentication.js

## Code Content
```javascript
import React, { useState } from 'react';
import axios from 'axios';

function UserAuthentication() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
    try {
      const response = await axios.post('/api/login', { username, password });
      localStorage.setItem('token', response.data.token);
      window.location.href = '/dashboard';
    } catch (err) {
      setError('Login failed');
    }
  };

  return (
    <div>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      {error && <p>{error}</p>}
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}

export default UserAuthentication;
```

## Project Context
This is a React component for a financial dashboard application. We use React 18, axios for API calls, and JWT for authentication. The application needs to meet financial industry security standards and handle high traffic.
```

## Tips
- Provide specific commit or branch information in the context
- For large files, highlight specific sections you're most concerned about
- Include any performance or security requirements specific to your project

## Expected Output
A structured review with sections for each review criteria, with issues clearly categorized by severity. Each issue should include:
- Description of the problem
- Why it's an issue
- Code example of how to fix it
- Severity level

## Tags
#code #review #quality #development #security
```

## Implementation Notes

1. **Storage Format**: Store prompts in individual markdown files for easy editing and version control

2. **Shortcuts System**: Implement commands like `/code-review` that expand to full templates

3. **Variable Substitution**: When a template is loaded, prompt the user for each variable or attempt to derive from context

4. **Conversion Utilities**:
   - Create functions to convert to/from MCP format
   - Create functions to generate DSPy code from templates
   - Implement template parsing and variable extraction

5. **Categorization System**: Use metadata and tags for building a searchable prompt library

6. **Version Control**: Track changes to prompts over time using the version field

This standardized format ensures consistency across your prompt library while maintaining compatibility with advanced AI frameworks and providing a user-friendly experience.
