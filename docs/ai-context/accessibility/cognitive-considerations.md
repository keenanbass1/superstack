# Cognitive Accessibility Considerations

Cognitive accessibility encompasses design practices that make content and interactions understandable and usable for people with cognitive disabilities, learning disabilities, memory impairments, attention limitations, and other cognitive differences.

## Core Principles

### 1. Clear and Simple Content

Present information in a clear, straightforward manner:

- Use plain language and avoid jargon
- Break complex information into manageable chunks
- Provide summaries for longer content
- Use clear headings and subheadings to organize content

Example of simplifying text:

```html
<!-- Complex version -->
<p>
  The aforementioned application must be submitted prior to the specified deadline
  in accordance with regulatory requirements. Failure to adhere to the submission
  timeline will result in the invalidation of your application.
</p>

<!-- Simplified version -->
<p>
  You must submit your application before the deadline. 
  Late applications will not be accepted.
</p>
```

### 2. Consistent Design and Navigation

Maintain consistent patterns throughout the interface:

- Use consistent layouts across pages
- Keep navigation in the same location
- Use familiar UI patterns
- Make interactive elements look consistent

Example of consistent navigation:

```html
<header>
  <nav aria-label="Main Navigation">
    <ul>
      <li><a href="/" class="nav-item">Home</a></li>
      <li><a href="/about" class="nav-item">About</a></li>
      <li><a href="/services" class="nav-item">Services</a></li>
      <li><a href="/contact" class="nav-item">Contact</a></li>
    </ul>
  </nav>
</header>

<style>
  /* Consistent styling for navigation items */
  .nav-item {
    display: block;
    padding: 10px 15px;
    text-decoration: none;
    color: #333;
    font-weight: 500;
  }
  
  .nav-item:hover, 
  .nav-item:focus {
    background-color: #f5f5f5;
    color: #0066cc;
  }
  
  /* Consistent focus indication */
  .nav-item:focus-visible {
    outline: 2px solid #0066cc;
    outline-offset: 2px;
  }
</style>
```

### 3. Multiple Ways to Understand Content

Provide information in different formats to accommodate different learning styles:

- Accompany text with relevant images
- Use diagrams to explain complex concepts
- Offer video alternatives to text
- Provide text alternatives to media content

Example of multiple formats:

```html
<div class="concept-explanation">
  <h2>How Solar Panels Work</h2>
  
  <p>
    Solar panels convert sunlight into electricity. When sunlight hits the panel,
    it energizes electrons in the silicon cells, creating an electric current.
  </p>
  
  <figure>
    <img 
      src="solar-diagram.png" 
      alt="Diagram showing sunlight hitting solar panel, creating electrical flow through circuits"
      width="500" 
      height="300">
    <figcaption>Solar energy conversion process</figcaption>
  </figure>
  
  <div class="video-explanation">
    <h3>Watch: Solar Panels Explained</h3>
    <video controls>
      <source src="solar-explanation.mp4" type="video/mp4">
      <track kind="captions" src="solar-captions.vtt" srclang="en" label="English">
    </video>
  </div>
</div>
```

### 4. Error Prevention and Recovery

Help users avoid errors and recover when they make mistakes:

- Provide clear instructions
- Use validation and confirmation
- Offer helpful error messages
- Allow users to undo actions

Example of form error prevention:

