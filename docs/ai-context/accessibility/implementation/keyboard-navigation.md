# Keyboard Navigation Guide

Keyboard accessibility is fundamental to web accessibility. Many users with motor disabilities, visual impairments, or those who prefer keyboard navigation rely on keyboard-only interaction.

## Core Requirements

1. **All interactive elements must be keyboard accessible**
2. **Focus must be visible at all times**
3. **Focus order must be logical and follow visual/content order**
4. **Keyboard traps must be avoided**

## Implementing Keyboard Accessibility

### Interactive Elements

All interactive elements should be:
- Focusable with Tab key
- Activatable with Enter or Space key
- Operated with appropriate keyboard shortcuts when applicable

Native HTML elements generally have good keyboard support:

```html
<!-- These have built-in keyboard support -->
<a href="page.html">Link</a>
<button type="button">Button</button>
<input type="checkbox"> Checkbox
<select>
  <option>Option 1</option>
  <option>Option 2</option>
</select>
```

For custom UI elements, use appropriate semantics:

```html
<!-- Custom button with keyboard support -->
<div 
  role="button" 
  tabindex="0" 
  onclick="handleClick()"
  onkeydown="handleKeyDown(event)">
  Custom Button
</div>

<script>
function handleKeyDown(event) {
  // Trigger on Enter or Space
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    handleClick();
  }
}
</script>
```

### Focus Management

#### Visible Focus

Always ensure focus is visible:

```css
/* Enhance default focus styles */
:focus {
  outline: 2px solid #1976d2;
  outline-offset: 2px;
}

/* If you remove outlines, provide alternatives */
.custom-focus:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.5);
}

/* Never do this without an alternative */
button:focus {
  outline: none; /* BAD - removes focus visibility */
}
```

#### Skip Links

Provide skip navigation links:

```html
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>
  
  <header>
    <!-- Navigation and header content -->
  </header>
  
  <main id="main-content">
    <!-- Main content -->
  </main>
</body>

<style>
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  z-index: 1000;
  padding: 8px;
  background: white;
  transition: top 0.2s;
}

.skip-link:focus {
  top: 0;
}
</style>
```

### Focus Order

Ensure a logical tab order:

```html
<!-- Good: Form follows logical order -->
<form>
  <label for="name">Name</label>
  <input id="name" type="text">
  
  <label for="email">Email</label>
  <input id="email" type="email">
  
  <button type="submit">Submit</button>
</form>

<!-- Bad: Labels after inputs disrupt logical flow -->
<form>
  <input id="name" type="text">
  <label for="name">Name</label>
  
  <input id="email" type="email">
  <label for="email">Email</label>
  
  <button type="submit">Submit</button>
</form>
```

### Managing Focus in SPAs

For single-page applications, manage focus when content changes:

```javascript
// After navigation/content change
function handleRouteChange() {
  // Option 1: Focus the main content
  document.getElementById('main-content').focus();
  
  // Option 2: Focus the heading
  document.querySelector('h1').focus();
  
  // Option 3: Announce with live region
  const announcer = document.getElementById('announcer');
  announcer.textContent = 'Navigated to ' + document.title;
}

// Example live region
<div id="announcer" class="sr-only" aria-live="polite"></div>

<style>
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
</style>
```

### Complex Widgets

For complex widgets like dropdown menus, tabs, and modals:

#### Dropdown Menu

```javascript
// Key mappings for dropdown
const keys = {
  up: function(selectedIndex) {
    return selectedIndex > 0 ? selectedIndex - 1 : 0;
  },
  down: function(selectedIndex, length) {
    return selectedIndex < length - 1 ? selectedIndex + 1 : length - 1;
  },
  home: function() {
    return 0;
  },
  end: function(length) {
    return length - 1;
  },
  escape: function() {
    closeDropdown();
    return -1;
  }
};

// Handle keyboard navigation
function handleKeyDown(event) {
  const options = Array.from(dropdown.querySelectorAll('[role="menuitem"]'));
  const currentIndex = options.indexOf(document.activeElement);
  
  if (Object.keys(keys).includes(event.key.toLowerCase())) {
    event.preventDefault();
    const newIndex = keys[event.key.toLowerCase()](currentIndex, options.length);
    if (newIndex >= 0) {
      options[newIndex].focus();
    }
  }
}
```

## Common Keyboard Navigation Issues

1. **Missing keyboard support for custom controls**
2. **Keyboard traps (user can't tab out of component)**
3. **Focus disappears or jumps to unexpected locations**
4. **No visible focus indicator**
5. **Illogical focus order**
6. **Important functionality only available via mouse**

## Testing Keyboard Navigation

Basic test procedure:
1. Disconnect your mouse
2. Navigate the entire interface using only Tab, Shift+Tab, Enter, Space, Arrow keys
3. Verify all functionality is accessible
4. Verify focus is always visible
5. Verify focus order is logical