# Buttons

This context module explains button components in UI design, providing a comprehensive guide to creating effective, accessible, and consistent button patterns across interfaces.

## Conceptual Foundation

Buttons are interactive elements that enable users to trigger actions or navigate to new contexts. They serve as primary interaction points in interfaces, communicating available actions and their relative importance. Effective button design balances visibility, affordance (suggesting how they should be used), and hierarchy (indicating relative importance of different actions).

Buttons represent perhaps the most fundamental interactive element in digital interfaces, directly translating user intent into system action. Their design significantly impacts usability, conversion rates, and overall user experience.

## Core Principles

### 1. Clear Affordance
- Buttons should be immediately recognizable as interactive elements
- Visual cues like depth, boundaries, or background color signal "clickability"
- Cursor changes (pointer) reinforce interactive nature
- Touch targets provide sufficient size for interaction (minimum 44×44px)
- Interactive states (hover, focus, active, disabled) communicate current status

### 2. Hierarchical Differentiation
- Different button styles communicate varying levels of importance
- Primary buttons highlight the main/recommended action
- Secondary buttons provide alternative or less important actions
- Tertiary/text buttons for supplementary or lower-emphasis actions
- Consistent application of hierarchy across the interface
- Only one primary button should appear in a given context

### 3. Purposeful Sizing & Placement
- Size should reflect importance and facilitate easy interaction
- Strategic placement based on user flow and expected actions
- Alignment with natural eye movement patterns and reading direction
- Appropriate spacing from other interactive elements (minimum 8px)
- Consistent positioning of similar actions across contexts
- Mobile considerations require larger touch targets and thumb-friendly placement

### 4. Content Clarity
- Label text clearly communicates the outcome of interaction
- Concise wording (typically 1-3 words) with action verbs
- Consistent terminology across the interface
- Optional icons to reinforce meaning, not replace text
- Sentence case (first word capitalized) or Title Case based on design system
- Ellipsis (...) indicates additional steps will be required before action completes

### 5. Comprehensive State Management
- All interactive states are visually distinct: default, hover, focus, active, disabled
- Keyboard focus states are clearly visible (not relying solely on hover effects)
- Loading states communicate ongoing processes
- Success/error states provide feedback on action results
- Transitions between states are smooth and meaningful
- States maintain sufficient contrast with backgrounds in all conditions

### 6. Accessibility Compliance
- Contrast ratio of at least 4.5:1 between text and background (WCAG AA)
- Appropriate ARIA roles and attributes when needed
- Keyboard navigability and focus management
- Support for screen readers with meaningful text
- No reliance on color alone to communicate state or meaning
- Scalable with browser text size changes

## Implementation Patterns

### Button Hierarchy System

#### Primary Buttons
- **Purpose**: Highlight the main action or most likely user path
- **Visual Treatment**: 
  - Highest visual weight with filled background using brand primary color
  - High contrast between text and background
  - Optional subtle depth effect (shadow)
- **Usage Guidance**:
  - Limit to one primary button per context/container
  - Position in the most prominent location in action groups
  - Reserve for the most important or frequently used action

#### Secondary Buttons
- **Purpose**: Present alternative actions of medium importance
- **Visual Treatment**:
  - Medium visual weight using outline style or subdued background
  - Often outlined with brand color or using brand color as text
  - Same size and shape as primary buttons for consistent clickable area
- **Usage Guidance**:
  - Can appear multiple times in the same context if needed
  - Often paired with a primary button ("Save" as primary, "Cancel" as secondary)
  - Maintains sufficient contrast while reducing visual competition

#### Tertiary/Text Buttons
- **Purpose**: Provide supplementary actions with minimum visual weight
- **Visual Treatment**:
  - Minimal styling, often appearing as colored/underlined text
  - May use brand color with no background or border
  - Hover/focus states add subtle background or underline
- **Usage Guidance**:
  - Used for lower-priority actions that should remain accessible
  - Good for space-constrained interfaces or dense action areas
  - Often used in card footers, toolbars, or as "learn more" actions

### Size Variants

#### Large Buttons
- **Dimensions**: Height 48-56px, padding 16-24px horizontal
- **Typography**: Larger text (16-18px)
- **Usage**: Primary call-to-action, landing pages, confirmation dialogs
- **Touch Considerations**: Ideal for touch interfaces, easily tappable

#### Medium Buttons (Default)
- **Dimensions**: Height 36-44px, padding 16px horizontal
- **Typography**: Standard text (14-16px)
- **Usage**: Most interface contexts, forms, dialogs
- **Touch Considerations**: Acceptable for touch with sufficient spacing