```html
<form>
  <div class="form-field">
    <label for="phone">
      Phone Number (format: 555-555-5555)
    </label>
    <input 
      type="tel" 
      id="phone" 
      pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"
      placeholder="555-555-5555"
      aria-describedby="phone-format">
    <span id="phone-format" class="field-hint">
      Use this format: 555-555-5555
    </span>
  </div>
  
  <div class="form-actions">
    <button type="reset">Clear Form</button>
    <button type="submit">Submit</button>
  </div>
</form>

<script>
  const form = document.querySelector('form');
  const phoneInput = document.getElementById('phone');
  
  phoneInput.addEventListener('input', function() {
    // Auto-format as user types
    let value = this.value.replace(/\D/g, ''); // Remove non-digits
    if (value.length > 3) {
      value = value.substring(0,3) + '-' + value.substring(3);
    }
    if (value.length > 7) {
      value = value.substring(0,7) + '-' + value.substring(7);
    }
    if (value.length > 12) {
      value = value.substring(0,12);
    }
    this.value = value;
  });
  
  form.addEventListener('submit', function(e) {
    if (!phoneInput.checkValidity()) {
      e.preventDefault();
      
      // Show a clear error message
      const errorElement = document.createElement('div');
      errorElement.className = 'error-message';
      errorElement.textContent = 'Please enter a valid phone number: 555-555-5555';
      errorElement.id = 'phone-error';
      phoneInput.setAttribute('aria-invalid', 'true');
      phoneInput.setAttribute('aria-describedby', 'phone-format phone-error');
      
      const existingError = document.getElementById('phone-error');
      if (existingError) {
        existingError.remove();
      }
      
      phoneInput.parentNode.appendChild(errorElement);
      phoneInput.focus();
    }
  });
</script>

<style>
  .field-hint {
    display: block;
    margin-top: 5px;
    font-size: 0.9em;
    color: #555;
  }
  
  .error-message {
    color: #d32f2f;
    margin-top: 5px;
    font-weight: bold;
  }
  
  input[aria-invalid="true"] {
    border-color: #d32f2f;
    background-color: #ffebee;
  }
</style>
```

### 5. Minimize Cognitive Load

Reduce the amount of information users need to remember:

- Use recognition rather than recall
- Provide visual cues and meaningful icons
- Maintain important context on screen
- Minimize the number of steps to complete tasks

Example of minimizing cognitive load in a checkout process:

```html
<div class="checkout-process">
  <!-- Progress indicator -->
  <ul class="checkout-steps">
    <li class="step completed">
      <span class="step-number">1</span>
      <span class="step-name">Cart</span>
    </li>
    <li class="step current">
      <span class="step-number">2</span>
      <span class="step-name">Shipping</span>
    </li>
    <li class="step">
      <span class="step-number">3</span>
      <span class="step-name">Payment</span>
    </li>
    <li class="step">
      <span class="step-number">4</span>
      <span class="step-name">Confirm</span>
    </li>
  </ul>
  
  <!-- Order summary that stays visible -->
  <div class="order-summary">
    <h2>Order Summary</h2>
    <ul class="order-items">
      <li>Product A - $25.00</li>
      <li>Product B - $15.00</li>
    </ul>
    <p class="order-total">Total: $40.00</p>
  </div>
  
  <!-- Form with grouped fields -->
  <form class="shipping-form">
    <fieldset>
      <legend>Shipping Address</legend>
      
      <div class="form-row">
        <div class="form-field">
          <label for="first-name">First Name</label>
          <input type="text" id="first-name" autocomplete="given-name">
        </div>
        <div class="form-field">
          <label for="last-name">Last Name</label>
          <input type="text" id="last-name" autocomplete="family-name">
        </div>
      </div>
      
      <!-- More address fields -->
    </fieldset>
    
    <div class="form-actions">
      <button type="button" class="secondary-button">Back to Cart</button>
      <button type="submit" class="primary-button">Continue to Payment</button>
    </div>
  </form>
</div>

<style>
  .checkout-steps {
    display: flex;
    list-style: none;
    padding: 0;
    margin-bottom: 30px;
  }
  
  .step {
    flex: 1;
    text-align: center;
    position: relative;
  }
  
  .step:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 15px;
    right: -10px;
    width: 100%;
    height: 2px;
    background-color: #ddd;
    z-index: -1;
  }
  
  .step-number {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background-color: #ddd;
    margin: 0 auto 5px;
  }
  
  .step.completed .step-number {
    background-color: #4caf50;
    color: white;
  }
  
  .step.current .step-number {
    background-color: #2196f3;
    color: white;
  }
  
  .order-summary {
    position: sticky;
    top: 20px;
    background-color: #f8f8f8;
    padding: 15px;
    border-radius: 4px;
    margin-bottom: 20px;
  }
  
  .form-row {
    display: flex;
    gap: 15px;
    margin-bottom: 15px;
  }
  
  .form-field {
    flex: 1;
  }
  
  .form-actions {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
  }
</style>
```

