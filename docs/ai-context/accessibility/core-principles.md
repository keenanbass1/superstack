# Core Principles of Web Accessibility

## The POUR Framework

Accessibility is built on four foundational principles, known as POUR:

### 1. Perceivable
Information and user interface components must be presentable to users in ways they can perceive. This means:

- Text alternatives for non-text content
- Captions and alternatives for multimedia
- Content that can be presented in different ways
- Content that is distinguishable (e.g., separating foreground from background)

#### Key Requirements:
- All non-text content has text alternatives
- Time-based media has captions and audio descriptions
- Content can be presented in different ways without losing meaning
- Users can distinguish foreground content from background

### 2. Operable
User interface components and navigation must be operable by all users. This means:

- All functionality is available from a keyboard
- Users have enough time to read and use content
- Content does not cause seizures or physical discomfort
- Users can navigate, find content, and determine where they are

#### Key Requirements:
- All functionality works with keyboard-only input
- Users can pause, stop, or extend time limits
- Nothing flashes more than three times per second
- Multiple ways to find pages within a website
- Clear page titles and focused context

### 3. Understandable
Information and operation of the user interface must be understandable. This means:

- Text is readable and understandable
- Content appears and operates in predictable ways
- Users are helped to avoid and correct mistakes

#### Key Requirements:
- The language of the page is programmatically identified
- Navigation is consistent throughout the website
- Input assistance is provided (labels, error identification, etc.)
- Error messages are clear and provide suggestions

### 4. Robust
Content must be robust enough to be interpreted reliably by a wide variety of user agents, including assistive technologies. This means:

- Compatibility with current and future user tools
- Properly formed code that can be reliably interpreted

#### Key Requirements:
- Clean, valid HTML with proper nesting
- All UI components have proper names, roles, and values
- Status messages can be programmatically determined

## Universal Design Principles

Beyond WCAG, Universal Design principles help create accessible experiences:

1. **Equitable Use**: Useful to people with diverse abilities
2. **Flexibility in Use**: Accommodates a wide range of preferences
3. **Simple and Intuitive**: Easy to understand regardless of experience
4. **Perceptible Information**: Communicates information effectively
5. **Tolerance for Error**: Minimizes adverse consequences of accidents
6. **Low Physical Effort**: Can be used efficiently and comfortably
7. **Size and Space for Approach and Use**: Appropriate size and space for use

## Practical Application

When implementing any feature, consider:

1. **Can everyone perceive it?** Consider blind, low vision, deaf, and colorblind users.
2. **Can everyone operate it?** Consider keyboard-only users, people with motor disabilities, and those with limited time.
3. **Can everyone understand it?** Consider clear language, consistent patterns, and helpful error messages.
4. **Is it robust?** Test with assistive technology and validate your code.