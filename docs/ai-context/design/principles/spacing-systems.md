# Spacing Systems

This context module explains spacing systems in UI design, providing principles and implementation patterns for consistent spatial relationships.

## Conceptual Foundation

A spacing system creates visual rhythm and hierarchy through consistent distances between elements. It's built on a base unit (typically 4px or 8px) with values following a predictable progression. Systematic spacing improves readability, establishes hierarchy, and creates visual harmony.

## Core Principles

### 1. Base Unit Foundation
- Use a consistent base unit (8px is standard)
- All spacing values should be multiples of this base
- Common scales: 8, 16, 24, 32, 48, 64, 96

### 2. Meaningful Progression
- Follow a logical mathematical progression
- Common progressions: linear (8, 16, 24...) or geometric (8, 16, 32, 64...)
- Each step should create a noticeable, purposeful difference

### 3. Relational Spacing
- Related elements have smaller spacing between them
- Unrelated elements have larger spacing between them
- Spacing communicates relationships just as much as lines and borders

### 4. Consistent Application
- Similar components should use identical spacing values
- Maintain consistent spacing ratios across device sizes
- Use the same spacing system across the entire interface

### 5. Contextual Adaptation
- Increase spacing for larger viewports
- Tighten spacing on mobile (but maintain relationships)
- Consider information density requirements by context

## Implementation Patterns

### Component Internal Spacing

#### Cards & Containers
- **Padding**: 24px (3× base) for standard cards
- **Content Group Spacing**: 16px (2× base) between groups
- **Dense Cards**: 16px padding for compact displays
- **Title-to-Content**: 8px (1× base) between heading and content

#### Form Elements
- **Label-to-Field**: 8px between label and input
- **Between Fields**: 24px (3× base) vertical spacing
- **Field Groups**: 16px (2× base) between related fields
- **Section Spacing**: 32px (4× base) between form sections

#### Interactive Elements
- **Button Padding**: 16px horizontal, 8-12px vertical
- **Icon Spacing**: 8px between icon and text
- **Action Groups**: 16px between related actions

### Layout Spacing

#### Content Sections
- **Section Margins**: 48px or 64px (6-8× base unit)
- **Content Width**: Maximum paragraph width 60-75 characters
- **Header-to-Content**: 32px (4× base) between page header and content

#### Grid Systems
- **Gutters**: 24px standard, 16px on mobile
- **Margins**: 24px standard, 16px on mobile
- **Container Padding**: 24px (laptop), 16px (tablet), 16px (mobile)

## Decision Logic for Implementation

When determining spacing:

1. **Identify Relationship Type**
   - Are these elements directly related (label + field)?
   - Are they part of the same group (menu items)?
   - Are they in separate sections (content blocks)?

2. **Consider Information Density**
   - Is this a dense, data-heavy interface?
   - Is this a content-focused, reading-optimized view?
   - What is the primary task in this context?

3. **Select Scale Values**
   - Use smaller values (8px, 16px) for related elements
   - Use medium values (24px, 32px) for component separation
   - Use larger values (48px, 64px) for major section divisions

4. **Maintain Consistency**
   - Apply the same spacing values for similar relationships
   - Use spacing to reinforce content hierarchy
   - Ensure grid alignment through consistent spacing

## Code Translation

### CSS Variables System
```css
:root {
  /* Spacing scale */
  --space-1: 8px;     /* 1× - Minor spacing */
  --space-2: 16px;    /* 2× - Standard element spacing */
  --space-3: 24px;    /* 3× - Component padding */
  --space-4: 32px;    /* 4× - Small section spacing */
  --space-6: 48px;    /* 6× - Medium section spacing */
  --space-8: 64px;    /* 8× - Large section spacing */
  --space-12: 96px;   /* 12× - Major section spacing */
}

/* Card component example */
.card {
  padding: var(--space-3);
  margin-bottom: var(--space-4);
}

.card__header {
  margin-bottom: var(--space-2);
}

.card__content {
  margin-bottom: var(--space-2);
}

.card__footer {
  padding-top: var(--space-2);
}
```

### Tailwind Config Example
```js
// tailwind.config.js
module.exports = {
  theme: {
    spacing: {
      '0': '0',
      '1': '8px',
      '2': '16px',
      '3': '24px',
      '4': '32px',
      '6': '48px',
      '8': '64px',
      '12': '96px',
    }
  }
}
```

### React Component Example
```jsx
function ProfileCard({ user }) {
  return (
    <div className="p-3 mb-4"> {/* p-3 = padding: 24px, mb-4 = margin-bottom: 32px */}
      <div className="mb-2"> {/* mb-2 = margin-bottom: 16px */}
        <h3 className="text-xl mb-1">{user.name}</h3> {/* mb-1 = margin-bottom: 8px */}
        <p className="text-gray-600">{user.title}</p>
      </div>
      
      <div className="mb-2">
        <p>{user.bio}</p>
      </div>
      
      <div className="flex gap-2"> {/* gap-2 = gap: 16px */}
        <button className="px-2 py-1">Connect</button> {/* px-2 = padding-x: 16px, py-1 = padding-y: 8px */}
        <button className="px-2 py-1">Message</button>
      </div>
    </div>
  );
}
```

## Anti-Patterns

### Inconsistent Spacing
- Using arbitrary values (13px, 27px) instead of system values
- Different spacing for visually similar components
- Changing spacing values without clear reasoning

### Insufficient Spacing
- Elements so close they create visual tension
- Text running too close to container edges (< 16px)
- Related elements without enough separation from unrelated ones

### Excessive Spacing
- Too much white space creating "floating" elements
- Spacing so large it breaks perceived relationships
- Inefficient use of screen space in information-dense contexts

### Mixed Spacing Systems
- Combining 8px-based and 5px-based systems
- Inconsistent spacing ratios across components
- Using different spacing progressions in the same interface

## Reasoning Principles

Effective spacing systems work because they:

1. **Create Rhythm** - Consistent spacing creates visual patterns that feel harmonious
2. **Reduce Cognitive Load** - Predictable spacing helps users understand relationships
3. **Enhance Readability** - Proper spacing improves content consumption
4. **Establish Hierarchy** - Spacing variations signal importance and relationships
5. **Enable Scalability** - Systematic spacing adapts coherently across devices
6. **Improve Development** - Predefined values speed up implementation decisions

## Related Concepts

- **Visual Hierarchy** - How spacing influences content importance perception
- **Grid Systems** - Structured layout systems that work with spacing
- **Responsive Design** - How spacing adapts across different screen sizes
- **Component Architecture** - How spacing defines component boundaries
- **Typography Scale** - How text size relationships work with spacing