## Time-Based Considerations

People with cognitive disabilities may need more time to process information or complete tasks.

### Avoid Time Limits

Whenever possible, eliminate time constraints or provide options to extend time:

```html
<div class="timed-session">
  <div class="timer-warning" hidden id="session-warning">
    <p>Your session will expire in <span id="countdown">5:00</span> minutes.</p>
    <button type="button" id="extend-session">Extend Session</button>
  </div>
  
  <!-- Main content -->
</div>

<script>
  // Initialize session timeout (in milliseconds)
  let sessionTimeout = 25 * 60 * 1000; // 25 minutes
  let warningTime = 5 * 60 * 1000; // Show warning 5 minutes before expiration
  let countdownInterval;
  let sessionTimer;
  
  function startSessionTimer() {
    // Set timeout to show warning
    sessionTimer = setTimeout(() => {
      document.getElementById('session-warning').hidden = false;
      startCountdown();
    }, sessionTimeout - warningTime);
  }
  
  function startCountdown() {
    let timeLeft = warningTime;
    
    countdownInterval = setInterval(() => {
      timeLeft -= 1000;
      
      if (timeLeft <= 0) {
        clearInterval(countdownInterval);
        // Instead of automatically logging out, show a prompt
        showSessionExpiredPrompt();
      } else {
        // Update countdown display
        const minutes = Math.floor(timeLeft / 60000);
        const seconds = Math.floor((timeLeft % 60000) / 1000);
        document.getElementById('countdown').textContent = 
          `${minutes}:${seconds.toString().padStart(2, '0')}`;
      }
    }, 1000);
  }
  
  function extendSession() {
    // Clear existing timers
    clearTimeout(sessionTimer);
    clearInterval(countdownInterval);
    
    // Hide warning
    document.getElementById('session-warning').hidden = true;
    
    // Restart session timer
    startSessionTimer();
  }
  
  function showSessionExpiredPrompt() {
    const wantsToContinue = confirm(
      "Your session has expired. Would you like to continue working? " +
      "Click OK to continue or Cancel to log out."
    );
    
    if (wantsToContinue) {
      extendSession();
    } else {
      // Redirect to logout page
      window.location.href = '/logout';
    }
  }
  
  // Set up event listener for extend button
  document.getElementById('extend-session').addEventListener('click', extendSession);
  
  // Start the initial session timer
  startSessionTimer();
</script>
```

### Minimize Animations and Motion

Provide controls for animations that can be distracting:

```html
<div class="animation-controls">
  <button 
    id="toggle-animations" 
    aria-pressed="false"
    onclick="toggleAnimations()">
    Pause Animations
  </button>
</div>

<div class="animated-carousel" id="carousel">
  <!-- Carousel content -->
</div>

<script>
  function toggleAnimations() {
    const button = document.getElementById('toggle-animations');
    const carousel = document.getElementById('carousel');
    const isActive = button.getAttribute('aria-pressed') === 'true';
    
    if (isActive) {
      // Re-enable animations
      carousel.classList.remove('animations-paused');
      button.setAttribute('aria-pressed', 'false');
      button.textContent = 'Pause Animations';
    } else {
      // Disable animations
      carousel.classList.add('animations-paused');
      button.setAttribute('aria-pressed', 'true');
      button.textContent = 'Resume Animations';
    }
  }
</script>

<style>
  .animations-paused * {
    animation-play-state: paused !important;
    transition: none !important;
  }
  
  @media (prefers-reduced-motion: reduce) {
    /* Automatically reduce motion for users with this preference */
    .animated-carousel {
      animation-play-state: paused !important;
      transition: none !important;
    }
  }
</style>
```

## Reading and Language Support