#### Small Buttons
- **Dimensions**: Height 28-32px, padding 8-12px horizontal
- **Typography**: Smaller text (12-14px)
- **Usage**: Compact UIs, toolbars, data tables, space-constrained areas
- **Touch Considerations**: Should be used sparingly in touch interfaces

### Layout Patterns

#### Button Groups
- **Horizontal Alignment**: 
  - Place primary action on the right in LTR languages (left in RTL)
  - Maintain 8-16px spacing between buttons
  - Align buttons of the same type (e.g., all "Cancel" buttons align across contexts)

- **Vertical Stacking**:
  - Full-width buttons on mobile
  - Primary action at the bottom/most accessible position on mobile
  - Maintain 8-16px vertical spacing

#### Button Bars
- **Toolbar Pattern**:
  - Equal spacing between related buttons
  - Group related actions with separators when needed
  - Consistent height and treatment
  - Often uses icon buttons with tooltips

- **Form Actions**:
  - Right-aligned (LTR) at the bottom of forms
  - Cancel action to the left of submit/confirm
  - Align with the content container edges

### Special Button Types

#### Icon Buttons
- **Purpose**: Space-efficient controls, universal symbols
- **Dimensions**: Minimum 44×44px touch target regardless of icon size
- **Implementation**:
  - Icon should be clear and recognizable (universal symbols preferred)
  - Include tooltip or accessible label
  - Provide the same states as text buttons
  - Consider adding text labels for important actions

#### Toggle Buttons
- **Purpose**: Controls with binary states (on/off, active/inactive)
- **Implementation**:
  - Clear visual difference between states
  - Selected state often uses filled style similar to primary buttons
  - Often used in button groups where only one can be selected
  - Maintains pressed/selected state until clicked again

#### Floating Action Buttons (FAB)
- **Purpose**: Highlight the primary action of a screen
- **Implementation**:
  - Circular or pill-shaped button that "floats" above the interface
  - Higher elevation (shadow) than other elements
  - Typically uses primary brand color
  - Fixed position, often bottom-right
  - Should be used sparingly (one per screen)

#### Split Buttons
- **Purpose**: Provide a default action with related alternatives
- **Implementation**:
  - Main action area plus dropdown trigger
  - Clear visual separation between primary action and dropdown
  - Dropdown reveals related alternative actions
  - Follows same hierarchy rules as standard buttons

## Decision Logic for Implementation

When designing and implementing buttons:

1. **Determine Action Importance**
   - Is this the main action users should take?
   - How frequently will users need this action?
   - What happens if users miss or overlook this action?
   - Where does this action fit in the overall user flow?

2. **Select Appropriate Hierarchy**
   - Primary: Main action, what most users need to do
   - Secondary: Alternative actions, important but not the main path
   - Tertiary: Supplementary actions, available but less common

3. **Choose Size Based on Context**
   - What's the available space in the interface?
   - How important is the visibility of this action?
   - Is this a touch interface requiring larger targets?
   - What size do other buttons use in similar contexts?

4. **Craft Effective Button Text**
   - Use action verbs that clearly communicate the outcome
   - Be specific about what happens ("Save Changes" vs just "Save")
   - Keep text concise (1-3 words typically)
   - Ensure consistency with other similar actions
   - Consider whether an icon would enhance understanding

5. **Define All Required States**
   - Default: Normal resting state
   - Hover: Mouse pointer over button
   - Focus: Keyboard navigation focus
   - Active/Pressed: During click/tap
   - Disabled: Action unavailable
   - Loading: Action in progress
   - Success/Error: Action result

6. **Validate Accessibility**
   - Does it meet contrast requirements? (4.5:1 for AA compliance)
   - Is it keyboard navigable?
   - Does it have appropriate ARIA attributes if needed?
   - Is the text understandable when read by screen readers?
   - Is the touch target large enough? (minimum 44×44px)
   - Does it scale appropriately with text size changes?

## Code Translation

