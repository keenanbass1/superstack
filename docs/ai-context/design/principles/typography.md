# Typography

This context module explains typography principles in UI design, providing guidelines for creating readable, hierarchical, and aesthetically pleasing text systems.

## Conceptual Foundation

Typography is the art and technique of arranging type to make written language legible, readable, and appealing. In digital interfaces, effective typography establishes hierarchy, improves readability, creates visual harmony, and reinforces brand identity. A systematic approach to typography creates consistency while supporting various content needs.

## Core Principles

### 1. Hierarchical Structure
- Clear differentiation between heading levels
- Consistent size and weight progression
- Limited number of text styles (typically 5-7)
- Visual weight matches content importance

### 2. Readability Optimization
- Appropriate line length (45-75 characters per line)
- Sufficient line height (1.4-1.6 for body text)
- Adequate contrast (4.5:1 minimum for WCAG AA)
- Suitable font size (minimum 16px for body text)

### 3. Font Selection
- Limited font families (typically 1-3)
- Purposeful pairing (e.g., serif headings with sans-serif body)
- Font suitability for context and purpose
- Fallback stacks for reliable rendering

### 4. Consistent Scale
- Mathematical progression of sizes
- Common ratios: 1.2 (minor third), 1.25 (major third), 1.5 (perfect fifth)
- Size adaptation for different viewport widths
- Relationships maintained across screen sizes

### 5. Stylistic Restraint
- Focused use of emphasis (bold, italic, etc.)
- Purposeful alignment (typically left-aligned for LTR languages)
- Careful use of decorative elements
- Color as an enhancement, not a requirement for understanding

## Implementation Patterns

### Type Scale System

#### Standard Type Scale (1.25 Ratio)
- **Caption text**: 12px / 0.75rem
- **Body small**: 14px / 0.875rem
- **Body default**: 16px / 1rem (base)
- **Body large**: 18px / 1.125rem
- **Heading 4**: 20px / 1.25rem
- **Heading 3**: 25px / 1.563rem
- **Heading 2**: 31.25px / 1.953rem
- **Heading 1**: 39.06px / 2.441rem
- **Display**: 48.83px / 3.052rem

#### Font Weight Distribution
- **Regular (400)**: Body text, captions, less emphasis
- **Medium (500)**: Subtle emphasis, subheadings
- **Semibold (600)**: Secondary headings, important text
- **Bold (700)**: Primary headings, strong emphasis

### Common Typography Patterns

#### Content Typography
- Body text: 16-18px, 1.5 line height, 700-800 characters per paragraph max
- Headings: Clear size hierarchy, tighter line height than body (1.2-1.3)
- Links: Distinguishable through color and/or underline
- Lists: Proper indentation, consistent bullet/numbering style

#### Interface Typography
- Labels: 14-16px, often medium (500) weight
- Buttons: 14-16px, typically medium (500) or semibold (600)
- Navigation: 14-16px, weight often used to indicate current state
- System messages: 14-16px, with appropriate colorization

#### Form Typography
- Input text: 16px minimum (prevents mobile zoom)
- Field labels: Clear relationship to fields, typically 14-16px
- Help text: Typically 14px, lighter color than primary text
- Validation messages: Clear association with fields, actionable text

## Decision Logic for Implementation

When designing typography:

1. **Identify Content Types and Hierarchy**
   - What levels of hierarchy are needed?
   - What types of content must be accommodated?
   - What reading contexts will users encounter?

2. **Choose Base Size and Scale**
   - Select body text size (typically 16px)
   - Choose appropriate scale ratio based on hierarchy needs
   - Verify readability across target devices

3. **Assign Weights and Styles**
   - Map weights to hierarchy (typically heavier = more important)
   - Decide style variations for different content types
   - Ensure sufficient contrast between styles

4. **Test and Refine for Readability**
   - Verify line length is appropriate (45-75 characters)
   - Check line height supports comfortable reading
   - Ensure proper spacing between paragraphs and sections

## Code Translation

### CSS Variables System
```css
:root {
  /* Font families */
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-secondary: 'Georgia', serif;
  
  /* Font sizes */
  --text-xs: 0.75rem;      /* 12px */
  --text-sm: 0.875rem;     /* 14px */
  --text-base: 1rem;       /* 16px */
  --text-lg: 1.125rem;     /* 18px */
  --text-xl: 1.25rem;      /* 20px */
  --text-2xl: 1.5625rem;   /* 25px */
  --text-3xl: 1.953rem;    /* 31.25px */
  --text-4xl: 2.441rem;    /* 39.06px */
  --text-5xl: 3.052rem;    /* 48.83px */
  
  /* Font weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
  
  /* Line heights */
  --leading-tight: 1.2;
  --leading-snug: 1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
}

/* Base typography */
body {
  font-family: var(--font-primary);
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  color: #333333;
}

/* Heading styles */
h1 {
  font-size: var(--text-4xl);
  font-weight: var(--font-bold);
  line-height: var(--leading-tight);
  margin-bottom: 1.5rem;
}

h2 {
  font-size: var(--text-3xl);
  font-weight: var(--font-semibold);
  line-height: var(--leading-tight);
  margin-bottom: 1.25rem;
}

h3 {
  font-size: var(--text-2xl);
  font-weight: var(--font-semibold);
  line-height: var(--leading-snug);
  margin-bottom: 1rem;
}
```