### Support for Reading Difficulties

Implement features that help users with reading difficulties:

```html
<div class="article-content">
  <div class="reading-controls">
    <button onclick="adjustTextSize(1)">Increase Text Size</button>
    <button onclick="adjustTextSize(-1)">Decrease Text Size</button>
    <button onclick="toggleLineFocus()">Toggle Line Focus</button>
    <button onclick="toggleDyslexiaFont()">Dyslexia-Friendly Font</button>
  </div>
  
  <article id="content" class="text-adjustable">
    <h1>Article Title</h1>
    <p>Article paragraph with content...</p>
    <p>Another paragraph with more content...</p>
  </article>
</div>

<script>
  let currentSize = 100; // percentage
  const content = document.getElementById('content');
  
  function adjustTextSize(change) {
    currentSize += change * 10; // increase/decrease by 10%
    currentSize = Math.min(Math.max(70, currentSize), 200); // Keep between 70% and 200%
    content.style.fontSize = `${currentSize}%`;
  }
  
  function toggleLineFocus() {
    content.classList.toggle('line-focus-active');
  }
  
  function toggleDyslexiaFont() {
    content.classList.toggle('dyslexia-font');
  }
</script>

<style>
  .text-adjustable {
    line-height: 1.5;
    max-width: 70ch; /* Optimal line length for readability */
  }
  
  .line-focus-active p {
    line-height: 2.5;
  }
  
  .line-focus-active p:hover,
  .line-focus-active p:focus-within {
    background-color: rgba(255, 255, 0, 0.2);
  }
  
  .dyslexia-font {
    font-family: 'Open Dyslexic', 'Comic Sans MS', 'Arial', sans-serif;
    letter-spacing: 0.05em;
    word-spacing: 0.1em;
  }
</style>
```

### Definitions and Explanations

Provide explanations for complex terms or concepts:

```html
<p>
  The treatment uses
  <span class="term" tabindex="0" aria-describedby="definition-phototherapy">
    phototherapy
    <span class="definition" role="tooltip" id="definition-phototherapy">
      Phototherapy: Treatment using special light to help skin conditions
    </span>
  </span>
  to improve symptoms.
</p>

<style>
  .term {
    text-decoration: dotted underline;
    position: relative;
    cursor: help;
  }
  
  .definition {
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: #333;
    color: white;
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 14px;
    width: 250px;
    visibility: hidden;
    opacity: 0;
    transition: opacity 0.3s;
    z-index: 10;
  }
  
  .term:hover .definition,
  .term:focus .definition {
    visibility: visible;
    opacity: 1;
  }
</style>
```

## Memory Support Features

### Reminders and Progress Indicators

Help users track progress and remember where they are:

```html
<div class="multi-step-form">
  <div class="progress-tracker">
    <div class="progress-bar" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100">
      <div class="progress-filled" style="width: 40%"></div>
    </div>
    <p class="progress-status">Step 2 of 5 completed</p>
  </div>
  
  <div class="form-section">
    <h2>Step 3: Personal Information</h2>
    <!-- Form fields -->
  </div>
  
  <div class="persistent-summary">
    <h3>Your Selections So Far</h3>
    <ul class="selection-list">
      <li>Step 1: Selected Plan - Premium</li>
      <li>Step 2: Options - Extra Storage, Mobile Access</li>
    </ul>
  </div>
  
  <div class="form-navigation">
    <button type="button" class="back-button">Back to Step 2</button>
    <button type="button" class="save-button">Save Progress</button>
    <button type="button" class="next-button">Continue to Step 4</button>
  </div>
</div>

<style>
  .progress-tracker {
    margin-bottom: 20px;
  }
  
  .progress-bar {
    height: 10px;
    background-color: #eee;
    border-radius: 5px;
    overflow: hidden;
  }
  
  .progress-filled {
    height: 100%;
    background-color: #4caf50;
  }
  
  .persistent-summary {
    background-color: #f8f8f8;
    padding: 15px;
    border-radius: 4px;
    margin: 20px 0;
  }
  
  .form-navigation {
    display: flex;
    justify-content: space-between;
    margin-top: 30px;
  }
</style>
```

