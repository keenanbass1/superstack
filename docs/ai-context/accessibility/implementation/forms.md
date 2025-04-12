# Accessible Form Patterns

Forms are essential for user interaction but can present significant accessibility barriers if not implemented properly.

## Core Form Accessibility Requirements

1. **All inputs must have associated labels**
2. **Error messages must be clear and programmatically associated with inputs**
3. **Required fields must be clearly indicated**
4. **Form controls must be keyboard accessible**
5. **Instructions must be provided where needed**

## Labeling Inputs

### Explicit Labels (Preferred Method)

```html
<label for="username">Username</label>
<input id="username" type="text">
```

### ARIA Labeling (When Visible Labels Can't Be Used)

```html
<!-- Using aria-label -->
<input type="search" aria-label="Search the website">

<!-- Using aria-labelledby -->
<span id="search-label">Search</span>
<input type="search" aria-labelledby="search-label">
```

### Placeholder is Not a Label

```html
<!-- Bad: Placeholder instead of label -->
<input type="email" placeholder="Email Address">

<!-- Good: Label with optional placeholder -->
<label for="email">Email Address</label>
<input id="email" type="email" placeholder="example@domain.com">
```

## Error Handling

### Error Messages

Associate error messages with form controls:

```html
<label for="password">Password</label>
<input 
  id="password" 
  type="password" 
  aria-describedby="password-error"
  aria-invalid="true">
<div id="password-error" class="error">
  Password must be at least 8 characters
</div>
```

### Form-Level Errors

For errors at the form level:

```html
<form aria-describedby="form-errors">
  <div id="form-errors" role="alert" class="error-summary">
    <h2>There were problems with your submission</h2>
    <ul>
      <li><a href="#name">Name is required</a></li>
      <li><a href="#email">Email is not valid</a></li>
    </ul>
  </div>
  
  <!-- Form fields -->
</form>
```

### Live Validation

For instant validation feedback:

```html
<label for="username">Username</label>
<input 
  id="username" 
  type="text" 
  aria-describedby="username-validation" 
  required>
<div id="username-validation" aria-live="polite"></div>

<script>
document.getElementById('username').addEventListener('input', function() {
  const validation = document.getElementById('username-validation');
  if (this.value === '') {
    validation.textContent = 'Username is required';
    this.setAttribute('aria-invalid', 'true');
  } else if (this.value.length < 5) {
    validation.textContent = 'Username must be at least 5 characters';
    this.setAttribute('aria-invalid', 'true');
  } else {
    validation.textContent = 'Username is valid';
    this.removeAttribute('aria-invalid');
  }
});
</script>
```

## Required Fields

### Indicating Required Fields

```html
<!-- Option 1: Text in label -->
<label for="name">Name (required)</label>
<input id="name" type="text" required>

<!-- Option 2: Symbol with accessible text -->
<label for="email">
  Email <span aria-label="required">*</span>
</label>
<input id="email" type="email" required>

<!-- Option 3: ARIA -->
<label for="phone">Phone</label>
<input id="phone" type="tel" aria-required="true">
```

Always explain your required field indicator:

```html
<form>
  <p>Fields marked with <span aria-label="required">*</span> are required.</p>
  <!-- Form fields -->
</form>
```

## Input Types and Attributes

Use appropriate input types:

```html
<input type="email"> <!-- Email validation -->
<input type="tel"> <!-- Phone keyboard on mobile -->
<input type="number"> <!-- Numeric keyboard -->
<input type="date"> <!-- Date picker -->
<input type="url"> <!-- URL validation -->
```

Use appropriate attributes:

```html
<input type="text" autocomplete="name"> <!-- Helps autofill -->
<input type="text" inputmode="numeric" pattern="[0-9]*"> <!-- Numeric entry -->
<input type="text" spellcheck="true"> <!-- Spelling check -->
```

## Grouping Controls

### Fieldsets

Group related controls with fieldset and legend:

```html
<fieldset>
  <legend>Shipping Address</legend>
  
  <div>
    <label for="street">Street</label>
    <input id="street" type="text">
  </div>
  
  <div>
    <label for="city">City</label>
    <input id="city" type="text">
  </div>
  
  <!-- More address fields -->
</fieldset>
```

### Radio Button Groups