### Typography System in Tailwind
```js
// tailwind.config.js
module.exports = {
  theme: {
    fontFamily: {
      sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      serif: ['Georgia', 'serif'],
    },
    fontSize: {
      'xs': ['0.75rem', { lineHeight: '1rem' }],
      'sm': ['0.875rem', { lineHeight: '1.25rem' }],
      'base': ['1rem', { lineHeight: '1.5rem' }],
      'lg': ['1.125rem', { lineHeight: '1.75rem' }],
      'xl': ['1.25rem', { lineHeight: '1.75rem' }],
      '2xl': ['1.5625rem', { lineHeight: '2rem' }],
      '3xl': ['1.953rem', { lineHeight: '2.25rem' }],
      '4xl': ['2.441rem', { lineHeight: '2.5rem' }],
      '5xl': ['3.052rem', { lineHeight: '1' }],
    },
    fontWeight: {
      normal: '400',
      medium: '500',
      semibold: '600',
      bold: '700',
    },
  },
}
```

### React Component Example
```jsx
function ArticleContent() {
  return (
    <article className="max-w-prose mx-auto">
      <h1 className="text-4xl font-bold leading-tight mb-6">
        Understanding Typography Systems
      </h1>
      
      <p className="text-lg mb-4 text-gray-700">
        A well-designed typography system creates harmony and clarity in your interface. 
        This article explores the key principles of effective typographic hierarchy.
      </p>
      
      <h2 className="text-3xl font-semibold leading-tight mt-8 mb-4">
        The Importance of Scale
      </h2>
      
      <p className="text-base mb-4">
        Typography scales provide consistent progression between sizes, creating predictable 
        relationships between different text elements. Most designers rely on mathematical 
        ratios to establish these relationships.
      </p>
      
      <h3 className="text-2xl font-semibold leading-snug mt-6 mb-3">
        Common Scale Ratios
      </h3>
      
      <ul className="list-disc pl-6 mb-4">
        <li className="mb-2">Minor third (1.2) - Subtle progression</li>
        <li className="mb-2">Major third (1.25) - Balanced progression</li>
        <li className="mb-2">Perfect fourth (1.333) - Moderate contrast</li>
        <li className="mb-2">Perfect fifth (1.5) - Significant contrast</li>
      </ul>
    </article>
  );
}
```

## Anti-Patterns

### Excessive Variety
- Too many font families (>3) creating visual noise
- Inconsistent or random size progression
- Too many weight variations without clear purpose
- Mixing incompatible font styles

### Poor Readability
- Text too small (<16px) for body content
- Line length too long (>80 characters) or too short (<45 characters)
- Insufficient line height causing text to feel cramped
- Low contrast between text and background

### Inconsistent Hierarchy
- Headings too similar in size to distinguish levels
- Body text competing with headings in visual weight
- Inconsistent styling for the same content type
- Random size/weight combinations

### Responsive Failures
- Text too large or small on mobile devices
- Fixed font sizes that don't adapt to viewport
- Line lengths not optimized for device width
- Insufficient spacing on smaller screens

### Accessibility Issues
- Relying solely on color to distinguish text types
- Text that doesn't resize when browser settings change
- Insufficient contrast ratios for text
- Fixed height containers that clip text when enlarged

## Reasoning Principles

Effective typography works because it:

1. **Reduces Cognitive Load** - Clear hierarchy guides users through content
2. **Enhances Comprehension** - Proper spacing and sizing improves readability
3. **Creates Rhythm** - Consistent type scales create visual harmony
4. **Establishes Identity** - Typography conveys personality and brand attributes
5. **Guides Attention** - Size and weight direct users to important information
6. **Improves Accessibility** - Well-designed type supports diverse reading needs

## Related Concepts

- **Visual Hierarchy** - How typography contributes to overall information ordering
- **Spacing Systems** - How whitespace interacts with typography
- **Color Theory** - How color enhances typographic hierarchy
- **Responsive Design** - How typography adapts across devices
- **Accessibility** - How typography supports inclusive reading experiences
