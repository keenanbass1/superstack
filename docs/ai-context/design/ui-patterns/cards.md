# Cards

This context module explains card components in UI design, providing implementation patterns and decision logic for using this versatile UI element effectively.

## Conceptual Foundation

A card is a flexible container that groups related content and actions. It serves as a distinct, interactive surface that typically represents a single entity or concept within an information hierarchy. Cards create a modular, consistent way to present collections of similar objects while visually separating them from the surrounding interface.

## Core Principles

### 1. Containment & Boundaries
- Cards clearly delineate content boundaries
- Visual separation through elevation (shadow) or borders
- Consistent internal padding (typically 24px)
- Rounded corners (typically 4-8px radius) for approachable feel

### 2. Content Structure
- Consistent internal organization
- Clear visual hierarchy within the card
- Optional distinct zones (header, body, footer)
- Support for various content types (text, media, actions)

### 3. Interactive Behavior
- Clear affordances for interactive elements
- Consistent hover/focus states
- May be entirely clickable or contain discrete actions
- Support for dynamic states (loading, selected, disabled)

### 4. Scalability & Responsiveness
- Maintains structure across screen sizes
- Consistent width behavior (fixed or fluid)
- Appropriate stacking on smaller screens
- Content adaptability for different sizes

### 5. Collection Patterns
- Cards often appear in groups
- Consistent spacing between cards (typically 16-24px)
- Grid, list, or carousel arrangements
- Similar cards should have equal height in a row

## Implementation Patterns

### Card Anatomy

#### Basic Structure
```
┌─────────────────────────┐
│ [Optional Media]        │
│                         │
│ Title                   │
│ Subtitle                │
│                         │
│ Content                 │
│                         │
│ [Actions]               │
└─────────────────────────┘
```

#### Common Variants
1. **Basic Card**: Simple container with consistent padding
2. **Media Card**: Contains image/video with text
3. **Action Card**: Includes interactive controls
4. **Profile Card**: Person or entity information
5. **Product Card**: Item with image, title, price, and actions
6. **Stat Card**: Focused on displaying metrics or data points

### Layout Patterns

#### Card Grids
- Uniform width cards (typically 2-4 per row on desktop)
- Equal spacing between cards (16-24px gutters)
- Equal height per row (either fixed or stretching)
- Responsive reflow to fewer columns on smaller screens

#### Card Lists
- Full-width or fixed-width cards in vertical sequence
- Consistent vertical spacing (16-24px)
- May include left-aligned elements for scannability
- Often includes consistent visual elements for rhythm

#### Card Carousels
- Horizontally scrolling card sequences
- Partially visible cards indicate scrollability
- Consistent card sizing and spacing
- Navigation controls for accessibility

## Decision Logic for Implementation

When using cards, consider:

1. **Content Relationship Assessment**
   - Does this content represent distinct entities?
   - Would grouping these items benefit understanding?
   - Is there a consistent structure across items?

2. **Card vs. Table vs. List Decision**
   - **Use cards when**: Items benefit from visual separation; content is varied; layout is flexible
   - **Use tables when**: Dense data comparison is primary; consistent columns are needed
   - **Use lists when**: Simple scanning is primary; minimal content per item

3. **Card Density Selection**
   - **Compact cards**: Dense information display; space-constrained interfaces
   - **Standard cards**: Balanced content presentation; most interfaces
   - **Expanded cards**: Content-heavy items; focus on readability

4. **Interaction Model Choice**
   - **Fully clickable cards**: Each card represents single destination
   - **Cards with actions**: Multiple possible interactions per card
   - **Selection cards**: Cards can be selected as part of a flow

## Code Translation

### HTML Structure
```html
<div class="card">
  <div class="card__media">
    <img src="image.jpg" alt="Card image">
  </div>
  <div class="card__content">
    <h3 class="card__title">Card Title</h3>
    <p class="card__description">Card description text goes here, providing additional context.</p>
  </div>
  <div class="card__footer">
    <button class="btn btn--primary">Primary Action</button>
    <button class="btn btn--secondary">Secondary</button>
  </div>
</div>
```

### CSS Implementation
```css
.card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: box-shadow 0.2s ease;
}

.card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.card__media {
  height: 200px;
  overflow: hidden;
}

.card__media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card__content {
  padding: 24px;
}

.card__title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
}

.card__description {
  color: #4b5563;
  margin-bottom: 16px;
}

.card__footer {
  padding: 16px 24px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 8px;
}
```

### React Component
```jsx
function Card({ title, description, imageUrl, primaryAction, secondaryAction }) {
  return (
    <div className="bg-white rounded-lg shadow transition-shadow hover:shadow-md overflow-hidden">
      {imageUrl && (
        <div className="h-48 overflow-hidden">
          <img 
            src={imageUrl} 
            alt={title} 
            className="w-full h-full object-cover"
          />
        </div>
      )}
      
      <div className="p-6">
        <h3 className="text-lg font-semibold mb-2">{title}</h3>
        {description && (
          <p className="text-gray-600 mb-4">{description}</p>
        )}
      </div>
      
      {(primaryAction || secondaryAction) && (
        <div className="px-6 py-4 border-t border-gray-100 flex gap-2">
          {primaryAction && (
            <button 
              className="px-4 py-2 bg-blue-600 text-white rounded"
              onClick={primaryAction.onClick}
            >
              {primaryAction.label}
            </button>
          )}
          
          {secondaryAction && (
            <button 
              className="px-4 py-2 border border-gray-300 rounded"
              onClick={secondaryAction.onClick}
            >
              {secondaryAction.label}
            </button>
          )}
        </div>
      )}
    </div>
  );
}
```

## Anti-Patterns

### Inconsistent Card Structure
- Varying padding within the same card collection
- Inconsistent title placement or alignment
- Mixed content structures in the same collection

### Poor Content Hierarchy
- Lack of clear focal points within cards
- Too many competing elements of equal visual weight
- Important information buried or de-emphasized

### Ineffective Collection Layout
- Irregular card sizes creating visual imbalance
- Insufficient spacing between cards (< 16px)
- Overly dense card collections without visual breaks

### Unclear Interaction Models
- Ambiguous clickable areas
- Mixed interaction models within the same collection
- Missing hover/focus states for interactive elements

### Accessibility Issues
- Poor color contrast for text elements
- Interactive elements not keyboard accessible
- Missing focus indicators on interactive cards

## Reasoning Principles

Cards are effective because they:

1. **Create Chunking** - Breaking content into discrete units aids cognitive processing
2. **Enable Comparison** - Standardized format facilitates quick scanning and comparison
3. **Establish Boundaries** - Clear container boundaries reduce cognitive load
4. **Support Flexibility** - Modular nature accommodates various content types
5. **Encourage Scannability** - Card collections support non-linear browsing
6. **Provide Familiarity** - Card metaphor connects to physical card organizing systems

## Related Concepts

- **Grid Systems** - Structured layouts for organizing card collections
- **Visual Hierarchy** - How elements within cards are organized by importance
- **Information Architecture** - How cards fit into overall information structure
- **Container Design** - General principles of content containment and separation
- **List Design** - Alternative pattern for sequential content presentation
