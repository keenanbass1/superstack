# Accessible Interactive Elements

Interactive elements like buttons, tabs, modals, and tooltips require special attention to ensure they're accessible to all users.

## Buttons

### Native Buttons

Use native `<button>` elements whenever possible:

```html
<button type="button">Click Me</button>
<button type="submit">Submit Form</button>
<button type="reset">Reset Form</button>
```

Native buttons provide:
- Keyboard accessibility (Enter/Space activation)
- Focus management
- Semantics for assistive technology

### Custom Buttons

If you must create custom buttons, ensure proper accessibility:

```html
<div 
  role="button" 
  tabindex="0" 
  id="custom-button"
  aria-pressed="false" 
  onclick="toggleButton(this)"
  onkeydown="handleButtonKeydown(event, this)">
  Toggle Feature
</div>

<script>
function toggleButton(button) {
  const isPressed = button.getAttribute('aria-pressed') === 'true';
  button.setAttribute('aria-pressed', !isPressed);
  
  // Additional functionality...
}

function handleButtonKeydown(event, button) {
  // Activate on Enter or Space
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault(); // Prevent scrolling on Space
    toggleButton(button);
  }
}
</script>

<style>
[role="button"] {
  display: inline-block;
  padding: 8px 16px;
  cursor: pointer;
  background: #eee;
  border: 1px solid #ccc;
  border-radius: 4px;
  user-select: none; /* Prevent text selection */
}

[role="button"]:hover {
  background: #ddd;
}

[role="button"]:focus {
  outline: 2px solid #1976d2;
  outline-offset: 2px;
}

[role="button"][aria-pressed="true"] {
  background: #1976d2;
  color: white;
}
</style>
```

### Button States

Clearly indicate button states:

```html
<!-- Disabled button -->
<button type="button" disabled>Disabled Button</button>

<!-- Toggle/pressed button -->
<button 
  type="button" 
  aria-pressed="true" 
  class="toggle-button pressed">
  Active Feature
</button>

<!-- Button with loading state -->
<button 
  type="button" 
  aria-busy="true" 
  class="loading-button">
  <span class="spinner" aria-hidden="true"></span>
  <span class="button-text">Loading...</span>
</button>

<style>
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.toggle-button.pressed {
  background-color: #0056b3;
  color: white;
}

.loading-button {
  opacity: 0.8;
  cursor: wait;
}

.spinner {
  display: inline-block;
  width: 1em;
  height: 1em;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
  margin-right: 0.5em;
  vertical-align: middle;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
```

## Tabs

Create accessible tab interfaces:

```html
<div class="tabs-container">
  <!-- Tab List -->
  <div role="tablist" aria-label="Programming Languages">
    <button 
      id="tab-html" 
      role="tab" 
      aria-selected="true" 
      aria-controls="panel-html">
      HTML
    </button>
    <button 
      id="tab-css" 
      role="tab" 
      aria-selected="false" 
      aria-controls="panel-css"
      tabindex="-1">
      CSS
    </button>
    <button 
      id="tab-js" 
      role="tab" 
      aria-selected="false" 
      aria-controls="panel-js"
      tabindex="-1">
      JavaScript
    </button>
  </div>
  
  <!-- Tab Panels -->
  <div 
    id="panel-html" 
    role="tabpanel" 
    aria-labelledby="tab-html"
    tabindex="0">
    <h3>HTML Content</h3>
    <p>HTML is the standard markup language for creating web pages.</p>
  </div>
  
  <div 
    id="panel-css" 
    role="tabpanel" 
    aria-labelledby="tab-css"
    tabindex="0"
    hidden>
    <h3>CSS Content</h3>
    <p>CSS is the language used to style web pages.</p>
  </div>
  
  <div 
    id="panel-js" 
    role="tabpanel" 
    aria-labelledby="tab-js"
    tabindex="0"
    hidden>
    <h3>JavaScript Content</h3>
    <p>JavaScript is the programming language of the web.</p>
  </div>
</div>

<script>
  const tabs = document.querySelectorAll('[role="tab"]');
  const tabPanels = document.querySelectorAll('[role="tabpanel"]');
  
  // Add click handlers
  tabs.forEach(tab => {
    tab.addEventListener('click', () => activateTab(tab));
  });
  
  // Add keyboard navigation
  tabs.forEach(tab => {
    tab.addEventListener('keydown', e => {
      const tabsList = Array.from(tabs);
      const currentIndex = tabsList.indexOf(document.activeElement);
      
      // Handle arrow keys
      switch (e.key) {
        case 'ArrowRight':
          e.preventDefault();
          const nextTab = tabsList[(currentIndex + 1) % tabsList.length];
          nextTab.focus();
          activateTab(nextTab);
          break;
        case 'ArrowLeft':
          e.preventDefault();
          const prevIndex = (currentIndex - 1 + tabsList.length) % tabsList.length;
          const prevTab = tabsList[prevIndex];
          prevTab.focus();
          activateTab(prevTab);
          break;
        case 'Home':
          e.preventDefault();
          const firstTab = tabsList[0];
          firstTab.focus();
          activateTab(firstTab);
          break;
        case 'End':
          e.preventDefault();
          const lastTab = tabsList[tabsList.length - 1];
          lastTab.focus();
          activateTab(lastTab);
          break;
      }
    });
  });
  
  function activateTab(tab) {
    // Deactivate all tabs
    tabs.forEach(t => {
      t.setAttribute('aria-selected', 'false');
      t.setAttribute('tabindex', '-1');
    });
    
    // Hide all tab panels
    tabPanels.forEach(panel => {
      panel.hidden = true;
    });
    
    // Activate clicked tab
    tab.setAttribute('aria-selected', 'true');
    tab.removeAttribute('tabindex');
    
    // Show corresponding panel
    const panelId = tab.getAttribute('aria-controls');
    const panel = document.getElementById(panelId);
    panel.hidden = false;
  }
</script>
```

