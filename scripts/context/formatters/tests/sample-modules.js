/**
 * Sample context modules for testing formatters
 */

module.exports = [
  {
    id: 'react-component-structure',
    name: 'React Component Structure',
    description: 'Best practices for structuring React components',
    domain: 'frontend',
    type: 'pattern',
    content: `When creating React components:
1. Use functional components with hooks
2. Keep components small and focused
3. Extract reusable logic to custom hooks
4. Use proper prop typing with PropTypes or TypeScript
5. Follow the presentational/container component pattern when appropriate`,
    active: true,
    tags: ['react', 'components', 'frontend']
  },
  {
    id: 'database-query-optimization',
    name: 'Database Query Optimization',
    description: 'Guidelines for optimizing database queries',
    domain: 'backend',
    type: 'pattern',
    content: `When writing database queries:
1. Use indexes for frequently queried columns
2. Avoid SELECT * and only query needed columns
3. Use JOINs efficiently and limit nested queries
4. Consider pagination for large result sets
5. Use query caching when appropriate`,
    active: true,
    tags: ['database', 'performance', 'backend']
  },
  {
    id: 'api-error-handling',
    name: 'API Error Handling',
    description: 'Standard approach for API error responses',
    domain: 'backend',
    type: 'standard',
    content: `API error responses should:
1. Use appropriate HTTP status codes
2. Include a consistent error object structure
3. Provide meaningful error messages
4. Include a unique error code when applicable
5. Log detailed errors server-side but return safe messages to clients`,
    active: true,
    tags: ['api', 'error-handling', 'backend']
  },
  {
    id: 'css-naming-convention',
    name: 'CSS Naming Convention',
    description: 'BEM methodology for CSS class naming',
    domain: 'frontend',
    type: 'standard',
    content: `Follow BEM (Block Element Modifier) naming convention:
1. Block: Standalone component (e.g., .button)
2. Element: Part of a block (e.g., .button__icon)
3. Modifier: Variation of a block or element (e.g., .button--large)
4. Use hyphens for word separation
5. Keep names descriptive but concise`,
    active: false,
    tags: ['css', 'naming', 'frontend']
  },
  {
    id: 'security-input-validation',
    name: 'Security Input Validation',
    description: 'Best practices for validating user input',
    domain: 'security',
    type: 'pattern',
    content: `When handling user input:
1. Validate on both client and server side
2. Use whitelisting rather than blacklisting
3. Sanitize input to prevent XSS attacks
4. Use parameterized queries to prevent SQL injection
5. Validate content type and size for file uploads`,
    active: true,
    tags: ['security', 'validation', 'input']
  }
];