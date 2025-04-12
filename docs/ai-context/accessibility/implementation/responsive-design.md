# Accessibility in Responsive Design

Responsive design and accessibility work together to ensure content is usable by everyone across all devices and screen sizes.

## Core Principles

### 1. Design Responsively from the Start

Always begin with a responsive approach:

```css
/* Base responsive setup */
* {
  box-sizing: border-box;
}

html {
  font-size: 100%; /* Base for rem units */
}

body {
  margin: 0;
  padding: 0;
  width: 100%;
  overflow-x: hidden; /* Prevent horizontal scrolling */
}

img, video, canvas, svg {
  max-width: 100%;
  height: auto;
}
```

### 2. Use Responsive Units

Prefer relative units over absolute ones:

```css
/* Prefer these responsive units */
.container {
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.text {
  font-size: 1rem;
  line-height: 1.5;
  margin-bottom: 1.5em;
}

/* Avoid fixed units like these for layout */
.avoid-fixed {
  width: 960px; /* Not responsive */
  padding: 20px; /* Not responsive */
  margin-left: 250px; /* Not responsive */
}
```

### 3. Mobile-First Approach

Start with styles for small screens, then enhance for larger ones:

```css
/* Base styles for all devices */
.card {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 1rem;
}

/* Enhance for larger screens */
@media (min-width: 768px) {
  .card {
    padding: 2rem;
    margin-bottom: 2rem;
  }
}

.card-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 768px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
  }
}

@media (min-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

## Responsive Layout Techniques

### Flexible Grids

Use CSS Grid or Flexbox for responsive layouts:

```css
/* CSS Grid example */
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

/* Flexbox example */
.flex-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.flex-item {
  flex: 1 1 300px; /* grow, shrink, basis */
  min-width: 0; /* Prevent overflow */
}
```

### Responsive Typography

Use fluid typography for better readability:

```css
/* Base font size */
html {
  font-size: 16px;
}

/* Simple responsive approach */
h1 { font-size: 2rem; }
h2 { font-size: 1.5rem; }
h3 { font-size: 1.25rem; }

@media (min-width: 768px) {
  h1 { font-size: 2.5rem; }
  h2 { font-size: 2rem; }
  h3 { font-size: 1.5rem; }
}

/* Fluid typography with clamp */
h1 {
  /* min, preferred, max */
  font-size: clamp(1.75rem, 5vw, 2.5rem);
}

p {
  font-size: clamp(1rem, 1.5vw, 1.25rem);
  line-height: 1.5;
  max-width: 70ch; /* Optimal reading length */
}
```

### Responsive Navigation

Create accessible navigation patterns:

```html
<!-- Responsive navigation -->
<nav class="main-nav">
  <button 
    class="menu-toggle" 
    aria-expanded="false"
    aria-controls="main-menu"
    hidden>
    <span class="icon" aria-hidden="true"></span>
    <span class="text">Menu</span>
  </button>
  
  <ul id="main-menu" class="menu">
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
    <li><a href="/services">Services</a></li>
    <li><a href="/contact">Contact</a></li>
  </ul>
</nav>

<style>
.main-nav {
  position: relative;
}

/* Desktop menu */
@media (min-width: 768px) {
  .menu-toggle {
    display: none;
  }
  
  .menu {
    display: flex;
    list-style: none;
    gap: 1.5rem;
    padding: 0;
  }
}

