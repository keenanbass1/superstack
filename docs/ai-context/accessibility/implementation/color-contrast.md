# Color Contrast and Color Use

Proper color use and sufficient contrast are essential for users with low vision, color blindness, or those using devices in bright environments.

## Color Contrast Requirements

### Text Contrast Ratios (WCAG)

- **Normal Text (AA)**: 4.5:1 minimum contrast ratio
- **Large Text (AA)**: 3:1 minimum contrast ratio (18pt+ or 14pt+ bold)
- **Normal Text (AAA)**: 7:1 minimum contrast ratio
- **Large Text (AAA)**: 4.5:1 minimum contrast ratio

### UI Component Contrast (WCAG 2.1)

- **UI Components and Graphics**: 3:1 minimum contrast against adjacent colors

## Checking Contrast Ratios

### Contrast Ratio Formula

Contrast ratio = (L1 + 0.05) / (L2 + 0.05)

Where:
- L1 is the relative luminance of the lighter color
- L2 is the relative luminance of the darker color

### Using Tools

Online tools for checking contrast:
- WebAIM Contrast Checker
- Colour Contrast Analyzer
- Accessible Color Matrix

Code example using JavaScript to calculate contrast:

```javascript
// Calculate relative luminance (simplified)
function getLuminance(rgb) {
  const [r, g, b] = rgb.map(v => {
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  });
  
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

// Calculate contrast ratio
function getContrastRatio(rgb1, rgb2) {
  const l1 = getLuminance(rgb1);
  const l2 = getLuminance(rgb2);
  
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  
  return (lighter + 0.05) / (darker + 0.05);
}

// Example usage
const backgroundColor = [255, 255, 255]; // White
const textColor = [102, 102, 102]; // Medium gray
const ratio = getContrastRatio(backgroundColor, textColor);
console.log(`Contrast ratio: ${ratio.toFixed(2)}:1`);

// Check if meets WCAG AA for normal text
const meetsWCAGAA = ratio >= 4.5;
console.log(`Meets WCAG AA for normal text: ${meetsWCAGAA}`);
```

## Implementing Good Contrast

### Text Examples

```css
/* Good contrast (7.8:1 ratio) */
.good-contrast {
  color: #333; /* Dark gray text */
  background-color: #fff; /* White background */
}

/* Insufficient contrast (2.6:1 ratio) */
.poor-contrast {
  color: #999; /* Light gray text */
  background-color: #fff; /* White background */
}

/* Good contrast for large text (4.2:1 ratio) */
.large-text {
  font-size: 24px;
  color: #666; /* Medium gray text */
  background-color: #fff; /* White background */
}
```

### UI Components

```css
/* Good contrast for UI components */
.button {
  color: white;
  background-color: #0056b3; /* Sufficient contrast with white text */
  border: none;
  padding: 8px 16px;
}

/* Focus indicators with good contrast */
.button:focus {
  outline: 3px solid #ff9000; /* High contrast focus ring */
  outline-offset: 2px;
}

/* Form controls with sufficient contrast */
.input {
  border: 2px solid #666; /* Border with 4.5:1 contrast against white */
  background-color: white;
  color: #333;
}
```

## Color Blindness Considerations

About 8% of men and 0.5% of women have some form of color blindness. The most common type is red-green color blindness.

### Don't Rely on Color Alone

Always use multiple cues beyond color to convey information:

```html
<!-- Bad: Color alone indicates required field -->
<style>
  .required-field { color: red; }
</style>
<label class="required-field">Name</label>
<input type="text">

<!-- Good: Uses symbol and text in addition to color -->
<style>
  .required-field { color: red; }
  .required-symbol::after { content: " *"; }
</style>
<label class="required-field">
  Name<span class="required-symbol" aria-label="required"></span>
</label>
<input type="text" aria-required="true">
<p>Fields marked with <span aria-hidden="true">*</span> are required</p>
```

### Form Validation

