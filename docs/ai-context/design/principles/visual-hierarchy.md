# Visual Hierarchy

This context module provides understanding of visual hierarchy principles for information organization and user attention guidance.

## Conceptual Foundation

Visual hierarchy is the arrangement of elements to show their order of importance. Effective hierarchy guides users through content in the intended sequence, creating clear paths for information consumption and action.

## Core Principles

### 1. Size Relationships
- Larger elements are perceived as more important
- Size contrast should reflect importance differential
- Relative sizing (rather than absolute) creates relationships

### 2. Color & Contrast
- Higher contrast elements draw more attention
- Saturated colors stand out against desaturated ones
- Strategic color usage highlights key interactive elements
- Brand colors often indicate primary actions

### 3. Typography Hierarchy
- Font weight differentiates heading levels (700 for primary, 600 for secondary)
- Size progression follows consistent ratio (typically 1.2-1.5× scale)
- Style variations (regular, italic, bold) create distinct content types
- Line height decreases as font size increases

### 4. Spatial Relationships
- Proximity groups related elements
- White space isolates and emphasizes important content
- Alignment creates connection between elements
- Grid-based layouts establish systematic hierarchy

### 5. Content Density
- Lower density content receives more attention
- Strategic density variations guide focus
- Consistent density within logical groups

## Implementation Patterns

### Web/Application Interface
```
1. Primary Heading (H1)
   • Secondary Heading (H2)
      - Content group
        · Detail content
        · Supporting text
   • Related action
2. Next Primary Section
```

### Typical Hierarchy Sequence
1. **Primary CTA/Critical Information** - Largest, highest contrast
2. **Key Supporting Information** - Second in prominence
3. **Navigation Elements** - Clearly visible but less dominant
4. **Secondary Actions** - Present but visually subordinate
5. **Tertiary Content** - Smallest, lowest contrast

### Visual Hierarchy Algorithms
- **Size**: Most important = largest (typically 2-3× larger than body text)
- **Weight**: Most important = heaviest (700 vs 400 for body)
- **Color**: Most important = highest contrast with background
- **Position**: Most important = top/left (in Western reading patterns)
- **Isolation**: Most important = most white space surrounding it

## Decision Logic for Implementation

When establishing visual hierarchy:

1. **Identify Content Relationships**
   - What information belongs together?
   - What is the logical reading sequence?
   - Which elements are interdependent?

2. **Determine Importance Levels**
   - What is the primary user goal?
   - Which information is critical vs supplementary?
   - What actions should be prioritized?

3. **Apply Consistent System**
   - Choose hierarchy mechanisms (size, weight, color, space)
   - Ensure sufficient contrast between levels
   - Maintain consistent patterns across the interface

4. **Validate with Sequence Check**
   - Trace the actual visual flow through squinting test
   - Verify first attention point matches intended primary element
   - Ensure secondary elements receive appropriate attention

## Code Translation

### CSS Implementation System
```css
:root {
  /* Typography scale */
  --text-xs: 0.75rem;    /* 12px - supporting text */
  --text-sm: 0.875rem;   /* 14px - interface text */
  --text-base: 1rem;     /* 16px - body copy */
  --text-lg: 1.125rem;   /* 18px - emphasized content */
  --text-xl: 1.25rem;    /* 20px - subheadings */
  --text-2xl: 1.5rem;    /* 24px - section headings */
  --text-3xl: 1.875rem;  /* 30px - page headings */
  --text-4xl: 2.25rem;   /* 36px - major headlines */
  
  /* Font weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
}

/* Heading hierarchy */
h1 {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  margin-bottom: 1.5rem;
}

h2 {
  font-size: var(--text-2xl);
  font-weight: var(--font-semibold);
  margin-bottom: 1rem;
}

/* Button hierarchy */
.btn-primary {
  font-size: var(--text-base);
  font-weight: var(--font-medium);
  padding: 0.75rem 1.25rem;
  background-color: var(--color-primary);
}

.btn-secondary {
  font-size: var(--text-sm);
  font-weight: var(--font-normal);
  padding: 0.5rem 1rem;
  background-color: var(--color-secondary);
}
```

### Component Pattern Example
```jsx
const ContentSection = () => (
  <section className="content-section">
    <h2 className="section-title">Feature Overview</h2>
    <p className="section-intro">Our platform provides powerful analytics with an intuitive interface.</p>
    
    <div className="feature-list">
      <FeatureCard 
        title="Real-time Data"
        isPrimary={true}
      />
      <FeatureCard 
        title="Custom Reports"
        isPrimary={false}
      />
    </div>
    
    <button className="btn-primary">Get Started</button>
    <button className="btn-secondary">Learn More</button>
  </section>
);
```

## Anti-Patterns

### Competing Focal Points
- Multiple elements with equal visual weight create confusion
- Too many bold or colorful elements dilute hierarchy
- Similar-sized text blocks without clear differentiation

### Insufficient Contrast
- Too subtle differences between hierarchy levels
- Weak differentiation between interactive and static elements
- Inadequate spacing between hierarchy groups

### Inconsistent Application
- Different hierarchy signals on similar content types
- Arbitrary size or weight changes without meaning
- Unpredictable positioning of similar elements

### Hierarchy Inflation
- Overuse of emphasis (when everything is bold, nothing is)
- Too many levels of hierarchy (5+ distinct levels)
- Excessive variations creating visual noise

## Reasoning Principles

Effective visual hierarchy works because it:

1. **Matches cognitive processing** - Aligns with how humans naturally scan information
2. **Reduces cognitive load** - Pre-organizes content so users don't have to
3. **Creates information scent** - Helps users predict what content is important
4. **Establishes design grammar** - Sets expectations for how information types appear
5. **Supports scanning behavior** - Facilitates non-linear information consumption

## Related Concepts

- **Information Architecture** - Overall structure of information
- **Gestalt Principles** - Perceptual organization of visual elements
- **Typography Systems** - Text organization and styling
- **Color Theory** - Strategic use of color for emphasis and meaning
