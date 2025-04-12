# Accessibility Checklists

These practical checklists help ensure your web content meets accessibility requirements at different stages of development.

## Design Phase Checklist

### Color and Visual Design
- [ ] Color contrast meets WCAG AA standards (4.5:1 for normal text, 3:1 for large text)
- [ ] Information is not conveyed by color alone
- [ ] UI maintains sufficient contrast in light and dark modes
- [ ] Text can resize up to 200% without loss of content or functionality
- [ ] Layout works at different viewport sizes (responsive design)
- [ ] Focus indicators are clearly visible
- [ ] Visual hierarchy is clear and logical

### User Experience
- [ ] Interactions are designed with keyboard navigation in mind
- [ ] Touch targets are at least 44x44 pixels
- [ ] Error states are clearly indicated visually
- [ ] Required fields are clearly marked
- [ ] Form validation messages are clear and helpful
- [ ] Content is organized with a clear hierarchy and structure
- [ ] Reading order is logical and follows visual layout

## Development Phase Checklist

### Semantic HTML
- [ ] Proper HTML5 document structure (`<!DOCTYPE html>`, `<html lang="en">`, etc.)
- [ ] Headings follow a logical hierarchy (`h1` → `h2` → `h3`, etc.)
- [ ] Lists are marked up with `<ul>`, `<ol>`, or `<dl>`
- [ ] Landmarks are used appropriately (`<header>`, `<nav>`, `<main>`, `<footer>`, etc.)
- [ ] Tables use appropriate headers (`<th>`) with scope attributes
- [ ] Forms use explicit labels with `for` attributes connecting to input IDs
- [ ] Buttons use `<button>` elements, links use `<a href="...">` elements
- [ ] Custom widgets use appropriate ARIA roles and states

### Keyboard and Focus Management
- [ ] All interactive elements are keyboard accessible
- [ ] Focus order follows a logical sequence
- [ ] Focus is trapped appropriately in modals/dialogs
- [ ] Custom widgets have proper keyboard interactions
- [ ] Skip links are provided for navigation
- [ ] Focus is managed when content updates dynamically
- [ ] No keyboard traps exist

### Images and Media
- [ ] All informative images have descriptive alt text
- [ ] Decorative images have empty alt text (`alt=""`)
- [ ] Complex images have extended descriptions
- [ ] SVGs include title and description as needed
- [ ] Videos have captions
- [ ] Audio content has transcripts
- [ ] No content auto-plays for more than 3 seconds
- [ ] Media players have accessible controls

### ARIA and Advanced Semantics
- [ ] ARIA is only used when HTML semantics aren't sufficient
- [ ] Required ARIA attributes are included for each role
- [ ] Dynamic content updates use appropriate `aria-live` regions
- [ ] Modal dialogs use `aria-modal="true"` and manage focus
- [ ] Custom widgets follow WAI-ARIA Authoring Practices
- [ ] Form fields use appropriate ARIA attributes when needed
- [ ] Error messages are connected to form fields with `aria-describedby`

### Forms and User Input
- [ ] All form controls have associated labels
- [ ] Required fields use the `required` attribute and visual indicators
- [ ] Error messages are programmatically associated with fields
- [ ] Form validation provides clear guidance for fixing errors
- [ ] Success and error states are announced to screen readers
- [ ] Complex forms are divided into manageable sections
- [ ] Autocomplete attributes are used appropriately

## Testing Phase Checklist

### Automated Testing
- [ ] Run axe or similar automated testing tool
- [ ] Check HTML validation
- [ ] Test with Lighthouse accessibility audit
- [ ] Validate color contrast with a contrast checker
- [ ] Test text resizing up to 200%
- [ ] Test page zooming up to 400%
- [ ] Check for valid landmarks and heading structure

### Manual Testing
- [ ] Complete keyboard-only navigation test
- [ ] Test with at least one screen reader (NVDA, JAWS, VoiceOver)
- [ ] Check focus visibility and order
- [ ] Verify form error handling and messaging
- [ ] Test with browser zoom and text resizing
- [ ] Verify that all media has appropriate alternatives
- [ ] Check dynamic content updates with screen reader