### CSS Implementation (Design System Variables)
```css
:root {
  /* Colors */
  --color-primary: #0066cc;
  --color-primary-dark: #0052a3;
  --color-neutral-50: #f9fafb;
  --color-neutral-100: #f3f4f6;
  --color-neutral-200: #e5e7eb;
  --color-neutral-300: #d1d5db;
  --color-neutral-600: #4b5563;
  --color-neutral-700: #374151;
  --color-neutral-800: #1f2937;
  
  /* Sizes */
  --button-height-sm: 32px;
  --button-height-md: 40px;
  --button-height-lg: 48px;
  
  /* Radii */
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  
  /* Typography */
  --font-size-sm: 14px;
  --font-size-md: 16px;
  --font-size-lg: 18px;
  
  /* Transitions */
  --transition-button: 150ms ease-in-out;
}

/* Base Button Styles */
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  border-radius: var(--radius-md);
  transition: all var(--transition-button);
  cursor: pointer;
  font-family: inherit;
  border: 1px solid transparent;
  white-space: nowrap;
  
  /* Base focus styles */
  &:focus-visible {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
  }
  
  /* Disabled state */
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

/* Size variants */
.button--small {
  height: var(--button-height-sm);
  padding: 0 12px;
  font-size: var(--font-size-sm);
  border-radius: var(--radius-sm);
}

.button--medium {
  height: var(--button-height-md);
  padding: 0 16px;
  font-size: var(--font-size-md);
}

.button--large {
  height: var(--button-height-lg);
  padding: 0 24px;
  font-size: var(--font-size-lg);
  border-radius: var(--radius-lg);
}

/* Hierarchy variants */
.button--primary {
  background-color: var(--color-primary);
  color: white;
  
  &:hover:not(:disabled) {
    background-color: var(--color-primary-dark);
  }
  
  &:active:not(:disabled) {
    transform: translateY(1px);
  }
}

.button--secondary {
  background-color: var(--color-neutral-50);
  border: 1px solid var(--color-neutral-300);
  color: var(--color-neutral-800);
  
  &:hover:not(:disabled) {
    background-color: var(--color-neutral-100);
    border-color: var(--color-neutral-400);
  }
  
  &:active:not(:disabled) {
    background-color: var(--color-neutral-200);
    transform: translateY(1px);
  }
}

.button--tertiary {
  background-color: transparent;
  color: var(--color-primary);
  
  &:hover:not(:disabled) {
    background-color: var(--color-neutral-50);
    text-decoration: underline;
  }
  
  &:active:not(:disabled) {
    background-color: var(--color-neutral-100);
  }
}

/* Icon support */
.button__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.button__icon--left {
  margin-right: 8px;
}

.button__icon--right {
  margin-left: 8px;
}

/* Loading state */
.button--loading {
  position: relative;
  color: transparent;
  pointer-events: none;
  
  &::after {
    content: "";
    position: absolute;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    border: 2px solid currentColor;
    border-right-color: transparent;
    animation: button-spinner 0.75s linear infinite;
  }
}

@keyframes button-spinner {
  to { transform: rotate(360deg); }
}
```

### React Component Implementation
```tsx
import React from 'react';
import classNames from 'classnames';

export type ButtonSize = 'small' | 'medium' | 'large';
export type ButtonVariant = 'primary' | 'secondary' | 'tertiary';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /** Button display variant that affects appearance */
  variant?: ButtonVariant;
  /** Button size */
  size?: ButtonSize;
  /** Shows loading spinner and disables button */
  isLoading?: boolean;
  /** Icon displayed before button text */
  iconLeft?: React.ReactNode;
  /** Icon displayed after button text */
  iconRight?: React.ReactNode;
  /** Full width button */
  fullWidth?: boolean;
  /** Button contents */
  children: React.ReactNode;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'medium',
      isLoading = false,
      iconLeft,
      iconRight,
      fullWidth = false,
      disabled = false,
      className,
      children,
      ...props
    },
    ref
  ) => {
    const buttonClasses = classNames(
      'button',
      `button--${variant}`,
      `button--${size}`,
      {
        'button--loading': isLoading,
        'button--full-width': fullWidth,
      },
      className
    );

    return (
      <button
        ref={ref}
        className={buttonClasses}
        disabled={disabled || isLoading}
        {...props}
      >
        {iconLeft && <span className="button__icon button__icon--left">{iconLeft}</span>}
        <span className="button__text">{children}</span>
        {iconRight && <span className="button__icon button__icon--right">{iconRight}</span>}
      </button>
    );
  }
);

Button.displayName = 'Button';
```