```html
<!-- Bad: Error indication with color only -->
<style>
  .error { border-color: red; }
</style>
<input type="email" class="error">

<!-- Good: Error with multiple cues -->
<style>
  .error { 
    border-color: red;
    background-image: url('error-icon.svg');
    background-repeat: no-repeat;
    background-position: right 8px center;
  }
</style>
<input 
  type="email" 
  class="error" 
  aria-invalid="true" 
  aria-describedby="email-error">
<p id="email-error" class="error-message">
  <span aria-hidden="true">❌</span> Please enter a valid email address
</p>
```

### Charts and Graphs

```html
<!-- Bad: Color-only differentiation -->
<div class="pie-chart">
  <!-- Chart with red, green, blue sections -->
</div>

<!-- Good: Multiple visual cues -->
<div class="pie-chart">
  <!-- Chart with different colors, patterns, and labels -->
</div>
<ul class="chart-legend">
  <li>
    <span class="legend-swatch" style="background: #ff0000; background-image: url('pattern1.svg');"></span>
    Revenue (35%)
  </li>
  <li>
    <span class="legend-swatch" style="background: #00ff00; background-image: url('pattern2.svg');"></span>
    Expenses (42%)
  </li>
  <li>
    <span class="legend-swatch" style="background: #0000ff; background-image: url('pattern3.svg');"></span>
    Profit (23%)
  </li>
</ul>
```

## Customizable Color Schemes

Allow users to choose their preferred color scheme:

```html
<div class="theme-switcher">
  <h3>Theme Preferences</h3>
  
  <div class="color-options">
    <button 
      id="default-theme" 
      class="theme-button" 
      aria-pressed="true">
      Default
    </button>
    
    <button 
      id="high-contrast-theme" 
      class="theme-button" 
      aria-pressed="false">
      High Contrast
    </button>
    
    <button 
      id="dark-theme" 
      class="theme-button" 
      aria-pressed="false">
      Dark Mode
    </button>
  </div>
</div>

<script>
  document.querySelectorAll('.theme-button').forEach(button => {
    button.addEventListener('click', function() {
      // Update aria-pressed state
      document.querySelectorAll('.theme-button').forEach(btn => {
        btn.setAttribute('aria-pressed', 'false');
      });
      this.setAttribute('aria-pressed', 'true');
      
      // Apply theme
      const themeId = this.id;
      document.body.className = themeId;
      
      // Save preference
      localStorage.setItem('theme-preference', themeId);
    });
  });
  
  // Apply saved preference
  const savedTheme = localStorage.getItem('theme-preference');
  if (savedTheme) {
    document.body.className = savedTheme;
    document.getElementById(savedTheme).setAttribute('aria-pressed', 'true');
  }
</script>

<style>
  /* Default theme */
  body {
    --text-color: #333;
    --background-color: #fff;
    --link-color: #0066cc;
    
    color: var(--text-color);
    background-color: var(--background-color);
  }
  
  a { color: var(--link-color); }
  
  /* High contrast theme */
  body.high-contrast-theme {
    --text-color: #000;
    --background-color: #fff;
    --link-color: #0000CC;
  }
  
  /* Dark theme */
  body.dark-theme {
    --text-color: #eee;
    --background-color: #121212;
    --link-color: #6bb5ff;
  }
</style>
```

## System Preferences

Respect users' system preferences:

```css
/* Respect user's reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.001s !important;
    transition-duration: 0.001s !important;
  }
}

/* Respect user's color scheme preference */
@media (prefers-color-scheme: dark) {
  :root {
    --text-color: #eee;
    --background-color: #121212;
    --link-color: #6bb5ff;
  }
}

@media (prefers-color-scheme: light) {
  :root {
    --text-color: #333;
    --background-color: #fff;
    --link-color: #0066cc;
  }
}
```

## Testing Color and Contrast

1. **Automated tools**: Use contrast checkers to verify ratios
2. **Grayscale test**: View pages in grayscale to check color-independent perception
3. **Color blindness simulators**: Test with tools that simulate different types of color blindness
4. **User testing**: Include people with visual impairments in your testing
5. **System preference test**: Check if your site responds to system preferences