```html
<fieldset>
  <legend>Subscription Type</legend>
  
  <div>
    <input type="radio" name="subscription" id="basic" value="basic">
    <label for="basic">Basic</label>
  </div>
  
  <div>
    <input type="radio" name="subscription" id="premium" value="premium">
    <label for="premium">Premium</label>
  </div>
  
  <div>
    <input type="radio" name="subscription" id="enterprise" value="enterprise">
    <label for="enterprise">Enterprise</label>
  </div>
</fieldset>
```

## Custom Form Components

### Custom Select/Dropdown

```html
<div class="custom-select">
  <label id="country-label">Country</label>
  
  <button 
    aria-haspopup="listbox" 
    aria-labelledby="country-label selected-country" 
    id="country-button">
    <span id="selected-country">Select a country</span>
    <span class="icon" aria-hidden="true">▼</span>
  </button>
  
  <ul 
    id="country-listbox" 
    role="listbox" 
    aria-labelledby="country-label"
    hidden>
    <li id="country-1" role="option">United States</li>
    <li id="country-2" role="option">Canada</li>
    <li id="country-3" role="option">Mexico</li>
  </ul>
</div>

<script>
  // Toggle dropdown
  document.getElementById('country-button').addEventListener('click', function() {
    const listbox = document.getElementById('country-listbox');
    const expanded = listbox.hidden === false;
    
    listbox.hidden = expanded;
    this.setAttribute('aria-expanded', !expanded);
    
    if (!expanded) {
      // Focus first option when opening
      document.getElementById('country-1').focus();
    }
  });
  
  // Handle option selection
  Array.from(document.querySelectorAll('[role="option"]')).forEach(option => {
    option.addEventListener('click', function() {
      document.getElementById('selected-country').textContent = this.textContent;
      document.getElementById('country-listbox').hidden = true;
      document.getElementById('country-button').setAttribute('aria-expanded', 'false');
      document.getElementById('country-button').focus();
    });
    
    // Add keyboard handling for options
    option.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        this.click();
      }
    });
  });
</script>
```

### Custom Checkbox

```html
<div class="custom-checkbox">
  <input type="checkbox" id="terms" class="visually-hidden">
  <label for="terms" class="checkbox-label">
    <span class="checkbox-indicator" aria-hidden="true"></span>
    I agree to the terms and conditions
  </label>
</div>

<style>
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}

.checkbox-label {
  display: inline-flex;
  align-items: center;
  cursor: pointer;
}

.checkbox-indicator {
  display: inline-block;
  width: 20px;
  height: 20px;
  margin-right: 10px;
  border: 2px solid #555;
  border-radius: 4px;
  background-color: white;
}

input[type="checkbox"]:checked + .checkbox-label .checkbox-indicator {
  background-color: #2196F3;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='white' d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z'/%3E%3C/svg%3E");
  background-size: 80%;
  background-position: center;
  background-repeat: no-repeat;
}

input[type="checkbox"]:focus + .checkbox-label .checkbox-indicator {
  outline: 2px solid #1976d2;
  outline-offset: 2px;
}
</style>
```

## Form Submission

### Submit Buttons

```html
<button type="submit">Submit Form</button>

<!-- Not: -->
<input type="submit" value="Submit Form">
```

### Feedback on Submission

```html
<!-- Loading state -->
<button type="submit" id="submit-button">
  Submit
</button>

<script>
document.querySelector('form').addEventListener('submit', function(e) {
  e.preventDefault();
  
  const button = document.getElementById('submit-button');
  button.disabled = true;
  button.innerHTML = '<span class="spinner" aria-hidden="true"></span> Submitting...';
  button.setAttribute('aria-busy', 'true');
  
  // AJAX submission
  // ...
  
  // After success/failure
  const statusMessage = document.getElementById('status-message');
  statusMessage.textContent = 'Form submitted successfully!';
  statusMessage.removeAttribute('hidden');
  statusMessage.focus();
  
  button.disabled = false;
  button.innerHTML = 'Submit';
  button.removeAttribute('aria-busy');
});
</script>

<div id="status-message" role="status" tabindex="-1" hidden></div>
```

## Common Form Accessibility Issues

1. **Missing labels**: Form controls without proper label association
2. **Placeholder as label**: Using placeholder text instead of visible labels
3. **Poor error handling**: Error messages not associated with inputs
4. **Missing focus indication**: No visible focus state on form controls
5. **No keyboard support**: Custom controls not operable with keyboard
6. **Required field indication**: No clear indication of which fields are required