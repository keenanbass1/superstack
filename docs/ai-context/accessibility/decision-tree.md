# Accessibility Decision Tree

This decision tree helps determine the appropriate accessibility solutions for common web development scenarios.

## Text Alternatives for Images

```
Is the image purely decorative (adds no information)?
├── Yes → Use empty alt text: alt=""
└── No → Does the image contain text?
    ├── Yes → Can the same information be provided as actual text on the page?
    │   ├── Yes → Consider replacing image with actual text and CSS
    │   └── No → Use alt text that includes all text from the image
    └── No → Is the image a complex diagram, chart, or infographic?
        ├── Yes → Provide short alt text + longer description
        │   (using aria-describedby, figure + figcaption, or adjacent text)
        └── No → Provide concise, descriptive alt text that conveys
            the image's purpose and content
```

## Interactive Elements

```
Is it an action that affects the current page?
├── Yes → Use <button> element
└── No → Does it navigate to another page?
    ├── Yes → Use <a> element with href attribute
    └── No → Is it a custom interactive component?
        ├── Yes → Does HTML provide a suitable native element?
        │   ├── Yes → Use the native element
        │   └── No → Create custom component with appropriate:
        │       • Role
        │       • Keyboard support
        │       • Focus management
        │       • ARIA states
        └── No → Reconsider whether interactivity is needed
```

## Form Design

```
For each input in the form:
├── Does the input need a label?
│   ├── Yes (most cases) → Use explicit <label> with for attribute
│   └── No (rare case) → Provide alternative (aria-label or aria-labelledby)
├── Is the input required?
│   ├── Yes → Add 'required' attribute and indicate visually, also use aria-required="true"
│   └── No → No additional attributes needed
├── Does the input need extra instructions?
│   ├── Yes → Add instructions with aria-describedby
│   └── No → No additional attributes needed
└── What happens on errors?
    ├── Provide clear error messages
    ├── Connect errors to inputs using aria-describedby
    └── Set aria-invalid="true" on invalid fields
```

## Color and Contrast

```
For each color combination:
├── Is it text on a background?
│   ├── Yes → Is the text large (18pt+/24px+ or 14pt+/18.5px+ bold)?
│   │   ├── Yes → Minimum 3:1 contrast ratio
│   │   └── No → Minimum 4.5:1 contrast ratio
│   └── No → Is it a UI component or graphic?
│       ├── Yes → Minimum 3:1 contrast ratio for boundaries/edges
│       └── No → No specific contrast requirement
└── Is meaning conveyed by color alone?
    ├── Yes → Add additional cues (patterns, icons, text)
    └── No → No additional cues needed
```

## ARIA Usage

```
Do you need to add ARIA to an element?
├── Can you use a native HTML element/attribute instead?
│   ├── Yes → Use native HTML (preferred)
│   └── No → Continue with ARIA assessment
├── Are you changing the element's role?
│   ├── Yes → Ensure you implement all required attributes for that role
│   └── No → No role attribute needed
├── Are you adding a property/state?
│   ├── Yes → Is it a property (unchanging) or state (changes)?
│   │   ├── Property → Use aria-* attribute appropriately
│   │   └── State → Use aria-* attribute + update with JavaScript as needed
│   └── No → No aria-* attributes needed
└── Are you hiding/showing content?
    ├── Visually hidden, available to screen readers → Use sr-only pattern
    ├── Hidden from everyone → Use hidden attribute
    └── Hidden from screen readers only → Use aria-hidden="true"
```

## Keyboard Navigation

```
For each interactive element:
├── Can it be reached with Tab key?
│   ├── Yes → Ensure visible focus styles
│   └── No → Add tabindex="0" (but prefer fixing HTML semantics)
├── Is it a custom widget with subcomponents?
│   ├── Yes → Implement keyboard pattern for that widget type:
│   │   • Menu/listbox: Arrow keys, Home/End, typeahead
│   │   • Tabs: Arrow keys, Home/End
│   │   • Tree: Arrow keys, Home/End, typeahead
│   │   • etc.
│   └── No → Ensure activation with Enter/Space as needed
└── Is there a focus order issue?
    ├── Yes → Fix tab order with document structure (preferred) 
    │   or tabindex (if necessary)
    └── No → No additional work needed
```

## Headings and Structure

```
For each page:
├── Does it have a unique, descriptive title?
│   ├── Yes → Good
│   └── No → Add appropriate <title> in <head>
├── Does it use heading elements (h1-h6)?
│   ├── Yes → Do they follow a logical hierarchy?
│   │   ├── Yes → Good
│   │   └── No → Restructure headings to follow proper hierarchy
│   └── No → Add semantic headings
└── Does it use semantic landmarks?
    ├── Yes → Ensure they're used appropriately
    └── No → Add appropriate landmarks:
        • header
        • nav
        • main
        • footer
        • aside
        • section (with aria-label)
```

## Responsive Design and Zoom

