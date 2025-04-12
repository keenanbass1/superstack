# Semantic HTML Guide

Semantic HTML is the foundation of web accessibility. Using the right HTML elements for their intended purpose provides built-in accessibility benefits and reduces the need for ARIA attributes.

## Why Semantic HTML Matters

1. **Accessibility**: Screen readers and assistive technologies understand semantic elements
2. **SEO**: Search engines better understand your content and its structure
3. **Maintainability**: Code is more readable and consistent
4. **Mobile**: Proper semantics help with responsive design

## Key Semantic Elements

### Document Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Page Title</title>
  <meta name="description" content="Page description">
</head>
<body>
  <header>
    <nav>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
      </ul>
    </nav>
  </header>
  
  <main>
    <article>
      <h1>Main Article Title</h1>
      <p>Article content...</p>
      
      <section>
        <h2>Section Heading</h2>
        <p>Section content...</p>
      </section>
    </article>
    
    <aside>
      <h2>Related Information</h2>
      <p>Sidebar content...</p>
    </aside>
  </main>
  
  <footer>
    <p>&copy; 2025 Example Company</p>
  </footer>
</body>
</html>
```

### Text Structure

```html
<!-- Headings in hierarchical order -->
<h1>Main Page Title</h1>
<h2>Section Title</h2>
<h3>Subsection Title</h3>

<!-- Paragraphs -->
<p>This is a paragraph of text.</p>

<!-- Emphasis -->
<em>Emphasized text</em>
<strong>Strongly emphasized text</strong>

<!-- Lists -->
<ul>
  <li>Unordered list item</li>
  <li>Another unordered item</li>
</ul>

<ol>
  <li>First ordered item</li>
  <li>Second ordered item</li>
</ol>

<dl>
  <dt>Definition term</dt>
  <dd>Definition description</dd>
</dl>

<!-- Quotes -->
<blockquote cite="https://example.com">
  <p>A longer quote that stands on its own.</p>
  <footer>— <cite>Author Name</cite></footer>
</blockquote>

<p>The author said <q>this is an inline quote</q>.</p>

<!-- Code -->
<pre><code>function example() {
  return 'This is code';
}</code></pre>

<p>The <code>button</code> element creates a button.</p>

<!-- Time -->
<time datetime="2025-04-10">April 10, 2025</time>
```

### Interactive Elements

```html
<!-- Links -->
<a href="/page">Link text</a>

<!-- Buttons -->
<button type="button">Click me</button>

<!-- Forms -->
<form action="/submit" method="post">
  <fieldset>
    <legend>Personal Information</legend>
    
    <div>
      <label for="name">Name:</label>
      <input id="name" type="text">
    </div>
    
    <div>
      <label for="email">Email:</label>
      <input id="email" type="email">
    </div>
  </fieldset>
  
  <button type="submit">Submit</button>
</form>

<!-- Details/Summary (Accordion) -->
<details>
  <summary>Click to expand</summary>
  <p>Hidden content revealed when expanded.</p>
</details>
```

### Media

```html
<!-- Images -->
<figure>
  <img src="image.jpg" alt="Descriptive text">
  <figcaption>Caption for the image</figcaption>
</figure>

<!-- Video -->
<figure>
  <video controls>
    <source src="video.mp4" type="video/mp4">
    <track src="captions.vtt" kind="subtitles" srclang="en" label="English">
    Your browser does not support the video tag.
  </video>
  <figcaption>Video description</figcaption>
</figure>

<!-- Audio -->
<audio controls>
  <source src="audio.mp3" type="audio/mpeg">
  Your browser does not support the audio element.
</audio>
```

### Tables

```html
<table>
  <caption>Monthly Budget</caption>
  <thead>
    <tr>
      <th scope="col">Category</th>
      <th scope="col">Amount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Housing</th>
      <td>$1,000</td>
    </tr>
    <tr>
      <th scope="row">Food</th>
      <td>$500</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <th scope="row">Total</th>
      <td>$1,500</td>
    </tr>
  </tfoot>
</table>
```

## Common Non-Semantic Patterns to Avoid

### Avoid: Div Soup

```html
<!-- Bad: Div soup with no semantics -->
<div class="header">
  <div class="nav">
    <div class="nav-item"><a href="/">Home</a></div>
    <div class="nav-item"><a href="/about">About</a></div>
  </div>
</div>

<!-- Good: Semantic elements -->
<header>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</header>
```

### Avoid: Faking Buttons with Links

```html
<!-- Bad: Link styled as button -->
<a href="#" onclick="submitForm()" class="button">Submit</a>

<!-- Good: Actual button element -->
<button type="button" onclick="submitForm()">Submit</button>
```

### Avoid: Using Headings for Styling

```html
<!-- Bad: Using h1 just for large text -->
<h1 class="large-text">This is not a heading, just big text</h1>

<!-- Good: Using CSS for styling, heading for structure -->
<p class="large-text">This is not a heading, just big text</p>
```

## Testing Semantic HTML

To verify your HTML is semantic:
1. **Remove all CSS**: The page should still have a logical structure
2. **Use a screen reader**: Try navigating your page with a screen reader
3. **Keyboard navigation**: Make sure you can access all features
4. **Validate your HTML**: Use validation tools to check for errors

## Semantic HTML Checklist

✅ Page has a single `<h1>` element  
✅ Headings follow a logical hierarchy (h1 → h2 → h3)  
✅ Lists are marked up with `<ul>`, `<ol>`, or `<dl>`  
✅ Navigation is within `<nav>` elements  
✅ Primary content is in `<main>`  
✅ `<button>` used for actions, `<a>` used for navigation  
✅ `<table>` only used for tabular data  
✅ Forms properly use `<label>`, `<fieldset>`, and `<legend>`  
✅ Images have appropriate alt text  
✅ `<time>` used for dates and times  