### Save and Resume

Allow users to save progress and come back later:

```html
<div class="form-container">
  <div class="save-status">
    <span id="autosave-status">All changes saved</span>
    <button id="manual-save">Save Progress</button>
  </div>
  
  <form id="long-form">
    <!-- Form fields -->
    <input type="text" id="name" name="name" autocomplete="name">
    <!-- More fields -->
  </form>
  
  <div class="form-footer">
    <button type="button" id="exit-button">Save and Exit</button>
    <button type="submit" form="long-form">Complete Submission</button>
  </div>
</div>

<script>
  const form = document.getElementById('long-form');
  const saveStatus = document.getElementById('autosave-status');
  const manualSave = document.getElementById('manual-save');
  const exitButton = document.getElementById('exit-button');
  
  // Set up autosave on field changes
  form.addEventListener('input', debounce(() => {
    saveProgress();
  }, 2000));
  
  // Manual save button
  manualSave.addEventListener('click', () => {
    saveProgress();
  });
  
  // Exit button
  exitButton.addEventListener('click', () => {
    saveProgress();
    // Show confirmation
    alert('Your progress has been saved. You can return to complete this form later.');
    // Redirect to home
    window.location.href = '/home';
  });
  
  // Save progress function
  function saveProgress() {
    // Save form data to localStorage
    const formData = new FormData(form);
    const formObject = {};
    
    formData.forEach((value, key) => {
      formObject[key] = value;
    });
    
    localStorage.setItem('savedFormData', JSON.stringify(formObject));
    
    // Update save status
    saveStatus.textContent = 'All changes saved';
    
    // Visual indicator
    saveStatus.classList.add('flash');
    setTimeout(() => {
      saveStatus.classList.remove('flash');
    }, 1000);
  }
  
  // Load saved data on page load
  window.addEventListener('load', () => {
    const savedData = localStorage.getItem('savedFormData');
    
    if (savedData) {
      const formObject = JSON.parse(savedData);
      
      // Populate form fields
      Object.keys(formObject).forEach(key => {
        const field = form.elements[key];
        if (field) {
          field.value = formObject[key];
        }
      });
      
      // Show restore message
      const restoreMessage = document.createElement('div');
      restoreMessage.className = 'restore-message';
      restoreMessage.innerHTML = `
        <p>We've restored your previously saved information.</p>
        <button type="button" id="clear-data">Clear saved data and start fresh</button>
      `;
      
      form.insertBefore(restoreMessage, form.firstChild);
      
      document.getElementById('clear-data').addEventListener('click', () => {
        localStorage.removeItem('savedFormData');
        window.location.reload();
      });
    }
  });
  
  // Debounce helper function
  function debounce(func, wait) {
    let timeout;
    return function() {
      const context = this;
      const args = arguments;
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        func.apply(context, args);
      }, wait);
    };
  }
</script>

<style>
  .save-status {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 10px;
    margin-bottom: 15px;
    font-size: 14px;
    color: #666;
  }
  
  .flash {
    animation: flash-animation 1s;
  }
  
  @keyframes flash-animation {
    0% { color: #666; }
    50% { color: #4caf50; font-weight: bold; }
    100% { color: #666; }
  }
  
  .restore-message {
    background-color: #e3f2fd;
    padding: 10px 15px;
    border-radius: 4px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
</style>
```

## Testing for Cognitive Accessibility

1. **Text complexity**: Run content through readability analyzers
2. **Consistency check**: Audit for consistent layouts, terminology, and navigation
3. **Error handling**: Test form submissions with incorrect data
4. **Memory load**: Evaluate how much information users need to remember
5. **Distractions**: Assess animations and potentially distracting elements
6. **Time limits**: Test with extended time needed to complete tasks
7. **User testing**: Include people with cognitive disabilities in testing
8. **Reading support**: Verify text customization features work properly