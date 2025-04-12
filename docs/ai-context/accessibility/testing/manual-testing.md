# Manual Accessibility Testing Guide

While automated tools like axe and Lighthouse are invaluable, they can only catch about 30-50% of accessibility issues. Manual testing is essential for comprehensive accessibility evaluation.

## Essential Manual Tests

### 1. Keyboard Navigation Testing

**Procedure:**
1. Disconnect your mouse/trackpad
2. Navigate through the entire page using only:
   - Tab: Move forward
   - Shift+Tab: Move backward
   - Enter/Space: Activate controls
   - Arrow keys: Navigate within components

**Check for:**
- All interactive elements are reachable
- Focus order is logical and follows visual layout
- Focus indicator is clearly visible at all times
- No keyboard traps (can't tab out of a component)
- All functionality is available without a mouse
- Custom widgets work with appropriate keyboard interactions

### 2. Screen Reader Testing

**Recommended screen readers:**
- NVDA (Windows, free)
- JAWS (Windows, commercial)
- VoiceOver (Mac/iOS, built-in)
- TalkBack (Android, built-in)

**Basic test procedure:**
1. Navigate the page using the screen reader's navigation commands
2. Interact with all components
3. Fill out and submit forms
4. Navigate through tables and complex content

**Check for:**
- All content is announced correctly
- Images have appropriate alt text
- Headings are properly structured
- Form controls have labels
- Custom widgets have proper ARIA roles and properties
- Status messages are announced
- Dynamic content changes are perceivable

### 3. Zoom and Magnification

**Procedure:**
1. Zoom the page to 200% (browser zoom)
2. Navigate and interact with all components

**Check for:**
- Content doesn't overflow or become truncated
- Text remains readable
- Controls remain usable
- No horizontal scrolling on responsive designs
- Layout adapts appropriately

### 4. Color and Contrast

**Procedure:**
1. Use browser extensions like "Colorblindly" to simulate color blindness
2. Use contrast checkers for specific elements

**Check for:**
- Information is not conveyed by color alone
- UI works in grayscale
- Text meets contrast requirements (4.5:1 for normal text, 3:1 for large text)
- Interactive elements have sufficient contrast against backgrounds

### 5. Content and Structure

**Procedure:**
1. Review the page structure using browser developer tools
2. Check heading hierarchy
3. Examine form field labels and instructions

**Check for:**
- Proper HTML5 semantic elements (<header>, <main>, <nav>, etc.)
- Logical heading hierarchy (h1 → h2 → h3, etc.)
- Lists are properly structured
- Tables have appropriate headers
- Forms have clear labels and instructions
- Language is set properly (html lang attribute)

### 6. Time-Based Content

**Procedure:**
1. Identify content that auto-updates, auto-plays, or has time limits
2. Test pause, stop, or extend functionality

**Check for:**
- Ability to pause/stop auto-playing content
- Options to extend time limits
- No content that flashes more than 3 times per second

### 7. User Control Testing

**Procedure:**
1. Test any functionality that changes context
2. Check form validation and error handling

**Check for:**
- Changes in context only occur when initiated by user
- Error messages are clear and descriptive
- Error messages are programmatically associated with relevant fields
- Suggestions for error correction are provided when possible

## Document and Report Issues

For each identified issue:
1. **Document the problem**: Describe what's happening
2. **Reference standards**: Cite specific WCAG criteria
3. **Provide impact assessment**: How severely does this affect users?
4. **Suggest fixes**: Offer specific solutions
5. **Prioritize**: Rank issues by impact and difficulty to fix

## Manual Testing Checklist

### Perceivable
- [ ] Images have appropriate alt text
- [ ] Videos have captions and audio descriptions
- [ ] Content is readable when zoomed to 200%
- [ ] Color is not used alone to convey information
- [ ] Audio content can be paused and has volume control
- [ ] Page structure uses proper semantic elements

### Operable
- [ ] All functionality works with keyboard alone
- [ ] Focus indicator is visible
- [ ] Focus order is logical
- [ ] No keyboard traps
- [ ] No content flashes more than 3 times per second
- [ ] Page has descriptive title
- [ ] Navigation is consistent across pages

### Understandable
- [ ] Language is specified (lang attribute)
- [ ] Form labels are clear
- [ ] Error messages are helpful
- [ ] Context doesn't change unexpectedly
- [ ] Navigation is consistent
- [ ] Buttons and controls are labeled consistently

### Robust
- [ ] HTML validates without errors
- [ ] ARIA is used appropriately
- [ ] Custom controls have proper roles and states
- [ ] Content works across browsers and assistive technologies
- [ ] Dynamic changes are announced to screen readers

## Tools for Manual Testing

- **Accessibility Insights for Web**: Guided manual testing steps
- **WAVE by WebAIM**: Visual feedback for manual inspections
- **Color Contrast Analyzers**: For checking specific color combinations
- **Screen Readers**: NVDA, JAWS, VoiceOver, TalkBack
- **Keyboard Focus Visualizers**: Shows focus indicator clearly for testing