/* Mobile menu */
@media (max-width: 767px) {
  .menu-toggle {
    display: flex;
    align-items: center;
    background: none;
    border: 1px solid #ddd;
    padding: 0.5rem 1rem;
    border-radius: 4px;
  }
  
  .menu {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    list-style: none;
    padding: 0;
    margin: 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  
  .menu[data-visible="true"] {
    display: block;
  }
  
  .menu a {
    display: block;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #eee;
  }
}
</style>

<script>
  const menuToggle = document.querySelector('.menu-toggle');
  const menu = document.getElementById('main-menu');
  
  // Show button only if JavaScript is available
  menuToggle.hidden = false;
  
  // Toggle menu visibility
  menuToggle.addEventListener('click', () => {
    const expanded = menuToggle.getAttribute('aria-expanded') === 'true';
    menuToggle.setAttribute('aria-expanded', !expanded);
    menu.dataset.visible = !expanded;
  });
  
  // Close menu when clicking outside
  document.addEventListener('click', (event) => {
    if (!menu.contains(event.target) && !menuToggle.contains(event.target)) {
      if (menu.dataset.visible === 'true') {
        menuToggle.setAttribute('aria-expanded', 'false');
        menu.dataset.visible = false;
      }
    }
  });
</script>
```

## Responsive Images

### Basic Responsive Images

Use modern HTML for responsive images:

```html
<!-- Simple responsive image -->
<img 
  src="image.jpg" 
  alt="Description of image" 
  style="max-width: 100%; height: auto;">

<!-- Responsive image with multiple sources -->
<picture>
  <!-- Small screens: crop to focus on the subject -->
  <source 
    media="(max-width: 600px)" 
    srcset="image-mobile.jpg">
  
  <!-- Medium screens: show full image -->
  <source 
    media="(max-width: 1024px)" 
    srcset="image-tablet.jpg">
  
  <!-- Default/desktop image -->
  <img 
    src="image-desktop.jpg" 
    alt="Description of image"
    width="1200"
    height="800">
</picture>

<!-- Resolution switching -->
<img 
  src="image-400.jpg"
  srcset="image-400.jpg 400w,
          image-800.jpg 800w,
          image-1200.jpg 1200w"
  sizes="(max-width: 600px) 100vw,
         (max-width: 1024px) 50vw,
         33vw"
  alt="Description of image"
  width="1200"
  height="800">
```

### Responsive Background Images

Use media queries for responsive background images:

```css
.hero {
  /* Base/mobile background */
  background-image: url('hero-mobile.jpg');
  background-size: cover;
  background-position: center;
  min-height: 50vh;
  padding: 2rem;
}

@media (min-width: 768px) {
  .hero {
    background-image: url('hero-tablet.jpg');
    min-height: 60vh;
  }
}

@media (min-width: 1200px) {
  .hero {
    background-image: url('hero-desktop.jpg');
    min-height: 70vh;
  }
}
```

## Responsive Tables

Tables can be particularly challenging for responsive design. Here are some accessible approaches:

### 1. Horizontal Scrolling

Allow horizontal scrolling for complex tables:

```html
<div class="table-container">
  <table>
    <caption>Quarterly Sales Data</caption>
    <thead>
      <tr>
        <th scope="col">Product</th>
        <th scope="col">Q1 Sales</th>
        <th scope="col">Q2 Sales</th>
        <th scope="col">Q3 Sales</th>
        <th scope="col">Q4 Sales</th>
        <th scope="col">Total</th>
      </tr>
    </thead>
    <tbody>
      <!-- Table data rows -->
    </tbody>
  </table>
</div>

<style>
.table-container {
  width: 100%;
  overflow-x: auto;
  /* Indicate scrollability */
  background-image: linear-gradient(to right, white, white),
                    linear-gradient(to right, white, white),
                    linear-gradient(to right, rgba(0,0,0,0.1), rgba(255,255,255,0)),
                    linear-gradient(to left, rgba(0,0,0,0.1), rgba(255,255,255,0));
  background-position: left center, right center, left center, right center;
  background-repeat: no-repeat;
  background-size: 20px 100%, 20px 100%, 10px 100%, 10px 100%;
  background-attachment: local, local, scroll, scroll;
}

table {
  min-width: 600px;
  border-collapse: collapse;
}

th, td {
  padding: 0.75rem;
  border: 1px solid #ddd;
  text-align: left;
}

caption {
  margin-bottom: 0.5rem;
  font-weight: bold;
}
</style>
```

### 2. Responsive Card Layout

Transform tables to cards on mobile:

```html
<table class="responsive-table">
  <caption>Employee Information</caption>
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Title</th>
      <th scope="col">Department</th>
      <th scope="col">Location</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Name">Jane Smith</td>
      <td data-label="Title">Developer</td>
      <td data-label="Department">Engineering</td>
      <td data-label="Location">New York</td>
    </tr>
    <!-- More rows -->
  </tbody>
</table>

<style>
.responsive-table {
  width: 100%;
  border-collapse: collapse;
}

.responsive-table th, 
.responsive-table td {
  padding: 0.75rem;
  border: 1px solid #ddd;
  text-align: left;
}

@media (max-width: 767px) {
  .responsive-table thead {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    border: 0;
  }
  
  .responsive-table tr {
    display: block;
    margin-bottom: 1.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }
  
  .responsive-table td {
    display: block;
    text-align: right;
    border: none;
    border-bottom: 1px solid #eee;
  }
  
  .responsive-table td:last-child {
    border-bottom: none;
  }
  
  .responsive-table td::before {
    content: attr(data-label);
    float: left;
    font-weight: bold;
  }
}
</style>
```

## Responsive Forms

Create forms that work well across all devices:

```html
<form class="responsive-form">
  <div class="form-header">
    <h2>Contact Us</h2>
    <p>Fields marked with <span aria-label="required">*</span> are required.</p>
  </div>
  
  <div class="form-row">
    <div class="form-group">
      <label for="name">Name <span aria-label="required">*</span></label>
      <input type="text" id="name" required>
    </div>
    
    <div class="form-group">
      <label for="email">Email <span aria-label="required">*</span></label>
      <input type="email" id="email" required>
    </div>
  </div>
  
  <div class="form-group">
    <label for="subject">Subject</label>
    <input type="text" id="subject">
  </div>
  
  <div class="form-group">
    <label for="message">Message <span aria-label="required">*</span></label>
    <textarea id="message" rows="5" required></textarea>
  </div>
  
  <div class="form-actions">
    <button type="reset" class="secondary-button">Clear Form</button>
    <button type="submit" class="primary-button">Submit</button>
  </div>
</form>

<style>
.responsive-form {
  width: 100%;
  max-width: 800px;
  padding: 1.5rem;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  flex: 1;
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input, textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

button {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

.primary-button {
  background-color: #0056b3;
  color: white;
  border: none;
}

.secondary-button {
  background-color: transparent;
  border: 1px solid #ddd;
}

/* Responsive adjustments */
@media (max-width: 767px) {
  .form-row {
    flex-direction: column;
    gap: 0;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  button {
    width: 100%;
  }
}
</style>
```

## Testing Responsive Accessibility

### Viewport Testing

Test your designs at various viewport sizes:

1. **Small mobile**: 320px-375px width
2. **Large mobile**: 376px-767px width
3. **Tablets**: 768px-1023px width
4. **Desktop**: 1024px+ width

### Zoom Testing

Test your website with different zoom levels:

1. **100%**: Normal view
2. **200%**: WCAG AA requirement
3. **400%**: WCAG AAA requirement

### Device Testing

Test on actual devices when possible:

1. **iOS devices** with VoiceOver
2. **Android devices** with TalkBack
3. **Touch-only devices** for touch accessibility

### Assistive Technology Testing

Test with screen readers in responsive modes:

1. **VoiceOver** on iOS/macOS
2. **NVDA/JAWS** on Windows
3. **TalkBack** on Android

## Common Responsive Accessibility Issues

### 1. Hidden Content

Be careful with hiding content in responsive layouts:

```css
/* Bad - hides content from screen readers */
.mobile-hidden {
  display: none;
}

/* Good - visually hidden but accessible to screen readers */
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Good - responsive hiding */
@media (max-width: 767px) {
  .hide-on-mobile {
    display: none;
  }
}
```

### 2. Touch Target Size

Ensure touch targets are large enough:

```css
/* Minimum touch target size */
button, 
a,
input[type="checkbox"],
input[type="radio"],
input[type="submit"] {
  min-width: 44px;
  min-height: 44px;
}

/* For inline links in text */
p a {
  padding: 0.125em; /* Increase touch area without breaking text flow */
}

/* For icon buttons */
.icon-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
}
```

### 3. Maintaining Context on Resize

Ensure users don't lose context when resizing:

```css
/* Keep related content together */
.form-field {
  margin-bottom: 1.5rem; /* Space between fields */
}

.form-field label,
.form-field input,
.form-field .error-message {
  display: block; /* Keep label, input, and error together */
  max-width: 100%; /* Prevent overflow */
}

/* Maintain focus when resizing */
*:focus {
  outline: 2px solid #1976d2;
  outline-offset: 2px;
}
```

## Best Practices Summary

1. **Start with mobile design** and progressively enhance for larger screens
2. **Use relative units** (%, rem, em, vh, vw) instead of fixed ones (px)
3. **Test at different viewport widths** and zoom levels
4. **Ensure adequate touch target size** (minimum 44×44px)
5. **Maintain visible focus** across all screen sizes
6. **Preserve content hierarchy** in responsive layouts
7. **Provide alternative layouts** for complex content like tables
8. **Define responsive breakpoints** based on content needs, not specific devices
9. **Test with assistive technologies** at different screen sizes
10. **Implement proper semantic HTML** that works at all sizes