### User Testing
- [ ] Include users with disabilities in testing
- [ ] Test with keyboard-only users
- [ ] Test with screen reader users
- [ ] Test with users with low vision
- [ ] Test with users with cognitive disabilities
- [ ] Test with users with motor disabilities
- [ ] Document findings and make improvements

## Specific Component Checklists

### Navigation
- [ ] Navigation is marked with `<nav>` or `role="navigation"`
- [ ] Current page/location is indicated visually and programmatically
- [ ] Skip links are provided to bypass repetitive navigation
- [ ] Dropdown menus are keyboard accessible
- [ ] Submenus open on click/Enter, not just hover
- [ ] Navigation items have sufficient touch target size
- [ ] Mobile navigation is accessible via keyboard and touch

### Buttons and Links
- [ ] Buttons use `<button>` elements
- [ ] Links use `<a>` elements with href attributes
- [ ] Button/link text is descriptive and unique
- [ ] Icons have accessible text alternatives
- [ ] Clickable areas are sufficiently sized
- [ ] States (hover, focus, active, disabled) are clearly indicated
- [ ] Disabled elements have appropriate `disabled` or `aria-disabled` attributes

### Forms
- [ ] Form elements have associated labels
- [ ] Fieldsets group related form elements
- [ ] Required fields are marked programmatically and visually
- [ ] Error messages are clear and programmatically linked to inputs
- [ ] Success states are communicated to all users
- [ ] Form controls maintain sufficient color contrast
- [ ] Instructions are clear and available to all users

### Tables
- [ ] Tables use appropriate headers with `<th>` elements
- [ ] Complex tables use `scope`, `headers`, or `id` attributes
- [ ] Tables include a caption or accessible name
- [ ] Data cells use `<td>` elements
- [ ] Presentational tables (used for layout) use `role="presentation"`
- [ ] Table structure is simple and logical
- [ ] Responsive tables maintain accessibility on mobile

### Modals and Dialogs
- [ ] Dialog role is used: `role="dialog"` or native `<dialog>`
- [ ] Modal dialogs use `aria-modal="true"`
- [ ] Dialogs have an accessible name via `aria-labelledby` or `aria-label`
- [ ] Focus moves to the dialog when opened
- [ ] Focus is trapped within the dialog
- [ ] Dialog can be closed via keyboard (Escape key)
- [ ] Focus returns to triggering element when closed

### Tabs
- [ ] Tab list uses `role="tablist"` (unless using native `<tablist>`)
- [ ] Tab items use `role="tab"` with `aria-selected` states
- [ ] Tab panels use `role="tabpanel"`
- [ ] Tabs and panels are connected with `aria-controls` and `aria-labelledby`
- [ ] Keyboard navigation implemented (Arrow keys, Home/End)
- [ ] Selected tab is visually distinct
- [ ] Tab content is accessible and well structured

### Accordions
- [ ] Accordion headers use appropriate heading elements
- [ ] Toggle buttons use `aria-expanded` state
- [ ] Accordion panels are connected to headers with `aria-controls` and `aria-labelledby`
- [ ] Accordions can be operated with keyboard (Enter/Space to toggle)
- [ ] Current state is clearly visible
- [ ] Content within accordion is properly structured
- [ ] Opening one panel doesn't automatically close others (unless intended)

### Carousels
- [ ] Slides are keyboard accessible
- [ ] Current slide is indicated visually and programmatically
- [ ] Controls have appropriate text alternatives
- [ ] Auto-rotation can be paused
- [ ] Carousel respects reduced motion preferences
- [ ] Hidden slides are properly removed from focus order or accessible
- [ ] Carousel has an accessible name

