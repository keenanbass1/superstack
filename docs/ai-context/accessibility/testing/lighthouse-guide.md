# Lighthouse Accessibility Testing Guide

Google Lighthouse provides accessibility audits as part of its comprehensive web page analysis. This guide covers how to effectively use Lighthouse for accessibility testing.

## Lighthouse Capabilities

Lighthouse checks for many accessibility issues and provides scores based on the severity and prevalence of issues found.

### What Lighthouse Checks

- Correctly labeled elements
- Sufficient color contrast
- Appropriate ARIA attributes
- Keyboard navigability
- Document structure
- Text alternatives for non-text content

## Running Lighthouse Tests

### Chrome DevTools

1. Open Chrome DevTools (F12)
2. Go to the "Lighthouse" tab
3. Select "Accessibility" category
4. Click "Generate report"

### Command Line

```bash
# Install Lighthouse
npm install -g lighthouse

# Run test
lighthouse https://example.com --only-categories=accessibility --output=html --output-path=./report.html
```

### Programmatic Use

```javascript
const lighthouse = require('lighthouse');
const chromeLauncher = require('chrome-launcher');

async function runLighthouse(url) {
  const chrome = await chromeLauncher.launch();
  const options = {
    port: chrome.port,
    onlyCategories: ['accessibility']
  };
  
  const results = await lighthouse(url, options);
  await chrome.kill();
  
  return results;
}

runLighthouse('https://example.com')
  .then(results => console.log(results.lhr.categories.accessibility.score));
```

## Understanding Lighthouse Results

### Accessibility Score

The score (0-100) represents the estimated accessibility of your page:
- 0-49: Poor
- 50-89: Needs improvement
- 90-100: Good

### Audit Categories

Lighthouse organizes accessibility audits into categories:

1. **Names and labels**
   - Elements have accessible names
   - Form elements have associated labels

2. **Contrast**
   - Text has sufficient contrast with background
   - UI components have sufficient contrast

3. **Tables and lists**
   - Tables have headers and proper structure
   - Lists use appropriate markup

4. **Navigation**
   - Page has a proper heading structure
   - Focus order is logical
   - Focus is visible

5. **ARIA**
   - ARIA attributes are valid
   - ARIA roles are used appropriately

## Common Lighthouse Accessibility Findings

### Contrast Issues

```
Failing Elements:
.header-link (2.7:1)
.footer-text (3.8:1)

Background: #FFFFFF
Foreground: #999999
Required Ratio: 4.5:1
```

### Missing Alternative Text

```
Failing Elements:
img.hero-image
input[type="image"].submit-button

Issue: Images do not have alt attributes
```

### Document Structure

```
Failing Elements:
<html>

Issue: Document doesn't have a <title> element
```

## Best Practices for Lighthouse Testing

1. **Test regularly**: Include in development workflow
2. **Test on multiple pages**: Don't just test the homepage
3. **Test with different settings**: Try with different devices and throttling options
4. **Fix high-impact issues first**: Prioritize based on severity
5. **Combine with manual testing**: Lighthouse can't catch everything
6. **Automate in CI/CD**: Include in your build process
7. **Compare over time**: Track accessibility score changes