```
Does the design work at:
├── 320px viewport width?
│   ├── Yes → Good
│   └── No → Fix narrow viewport layout
├── 200% zoom?
│   ├── Yes → Good
│   └── No → Ensure layout functions at high zoom
├── 400% zoom?
│   ├── Yes → Good (AAA level)
│   └── No → Consider improvements for better AAA compliance
└── With enlarged text (browser settings)?
    ├── Yes → Good
    └── No → Fix layout issues with enlarged text
```

## Videos and Multimedia

```
For each video:
├── Does it have audio?
│   ├── Yes → Provide captions
│   └── No → No captions needed
├── Does it have visual information not conveyed by audio?
│   ├── Yes → Provide audio descriptions or descriptive transcript
│   └── No → No audio descriptions needed
└── Is there an alternative for users who can't access the video?
    ├── Yes → Good
    └── No → Provide full transcript
```

## Dynamic Content and AJAX

```
When content changes dynamically:
├── Is it a critical update users need to know about?
│   ├── Yes → Is it an alert or status update?
│   │   ├── Alert (important, interrupting) → Use role="alert"
│   │   └── Status (non-critical) → Use role="status"
│   └── No → No special announcement needed
├── Are you replacing/updating existing content?
│   ├── Yes → Use aria-live="polite" (usually) or aria-live="assertive" (critical)
│   └── No → No aria-live needed
└── Does the update change context or focus?
    ├── Yes → Is it in response to user action?
    │   ├── Yes → Should focus move to the new content?
    │   │   ├── Yes → Set focus programmatically to new content
    │   │   └── No → Maintain focus on triggering element
    │   └── No → Don't change context without user action
    └── No → No focus management needed
```

## Mobile and Touch Accessibility

```
For touch interfaces:
├── Are touch targets at least 44x44px?
│   ├── Yes → Good
│   └── No → Increase target size
├── Is the content accessible in portrait and landscape?
│   ├── Yes → Good
│   └── No → Fix orientation issues
├── Are gestures simple?
│   ├── Yes → Good
│   └── No → Provide simpler alternatives or instructions
└── Is there an alternative to hover/hover+click actions?
    ├── Yes → Good
    └── No → Provide touch-friendly alternatives
```

## Cognitive Accessibility

```
For content and interactions:
├── Is text written in plain language?
│   ├── Yes → Good
│   └── No → Simplify language, define terms, provide summaries
├── Are instructions clear and concise?
│   ├── Yes → Good
│   └── No → Simplify and clarify instructions
├── Are error messages helpful and specific?
│   ├── Yes → Good
│   └── No → Rewrite error messages to be specific and action-oriented
├── Is there visual consistency across the interface?
│   ├── Yes → Good
│   └── No → Create visual patterns and consistency
└── Are there time constraints or timeouts?
    ├── Yes → Can users extend or remove time limits?
    │   ├── Yes → Good
    │   └── No → Add ability to extend time limits
    └── No → Good
```

## Testing and Validation

```
For each accessibility test:
├── Has automated testing been performed?
│   ├── Yes → Were issues found?
│   │   ├── Yes → Fix issues and retest
│   │   └── No → Continue with manual testing
│   └── No → Run automated tests with axe, Lighthouse, or similar
├── Has keyboard testing been performed?
│   ├── Yes → Were issues found?
│   │   ├── Yes → Fix keyboard issues and retest
│   │   └── No → Continue with screen reader testing
│   └── No → Perform keyboard testing
├── Has screen reader testing been performed?
│   ├── Yes → Were issues found?
│   │   ├── Yes → Fix screen reader issues and retest
│   │   └── No → Continue with visual testing
│   └── No → Perform screen reader testing
└── Has testing with users with disabilities been conducted?
    ├── Yes → Were issues found?
    │   ├── Yes → Fix issues and retest
    │   └── No → Good, continue monitoring
    └── No → Consider testing with users with disabilities
```

## Custom Component Selection

```
Need to implement a custom interface component?
├── Is there a native HTML element that could work?
│   ├── Yes → Use the native element (e.g., <select>, <button>)
│   └── No → Does the WAI-ARIA Authoring Practices Guide have a pattern?
│       ├── Yes → Follow the ARIA pattern's keyboard and attribute guidance
│       └── No → Design a custom solution based on similar patterns:
│           • Define a clear, appropriate role
│           • Implement keyboard interactions
│           • Provide proper ARIA attributes
│           • Manage focus appropriately
│           • Test thoroughly with assistive technology
```

## Progressive Enhancement

```
For each feature:
├── Is the core functionality available without JavaScript?
│   ├── Yes → Good
│   └── No → Can a simpler version work without JS?
│       ├── Yes → Implement basic version, then enhance
│       └── No → Ensure JS failure is handled gracefully
├── Does it work with only keyboard?
│   ├── Yes → Good
│   └── No → Implement keyboard support first
├── Is content available without CSS?
│   ├── Yes → Good
│   └── No → Fix HTML structure for logical reading order
└── Does the enhancement maintain accessibility?
    ├── Yes → Good
    └── No → Revise enhancement to preserve accessibility
```

## Use this decision tree as a guide when implementing or reviewing web interfaces to ensure you're considering the key aspects of accessibility. Remember that accessibility is not a checklist but a continuous process of improving the experience for all users.
