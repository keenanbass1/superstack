# WCAG Guidelines Overview

The Web Content Accessibility Guidelines (WCAG) define how to make web content more accessible. This document covers essential success criteria from WCAG 2.1.

## Conformance Levels

WCAG defines three levels of conformance:
- **Level A**: Minimum level (must satisfy)
- **Level AA**: Mid-range level (should satisfy)
- **Level AAA**: Highest level (may satisfy where possible)

Most organizations aim for Level AA compliance, which includes all Level A criteria plus additional requirements.

## Essential Success Criteria

### Perceivable

#### 1.1.1 Non-text Content (Level A)
- All images need alt text
- Decorative images need empty alt attributes (alt="")
- Form controls need labels
- Audio/video needs text alternatives

**Example:**
```html
<!-- Good -->
<img src="chart.png" alt="Sales increased by 25% in Q4 2024">

<!-- Bad -->
<img src="chart.png">
```

#### 1.2.2 Captions (Level A)
- All pre-recorded video with audio needs captions

**Example:**
```html
<video controls>
  <source src="video.mp4" type="video/mp4">
  <track src="captions.vtt" kind="subtitles" srclang="en" label="English">
  Your browser does not support the video tag.
</video>
```

#### 1.3.1 Info and Relationships (Level A)
- Use semantic HTML to convey structure
- Associate form labels with inputs
- Use proper table markup with headers

**Example:**
```html
<!-- Good -->
<label for="name">Name:</label>
<input id="name" type="text">

<!-- Bad -->
Name:
<input type="text">
```

#### 1.4.3 Contrast (Level AA)
- Text needs 4.5:1 contrast ratio with background
- Large text (18pt+) needs 3:1 contrast ratio
- UI components and graphical objects need 3:1 contrast

**Example:**
```css
/* Good contrast */
.text {
  color: #333; /* Dark gray */
  background-color: #fff; /* White */
}

/* Poor contrast */
.text {
  color: #999; /* Light gray */
  background-color: #fff; /* White */
}
```

### Operable

#### 2.1.1 Keyboard (Level A)
- All functionality available via keyboard
- No keyboard traps

**Example:**
```javascript
// Good - custom button with keyboard support
const button = document.querySelector('.custom-button');
button.addEventListener('click', doSomething);
button.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    doSomething();
    e.preventDefault();
  }
});
```

#### 2.4.3 Focus Order (Level A)
- Focus order preserves meaning and operability
- Tabbing follows logical sequence

#### 2.4.7 Focus Visible (Level AA)
- Keyboard focus indicator is visible

**Example:**
```css
/* Good - Don't remove focus outline without replacement */
:focus {
  outline: 2px solid #007bff;
}

/* Bad - Removing focus without replacement */
:focus {
  outline: none;
}
```

### Understandable

#### 3.1.1 Language of Page (Level A)
- Page language is specified in HTML

**Example:**
```html
<html lang="en">
```

#### 3.2.2 On Input (Level A)
- Changing a setting doesn't automatically change context
- Users are warned before significant changes

#### 3.3.2 Labels or Instructions (Level A)
- Form inputs have clear labels
- Required fields are indicated

**Example:**
```html
<label for="email">Email address <span aria-label="required">*</span></label>
<input id="email" type="email" required>
```

### Robust

#### 4.1.1 Parsing (Level A)
- HTML is properly formed with complete start/end tags
- Elements are properly nested

#### 4.1.2 Name, Role, Value (Level A)
- All UI components have accessible names
- Custom controls use proper ARIA roles

**Example:**
```html
<div role="button" tabindex="0" aria-pressed="false">Toggle</div>
```