## Modals/Dialogs

Create accessible modal dialogs:

```html
<button 
  type="button" 
  onclick="openModal()"
  aria-haspopup="dialog">
  Open Modal
</button>

<div 
  id="modal" 
  role="dialog" 
  aria-labelledby="modal-title" 
  aria-describedby="modal-desc" 
  aria-modal="true"
  class="modal"
  hidden>
  
  <div class="modal-content">
    <div class="modal-header">
      <h2 id="modal-title">Modal Title</h2>
      <button 
        type="button" 
        class="close-button" 
        aria-label="Close"
        onclick="closeModal()">
        &times;
      </button>
    </div>
    
    <div class="modal-body">
      <p id="modal-desc">This is modal content that explains the purpose of this dialog.</p>
      <input type="text" aria-label="Sample input">
      <button type="button">Example Button</button>
    </div>
    
    <div class="modal-footer">
      <button type="button" onclick="closeModal()">Cancel</button>
      <button type="button" onclick="submitModal()">Confirm</button>
    </div>
  </div>
</div>

<script>
  const modal = document.getElementById('modal');
  let previouslyFocusedElement;
  
  function openModal() {
    // Store the element that had focus
    previouslyFocusedElement = document.activeElement;
    
    // Show the modal
    modal.hidden = false;
    
    // Set focus to first focusable element
    const focusableElements = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    if (focusableElements.length > 0) {
      focusableElements[0].focus();
    }
    
    // Add event listeners for keyboard handling
    document.addEventListener('keydown', handleModalKeydown);
    
    // Disable scrolling on the background
    document.body.style.overflow = 'hidden';
  }
  
  function closeModal() {
    // Hide the modal
    modal.hidden = true;
    
    // Restore focus to previous element
    if (previouslyFocusedElement) {
      previouslyFocusedElement.focus();
    }
    
    // Remove event listeners
    document.removeEventListener('keydown', handleModalKeydown);
    
    // Re-enable scrolling
    document.body.style.overflow = '';
  }
  
  function handleModalKeydown(event) {
    // Close on Escape
    if (event.key === 'Escape') {
      closeModal();
      return;
    }
    
    // Trap focus within modal
    if (event.key === 'Tab') {
      const focusableElements = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
      const firstElement = focusableElements[0];
      const lastElement = focusableElements[focusableElements.length - 1];
      
      // Shift+Tab on first element should go to last element
      if (event.shiftKey && document.activeElement === firstElement) {
        event.preventDefault();
        lastElement.focus();
      }
      // Tab on last element should go to first element
      else if (!event.shiftKey && document.activeElement === lastElement) {
        event.preventDefault();
        firstElement.focus();
      }
    }
  }
  
  function submitModal() {
    // Handle form submission or action
    console.log('Modal confirmed');
    closeModal();
  }
</script>

<style>
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    background-color: white;
    border-radius: 4px;
    max-width: 500px;
    width: 100%;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
  }
  
  .close-button {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    padding: 0;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
  }
  
  .close-button:hover {
    background-color: #eee;
  }
  
  .modal-body {
    margin-bottom: 20px;
  }
  
  .modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
  }
</style>
```

## Dropdown Menus

Create accessible dropdown menus:

```html
<div class="dropdown">
  <button 
    id="dropdown-button" 
    aria-haspopup="true" 
    aria-expanded="false"
    aria-controls="dropdown-menu"
    onclick="toggleDropdown()">
    Options
    <span aria-hidden="true">▼</span>
  </button>
  
  <ul 
    id="dropdown-menu" 
    role="menu" 
    aria-labelledby="dropdown-button"
    hidden>
    <li role="none">
      <a 
        href="#option1" 
        role="menuitem"
        tabindex="-1">
        Option 1
      </a>
    </li>
    <li role="none">
      <a 
        href="#option2" 
        role="menuitem"
        tabindex="-1">
        Option 2
      </a>
    </li>
    <li role="none">
      <a 
        href="#option3" 
        role="menuitem"
        tabindex="-1">
        Option 3
      </a>
    </li>
  </ul>
</div>

<script>
  const dropdownButton = document.getElementById('dropdown-button');
  const dropdownMenu = document.getElementById('dropdown-menu');
  const menuItems = dropdownMenu.querySelectorAll('[role="menuitem"]');
  
  function toggleDropdown() {
    const isExpanded = dropdownButton.getAttribute('aria-expanded') === 'true';
    
    if (isExpanded) {
      closeDropdown();
    } else {
      openDropdown();
    }
  }
  
  function openDropdown() {
    dropdownButton.setAttribute('aria-expanded', 'true');
    dropdownMenu.hidden = false;
    
    // Set tabindex for first item
    if (menuItems.length > 0) {
      menuItems[0].setAttribute('tabindex', '0');
      menuItems[0].focus();
    }
    
    // Add event listeners
    document.addEventListener('click', handleOutsideClick);
    dropdownMenu.addEventListener('keydown', handleMenuKeydown);
  }
  
  function closeDropdown() {
    dropdownButton.setAttribute('aria-expanded', 'false');
    dropdownMenu.hidden = true;
    
    // Reset tabindex
    menuItems.forEach(item => {
      item.setAttribute('tabindex', '-1');
    });
    
    // Remove event listeners
    document.removeEventListener('click', handleOutsideClick);
    dropdownMenu.removeEventListener('keydown', handleMenuKeydown);
  }
  
  function handleOutsideClick(event) {
    if (!dropdownButton.contains(event.target) && !dropdownMenu.contains(event.target)) {
      closeDropdown();
    }
  }
  
  function handleMenuKeydown(event) {
    const currentItem = document.activeElement;
    const currentIndex = Array.from(menuItems).indexOf(currentItem);
    
    switch (event.key) {
      case 'Escape':
        event.preventDefault();
        closeDropdown();
        dropdownButton.focus();
        break;
        
      case 'ArrowDown':
        event.preventDefault();
        if (currentIndex < menuItems.length - 1) {
          focusMenuItem(currentIndex + 1);
        }
        break;
        
      case 'ArrowUp':
        event.preventDefault();
        if (currentIndex > 0) {
          focusMenuItem(currentIndex - 1);
        } else {
          closeDropdown();
          dropdownButton.focus();
        }
        break;
        
      case 'Home':
        event.preventDefault();
        if (menuItems.length > 0) {
          focusMenuItem(0);
        }
        break;
        
      case 'End':
        event.preventDefault();
        if (menuItems.length > 0) {
          focusMenuItem(menuItems.length - 1);
        }
        break;
    }
  }
  
  function focusMenuItem(index) {
    // Update tabindex
    menuItems.forEach(item => {
      item.setAttribute('tabindex', '-1');
    });
    
    menuItems[index].setAttribute('tabindex', '0');
    menuItems[index].focus();
  }
  
  // Close dropdown when menu item is clicked
  menuItems.forEach(item => {
    item.addEventListener('click', () => {
      closeDropdown();
      dropdownButton.focus();
    });
  });
</script>

<style>
  .dropdown {
    position: relative;
    display: inline-block;
  }
  
  #dropdown-menu {
    position: absolute;
    background-color: white;
    min-width: 160px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    border-radius: 4px;
    padding: 8px 0;
    margin-top: 4px;
    list-style: none;
    z-index: 10;
  }
  
  #dropdown-menu [role="menuitem"] {
    display: block;
    padding: 8px 16px;
    text-decoration: none;
    color: #333;
  }
  
  #dropdown-menu [role="menuitem"]:hover,
  #dropdown-menu [role="menuitem"]:focus {
    background-color: #f5f5f5;
    outline: none;
  }
  
  #dropdown-menu [role="menuitem"]:focus-visible {
    outline: 2px solid #1976d2;
    outline-offset: -2px;
  }
</style>
```

## Tooltips

Create accessible tooltips:

```html
<button 
  aria-describedby="tooltip1" 
  class="tooltip-trigger">
  Help
  <span class="icon" aria-hidden="true">?</span>
</button>

<div 
  id="tooltip1" 
  role="tooltip" 
  class="tooltip"
  hidden>
  This is helpful information that explains the feature.
</div>

<script>
  const triggers = document.querySelectorAll('.tooltip-trigger');
  
  triggers.forEach(trigger => {
    const tooltipId = trigger.getAttribute('aria-describedby');
    const tooltip = document.getElementById(tooltipId);
    
    // Show tooltip on hover/focus
    function showTooltip() {
      tooltip.hidden = false;
      
      // Position tooltip
      const triggerRect = trigger.getBoundingClientRect();
      tooltip.style.top = `${triggerRect.bottom + 10}px`;
      tooltip.style.left = `${triggerRect.left + (triggerRect.width / 2) - (tooltip.offsetWidth / 2)}px`;
    }
    
    // Hide tooltip
    function hideTooltip() {
      tooltip.hidden = true;
    }
    
    // Event listeners
    trigger.addEventListener('mouseenter', showTooltip);
    trigger.addEventListener('mouseleave', hideTooltip);
    trigger.addEventListener('focus', showTooltip);
    trigger.addEventListener('blur', hideTooltip);
    
    // Close on Escape
    trigger.addEventListener('keydown', event => {
      if (event.key === 'Escape' && !tooltip.hidden) {
        hideTooltip();
      }
    });
  });
</script>

<style>
  .tooltip-trigger {
    position: relative;
  }
  
  .tooltip {
    position: absolute;
    background-color: #333;
    color: white;
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 14px;
    z-index: 100;
    max-width: 250px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  }
  
  .tooltip::before {
    content: '';
    position: absolute;
    top: -6px;
    left: 50%;
    transform: translateX(-50%);
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-bottom: 6px solid #333;
  }
</style>
```

## Accordions

Create accessible accordions:

```html
<div class="accordion">
  <h3>
    <button
      aria-expanded="false"
      class="accordion-trigger"
      aria-controls="section1-content"
      id="section1-header">
      <span class="accordion-title">Section 1</span>
      <span class="accordion-icon" aria-hidden="true"></span>
    </button>
  </h3>
  <div
    id="section1-content"
    role="region"
    aria-labelledby="section1-header"
    class="accordion-content"
    hidden>
    <p>Content for section 1 goes here.</p>
  </div>
  
  <h3>
    <button
      aria-expanded="false"
      class="accordion-trigger"
      aria-controls="section2-content"
      id="section2-header">
      <span class="accordion-title">Section 2</span>
      <span class="accordion-icon" aria-hidden="true"></span>
    </button>
  </h3>
  <div
    id="section2-content"
    role="region"
    aria-labelledby="section2-header"
    class="accordion-content"
    hidden>
    <p>Content for section 2 goes here.</p>
  </div>
</div>

<script>
  const accordionTriggers = document.querySelectorAll('.accordion-trigger');
  
  accordionTriggers.forEach(trigger => {
    trigger.addEventListener('click', () => {
      const isExpanded = trigger.getAttribute('aria-expanded') === 'true';
      trigger.setAttribute('aria-expanded', !isExpanded);
      
      const contentId = trigger.getAttribute('aria-controls');
      const content = document.getElementById(contentId);
      content.hidden = isExpanded;
    });
  });
</script>

<style>
  .accordion {
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-bottom: 20px;
  }
  
  .accordion-trigger {
    width: 100%;
    padding: 15px;
    text-align: left;
    background: none;
    border: none;
    border-bottom: 1px solid #ddd;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
  }
  
  .accordion-trigger:hover {
    background-color: #f5f5f5;
  }
  
  .accordion-trigger:focus {
    outline: 2px solid #1976d2;
    outline-offset: -2px;
  }
  
  .accordion-icon {
    width: 10px;
    height: 10px;
    border-right: 2px solid currentColor;
    border-bottom: 2px solid currentColor;
    transform: rotate(45deg);
    transition: transform 0.2s ease;
  }
  
  .accordion-trigger[aria-expanded="true"] .accordion-icon {
    transform: rotate(-135deg);
  }
  
  .accordion-content {
    padding: 15px;
  }
</style>
```

## Common Interactive Element Issues

1. **Non-semantic elements**: Using `<div>` or `<span>` without proper roles/attributes
2. **Keyboard inaccessibility**: Elements that can't be operated with keyboard
3. **Missing focus states**: No visible indication of keyboard focus
4. **Improper ARIA usage**: Incorrect roles or missing required attributes
5. **Focus management**: Not managing focus properly in complex widgets
6. **State indication**: Not clearly indicating current state (selected, expanded, etc.)
7. **Touch targets**: Too small or too close together for mobile users

## Testing Interactive Elements

1. **Keyboard testing**: Verify all functionality works with keyboard only
2. **Screen reader testing**: Test with popular screen readers (NVDA, VoiceOver, JAWS)
3. **Focus testing**: Verify focus is visible and follows a logical order
4. **State testing**: Verify states are properly announced by screen readers
5. **Touch testing**: Verify widgets work on touch devices
6. **Zoom testing**: Test at 200% zoom to ensure usability