### Dropdown Menus
- [ ] Dropdown trigger indicates expandable content (`aria-haspopup`, `aria-expanded`)
- [ ] Menu items use appropriate roles (`menuitem`, `menuitemcheckbox`, etc.)
- [ ] Keyboard navigation is implemented (Arrow keys, Escape to close)
- [ ] Focus is managed correctly when opening and closing
- [ ] Open state is visually clear and programmatically indicated
- [ ] Submenus are accessible via keyboard
- [ ] Dropdown closes when focus moves elsewhere

## Accessibility Compliance Checklist (WCAG 2.1 AA)

### Perceivable
- [ ] 1.1.1: Non-text content has text alternatives
- [ ] 1.2.1: Audio-only and video-only content has alternatives
- [ ] 1.2.2: Captions are provided for pre-recorded video with audio
- [ ] 1.2.3: Audio description or transcript for pre-recorded video
- [ ] 1.2.4: Captions for live audio in videos
- [ ] 1.2.5: Audio descriptions for pre-recorded video content
- [ ] 1.3.1: Information and relationships are programmatically available
- [ ] 1.3.2: Content follows a meaningful sequence
- [ ] 1.3.3: Sensory characteristics are not the only way to convey instructions
- [ ] 1.3.4: Content does not restrict its view/operation to single orientation
- [ ] 1.3.5: Input purpose can be programmatically determined
- [ ] 1.4.1: Color is not the only visual means of conveying information
- [ ] 1.4.2: Audio control is available
- [ ] 1.4.3: Text has sufficient contrast with background (4.5:1 ratio)
- [ ] 1.4.4: Text can be resized up to 200% without loss of content
- [ ] 1.4.5: Images of text are not used where actual text would work
- [ ] 1.4.10: Content reflows on small screens without horizontal scrolling
- [ ] 1.4.11: Non-text content has sufficient contrast (3:1 ratio)
- [ ] 1.4.12: Text spacing can be adjusted without loss of content
- [ ] 1.4.13: Content on hover or focus can be dismissed or accessed

### Operable
- [ ] 2.1.1: All functionality is available via keyboard
- [ ] 2.1.2: Keyboard focus is not trapped
- [ ] 2.1.4: Single-key shortcuts can be turned off or remapped
- [ ] 2.2.1: Time limits can be adjusted or extended
- [ ] 2.2.2: Moving/blinking content can be paused, stopped, or hidden
- [ ] 2.3.1: Content does not flash more than 3 times per second
- [ ] 2.4.1: Skip links are available to bypass blocks of repeated content
- [ ] 2.4.2: Pages have descriptive titles
- [ ] 2.4.3: Focus order is logical and meaningful
- [ ] 2.4.4: Link purpose is clear from link text
- [ ] 2.4.5: Multiple ways to find content are available
- [ ] 2.4.6: Headings and labels are descriptive and informative
- [ ] 2.4.7: Keyboard focus is visibly apparent
- [ ] 2.5.1: Gestures are not required (alternatives exist)
- [ ] 2.5.2: Pointer actions can be canceled
- [ ] 2.5.3: Visible text matches accessible name
- [ ] 2.5.4: Functionality operated by motion can also be operated by UI components

### Understandable
- [ ] 3.1.1: Page language is programmatically set
- [ ] 3.1.2: Language of parts can be programmatically determined
- [ ] 3.2.1: Focus doesn't trigger unexpected context changes
- [ ] 3.2.2: User input doesn't trigger unexpected context changes
- [ ] 3.2.3: Navigation is consistent across pages
- [ ] 3.2.4: Components with same functionality are identified consistently
- [ ] 3.3.1: Errors are identified and described to users
- [ ] 3.3.2: Labels or instructions are provided for user input
- [ ] 3.3.3: Error suggestion is provided when detected
- [ ] 3.3.4: Error prevention is available for legal, financial, or data submissions

### Robust
- [ ] 4.1.1: Markup is well-formed with no major validation errors
- [ ] 4.1.2: All UI components have proper names, roles, and values
- [ ] 4.1.3: Status messages can be programmatically determined