### HTML/Tailwind Implementation
```html
<!-- Primary Button (Default/Medium) -->
<button class="inline-flex items-center justify-center px-4 py-2 text-base font-medium text-white bg-blue-600 rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
  Save Changes
</button>

<!-- Secondary Button -->
<button class="inline-flex items-center justify-center px-4 py-2 text-base font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
  Cancel
</button>

<!-- Tertiary/Text Button -->
<button class="inline-flex items-center justify-center px-4 py-2 text-base font-medium text-blue-600 bg-transparent hover:bg-blue-50 hover:underline focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
  Learn More
</button>

<!-- Large Primary Button -->
<button class="inline-flex items-center justify-center px-6 py-3 text-lg font-medium text-white bg-blue-600 rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
  Create Account
</button>

<!-- Small Secondary Button -->
<button class="inline-flex items-center justify-center px-3 py-1.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
  Apply Filter
</button>

<!-- Icon Button -->
<button class="inline-flex items-center justify-center p-2 text-gray-500 bg-white rounded-full hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500" aria-label="Add item">
  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
    <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
  </svg>
</button>

<!-- Disabled Button -->
<button class="inline-flex items-center justify-center px-4 py-2 text-base font-medium text-white bg-blue-600 rounded-md opacity-50 cursor-not-allowed" disabled>
  Submit Form
</button>

<!-- Loading Button -->
<button class="relative inline-flex items-center justify-center px-4 py-2 text-base font-medium text-transparent bg-blue-600 rounded-md shadow-sm cursor-wait">
  <span class="absolute inset-0 flex items-center justify-center">
    <svg class="w-5 h-5 text-white animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
  </span>
  Processing
</button>
```

## Anti-Patterns

### Inconsistent Visual Hierarchy
- **Problem**: Using the same button style for actions of different importance
- **Why It's Bad**: Creates confusion about which actions are primary vs. secondary
- **Solution**: Establish clear visual distinction between primary, secondary, and tertiary buttons

### Ambiguous Button Labels
- **Problem**: Vague or generic button text like "OK", "Click Here", or "Submit"
- **Why It's Bad**: Fails to communicate the specific outcome of the interaction
- **Solution**: Use specific, action-oriented verbs that clearly describe the outcome

### Excessive Button Count
- **Problem**: Too many buttons of equal visual weight in the same context
- **Why It's Bad**: Creates decision paralysis and visual clutter
- **Solution**: Limit the number of primary actions, use dropdown menus for related actions, and consider moving less important actions to menus

### Insufficient Touch Targets
- **Problem**: Buttons that are too small or too close together for touch interaction
- **Why It's Bad**: Creates frustration through accidental taps or difficulty hitting targets
- **Solution**: Ensure minimum touch target size of 44×44px and adequate spacing (at least 8px)

### Missing or Inadequate States
- **Problem**: Buttons lacking clear hover, focus, active, or disabled states
- **Why It's Bad**: Reduces usability, especially for keyboard users and those with disabilities
- **Solution**: Design and implement all interactive states with sufficient visual distinction

### Ghost Buttons with Poor Contrast
- **Problem**: Outline/ghost buttons with insufficient contrast against backgrounds
- **Why It's Bad**: Reduces visibility and may fail accessibility requirements
- **Solution**: Ensure sufficient contrast between button borders/text and backgrounds, test against various backgrounds

### Misleading Button Styles
- **Problem**: Using standard button styling for non-button elements (links styled as buttons)
- **Why It's Bad**: Creates confusion about expected behavior and accessibility issues
- **Solution**: Use semantic HTML, style links as links and buttons as buttons, or use proper ARIA roles

### Unreachable or Poorly Placed Buttons
- **Problem**: Primary actions placed in non-standard locations or difficult to reach areas
- **Why It's Bad**: Reduces discoverability and increases interaction cost
- **Solution**: Place primary actions in prominent, predictable locations following platform conventions

## Reasoning Principles

Effective button design works because it:

1. **Reduces Cognitive Load** - Clear button hierarchy helps users quickly identify the most important actions without having to evaluate every option
   
2. **Leverages Learned Patterns** - Consistent button styling creates predictable interactions that users can apply across the interface

3. **Provides Interaction Feedback** - State changes confirm user actions and maintain system status awareness

4. **Creates Focus Through Contrast** - Strategic use of color, size, and placement draws attention to primary pathways

5. **Supports Multiple Interaction Modes** - Proper implementation supports mouse, touch, and keyboard interaction patterns

6. **Builds Behavioral Momentum** - Well-designed button flows guide users through multi-step processes smoothly

7. **Eliminates Uncertainty** - Clear labeling and consistent positioning reduce hesitation and improve task completion

## Related Concepts

- **Visual Hierarchy** - Button styling is a key application of visual hierarchy principles
- **Color Theory** - Button colors significantly influence perception of importance and function
- **Typography** - Text legibility and styling affects button clarity and usability
- **Spacing Systems** - Button padding and margins connect to the overall spacing rhythm
- **Accessibility** - Button implementation must consider keyboard navigation, screen readers, and other assistive technologies
- **Form Design** - Buttons often serve as form controls and submission mechanisms
- **Interaction Patterns** - Buttons initiate many standard interaction flows like dialogs
- **Responsive Design** - Button placement and sizing must adapt across device contexts
