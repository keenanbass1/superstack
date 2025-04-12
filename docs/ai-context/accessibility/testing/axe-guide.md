# Axe Testing Guide

Axe is a powerful accessibility testing tool developed by Deque Systems. This guide covers how to effectively use axe for automated accessibility testing.

## Axe Capabilities

Axe can detect approximately 57% of accessibility issues automatically. The remaining issues require manual testing and review.

### What Axe Can Detect

- Missing alternative text
- Insufficient color contrast
- Missing form labels
- Empty links and buttons
- Missing document language
- Invalid ARIA attributes
- Keyboard accessibility issues
- And many more...

### What Axe Cannot Detect

- Appropriateness of alternative text
- Logical reading order
- Meaningful sequence
- Accurate headings hierarchy for content
- Appropriate page titles
- Logical keyboard focus order

## Integrating Axe

### Browser Extensions

Install the axe DevTools extension for:
- Chrome
- Firefox
- Edge

### Development Integration

#### Axe Core (JavaScript)

```javascript
// Install via npm
npm install axe-core

// Basic usage
import * as axe from 'axe-core';

axe.run().then(results => {
  console.log(results.violations);
});
```

#### React Integration

```javascript
// Install
npm install @axe-core/react

// Setup in index.js (development only)
if (process.env.NODE_ENV !== 'production') {
  import('@axe-core/react').then(axe => {
    axe.default(React, ReactDOM, 1000);
  });
}
```

#### Testing Frameworks

```javascript
// Jest + Testing Library example
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

test('component has no accessibility violations', async () => {
  const { container } = render(<MyComponent />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

## Interpreting Results

Axe results are categorized by:

1. **Violations**: Definite accessibility issues
2. **Incomplete**: Potential issues requiring manual verification
3. **Passes**: Checks that passed
4. **Inapplicable**: Checks that don't apply to the tested content

### Sample Violation Object

```javascript
{
  id: 'color-contrast',
  impact: 'serious',
  tags: ['WCAG2AA', 'WCAG143'],
  description: 'Ensures the contrast between foreground and background colors meets WCAG 2 AA contrast ratio thresholds',
  help: 'Elements must have sufficient color contrast',
  helpUrl: 'https://dequeuniversity.com/rules/axe/4.3/color-contrast',
  nodes: [
    {
      html: '<p class="light-text">Low contrast text</p>',
      impact: 'serious',
      target: ['.light-text'],
      failureSummary: 'Fix any of the following: Element has insufficient color contrast of 2.5:1 (foreground color: #aaa, background color: #fff, font size: 12.0pt, font weight: normal)'
    }
  ]
}
```

## Best Practices

1. **Integrate early**: Run axe tests during development, not just before release
2. **Automate testing**: Include axe in CI/CD pipelines
3. **Prioritize fixes**: Address high-impact issues first
4. **Combine with manual testing**: Use axe as a starting point, not the end of testing
5. **Document known issues**: Track issues that can't be immediately fixed
6. **Progressive improvement**: Fix issues systematically over time