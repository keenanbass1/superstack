# ARIA Implementation Guide

ARIA (Accessible Rich Internet Applications) provides attributes to enhance accessibility when HTML alone isn't sufficient. This guide covers proper ARIA usage patterns.

## The First Rule of ARIA

> **Don't use ARIA if native HTML can do the job.**

Using semantic HTML elements is always preferable to adding ARIA to non-semantic elements.

**Good (Preferred):**
```html
<button type="button">Submit</button>
```

**Acceptable (but unnecessary):**
```html
<div role="button" tabindex="0">Submit</div>
```

## Essential ARIA Concepts

### Roles

Roles define what an element is or does:

```html
<div role="navigation">
  <!-- Navigation content -->
</div>
```

Common roles:
- `button`, `link`, `checkbox`, `radiogroup`, `tab`, `tabpanel`
- `navigation`, `main`, `search`, `form`
- `dialog`, `alertdialog`, `alert`
- `grid`, `listbox`, `menu`, `menuitem`

### Properties

Properties describe characteristics of elements:

```html
<button aria-haspopup="true" aria-controls="menu1">Options</button>
```

Common properties:
- `aria-label`, `aria-labelledby`, `aria-describedby`
- `aria-required`, `aria-readonly`, `aria-disabled`
- `aria-expanded`, `aria-haspopup`, `aria-controls`
- `aria-hidden`, `aria-live`, `aria-atomic`

### States

States describe the current condition of elements:

```html
<button aria-pressed="true">Like</button>
```

Common states:
- `aria-checked`, `aria-selected`, `aria-pressed`
- `aria-expanded`, `aria-busy`, `aria-invalid`

## ARIA Design Patterns

### Buttons

```html
<!-- Toggle button -->
<button aria-pressed="false" onclick="togglePressed(this)">
  Dark Mode
</button>
```

### Accordions

```html
<div class="accordion">
  <h3>
    <button aria-expanded="false" aria-controls="section1">
      Section 1
    </button>
  </h3>
  <div id="section1" hidden>
    <p>Content for section 1</p>
  </div>
</div>
```

### Modals

```html
<div id="modal1" role="dialog" aria-labelledby="modalTitle" aria-modal="true" hidden>
  <h2 id="modalTitle">Modal Title</h2>
  <div>Modal content here</div>
  <button onclick="closeModal()">Close</button>
</div>
```

### Tabs

```html
<div class="tabs">
  <div role="tablist" aria-label="Programming Languages">
    <button id="tab1" role="tab" aria-selected="true" aria-controls="panel1">HTML</button>
    <button id="tab2" role="tab" aria-selected="false" aria-controls="panel2">CSS</button>
    <button id="tab3" role="tab" aria-selected="false" aria-controls="panel3">JavaScript</button>
  </div>
  
  <div id="panel1" role="tabpanel" aria-labelledby="tab1">
    <p>HTML content here</p>
  </div>
  <div id="panel2" role="tabpanel" aria-labelledby="tab2" hidden>
    <p>CSS content here</p>
  </div>
  <div id="panel3" role="tabpanel" aria-labelledby="tab3" hidden>
    <p>JavaScript content here</p>
  </div>
</div>
```

## Common ARIA Mistakes

1. **Adding ARIA without behavior**
   ```html
   <!-- Bad: role without behavior -->
   <div role="button">Click me</div>
   
   <!-- Good: role with behavior -->
   <div role="button" tabindex="0" onclick="handleClick()" onkeydown="handleKeydown()">
     Click me
   </div>
   ```

2. **Incorrect role usage**
   ```html
   <!-- Bad: menu role for site navigation -->
   <nav role="menu">
     <!-- Navigation items -->
   </nav>
   
   <!-- Good: menu role is for application menus, not site navigation -->
   <nav>
     <!-- Navigation items -->
   </nav>
   ```

3. **Hiding visible content from screen readers**
   ```html
   <!-- Bad: hides content that's visually present -->
   <p aria-hidden="true">Important information</p>
   
   <!-- Good: aria-hidden only for decorative or redundant content -->
   <span class="icon" aria-hidden="true"></span> Settings
   ```