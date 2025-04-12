# Visual Hierarchy

> This module provides a comprehensive understanding of visual hierarchy principles for effective information organization and user attention guidance in UI/UX design.

## Metadata
- **Priority:** high
- **Domain:** design
- **Target Models:** claude, gpt
- **Related Modules:** typography, spacing-systems, color-theory

## Module Overview

Visual hierarchy is a fundamental design concept that determines how users perceive and interact with interfaces. This module covers core principles, implementation patterns, decision frameworks, and anti-patterns to help you create effective visual hierarchies.

<!-- 
NOTE: This module is structured following optimal prompt engineering principles:
1. Each section begins with a clear conceptual foundation
2. Content is organized from most to least important
3. Examples use few-shot patterns to demonstrate application
4. Decision trees guide practical implementation
5. Anti-patterns show common mistakes to avoid
6. Model-specific notes provide tailored guidance
-->

<context name="visual_hierarchy_definition" priority="high">
## Conceptual Foundation

Visual hierarchy is the deliberate arrangement of elements to show their order of importance, guiding users through content in an intended sequence. It creates intuitive paths for information consumption and action.

A well-designed visual hierarchy:
- Directs user attention to the most important information first
- Organizes content into logical groups and relationships
- Creates predictable patterns that reduce cognitive load
- Differentiates between interactive and static elements
- Supports both quick scanning and detailed reading

When implemented correctly, users intuitively understand:
1. Where to look first
2. What elements are most important
3. How information is related
4. What actions they can take
</context>

<context name="visual_hierarchy_core_principles" priority="high">
## Core Principles

### 1. Size Relationships
Large elements attract attention before smaller ones. This fundamental principle works because:
- Larger elements occupy more visual space in our field of vision
- Size differential creates immediate visual priority
- Our visual system is wired to notice larger objects first

**Implementation Guidelines:**
- Make the most important elements largest (typically 2-3× larger than body text)
- Use a consistent scale ratio (e.g., 1.2× or 1.5×) between hierarchy levels
- Ensure size differences are large enough to create clear distinction
- Consider responsive behavior across device sizes

**Example: Size Hierarchy in Action**
```
MAIN HEADLINE (24px)
Subheading (18px)
Body text (16px) describing the content in detail with supporting information
that elaborates on the main concept introduced in the headline.
Caption text (12px) providing supplementary information
```

### 2. Color & Contrast
High-contrast elements draw more attention than low-contrast ones. This works because:
- Our visual system is attracted to areas of high contrast
- Color can create emotional impact and signify importance
- Different colors have different visual weights

**Implementation Guidelines:**
- Use highest contrast for primary elements (against background)
- Reserve saturated colors for important interactive elements
- Employ brand colors to indicate primary actions
- Create a deliberate contrast hierarchy (primary, secondary, tertiary)

**Example: Contrast Hierarchy**
| Element | Background | Text/Icon | Contrast Ratio |
|---------|------------|-----------|----------------|
| Primary button | #3366FF | #FFFFFF | 4.5:1 |
| Secondary button | #EAEAEA | #333333 | 12:1 |
| Disabled button | #F5F5F5 | #999999 | 2.5:1 |

### 3. Typography Hierarchy
Different typographic treatments signal different levels of importance. This works because:
- Weight, size, and style variations create visual distinction
- Consistent typographic patterns establish predictable hierarchy
- Font characteristics influence reading behavior

**Implementation Guidelines:**
- Use weight to differentiate content types (bold: 700, semibold: 600, regular: 400)
- Scale size following a consistent ratio (1.2-1.5× between levels)
- Decrease line height as font size increases
- Limit number of font styles to maintain clarity

**Example: Typography System**
```
# Heading 1 (24px, 700 weight, 1.2 line height)
## Heading 2 (20px, 600 weight, 1.3 line height)
### Heading 3 (18px, 600 weight, 1.4 line height)

Body text (16px, 400 weight, 1.5 line height) for the main content.

*Emphasized text* within the content flow.
```

### 4. Spatial Relationships
How elements are positioned relative to each other affects their perceived importance. This works because:
- Proximity indicates relationship
- White space draws attention to isolated elements
- Alignment creates visual connection
- Position influences viewing sequence

**Implementation Guidelines:**
- Group related elements with consistent spacing
- Use larger spacing to separate logical sections
- Position high-priority content in natural starting points (top-left for Western languages)
- Create breathing room around important elements

**Example: Spacing Hierarchy**
```
Section heading
[16px gap]
Content block with related elements
[8px gap between related elements]
[24px gap]
Next section heading
```

### 5. Content Density
Areas with lower content density receive more visual attention. This works because:
- Dense content requires more cognitive processing
- White space creates emphasis
- Variation in density creates rhythm and focus points

**Implementation Guidelines:**
- Create lowest density around highest priority elements
- Maintain consistent density within logical groups
- Use density strategically to highlight or de-emphasize content
- Consider cultural reading patterns in density distribution
</context>

<context name="visual_hierarchy_implementation_patterns" priority="medium">
## Implementation Patterns

### Common Interface Hierarchies

#### Web/Application Interface Pattern
```
1. PRIMARY HEADING (H1)
   • Secondary Heading (H2)
      - Content group
        · Detail content
        · Supporting text
   • Related action
2. NEXT PRIMARY SECTION
```

#### Dashboard Hierarchy Pattern
```
1. GLOBAL NAVIGATION
2. PAGE TITLE & KEY METRICS
3. PRIMARY VISUALIZATION/CONTENT
4. SUPPORTING VISUALIZATIONS
5. DETAILED DATA TABLES
6. SECONDARY ACTIONS
```

#### Form Hierarchy Pattern
```
1. FORM TITLE/PURPOSE
2. INPUT FIELDS (grouped logically)
   - Field Label
   - Input Element
   - Validation/Help Text
3. FORM ACTIONS (submit, cancel)
4. SUPPLEMENTARY INFORMATION
```

### Typical Visual Attention Sequence

1. **Primary CTA/Critical Information** - Largest, highest contrast elements
   - Example: Main headline, hero image, primary button
   - Properties: Largest size, highest contrast, most distinctive color

2. **Key Supporting Information** - Second in prominence
   - Example: Benefits, features, subheadings
   - Properties: Medium size, strong contrast, supportive of primary elements

3. **Navigation Elements** - Clearly visible but less dominant
   - Example: Menu items, breadcrumbs, tabs
   - Properties: Consistent styling, medium contrast, conventional positioning

4. **Secondary Actions** - Present but visually subordinate
   - Example: "Learn more" links, secondary buttons, related content
   - Properties: Smaller size, medium-low contrast, secondary colors

5. **Tertiary Content** - Smallest, lowest contrast
   - Example: Footer content, legal text, metadata
   - Properties: Smallest size, lowest contrast, minimal visual weight
</context>

<context name="visual_hierarchy_decision_logic" priority="medium">
## Decision Logic for Implementation

When establishing visual hierarchy, follow this decision framework:

### Step 1: Content Analysis
First, analyze your content to understand its structure and importance:

```
START
│
├─ Identify the single most important element
│  └─ This will receive highest visual priority
│
├─ Group related content items
│  └─ These will share visual treatments
│
├─ Determine logical reading sequence
│  └─ This will inform layout flow
│
└─ Identify action items/CTAs
   └─ These need appropriate emphasis
```

### Step 2: Hierarchy Mapping
Next, map content importance to visual treatments:

```
FOR EACH content element:
│
├─ IF primary importance
│  └─ Apply strongest visual emphasis
│     (largest size, highest contrast, most prominent position)
│
├─ IF secondary importance
│  └─ Apply moderate visual emphasis
│     (medium size, strong contrast, supportive position)
│
├─ IF supporting content
│  └─ Apply subtle visual emphasis
│     (standard size, good readability, logical placement)
│
└─ IF tertiary/optional content
   └─ Apply minimal visual emphasis
      (smaller size, lower contrast, peripheral position)
```

### Step 3: Visual System Selection
Choose appropriate visual mechanisms based on content type:

```
IF text-heavy content:
│
├─ Primary emphasis: Size + Weight + Color
├─ Secondary emphasis: Weight + Color
└─ Tertiary emphasis: Size (smaller) + Color (muted)

IF visually-oriented content:
│
├─ Primary emphasis: Size + Position + Contrast
├─ Secondary emphasis: Position + Contrast
└─ Tertiary emphasis: Size (smaller) + Lower contrast

IF interactive interface:
│
├─ Primary actions: Size + Color + Prominence
├─ Secondary actions: Standard size + Distinct styling
└─ Tertiary actions: Text links or icon buttons
```

### Step 4: Validation Process
Test your hierarchy to ensure it creates the intended experience:

```
VALIDATION CHECKLIST:
│
├─ Squint test: Do important elements still stand out?
│
├─ Five-second test: What do users notice first?
│
├─ Reading flow: Does the eye follow the intended path?
│
├─ Consistency check: Are similar elements treated similarly?
│
└─ Accessibility check: Is contrast sufficient at all levels?
```
</context>

<context name="visual_hierarchy_code_implementation" priority="medium">
## Code Implementation

### CSS Variables for Hierarchy System

```css
:root {
  /* Typography scale - follows 1.25 ratio */
  --text-xs: 0.75rem;    /* 12px - supporting text */
  --text-sm: 0.875rem;   /* 14px - interface text */
  --text-base: 1rem;     /* 16px - body copy */
  --text-lg: 1.125rem;   /* 18px - emphasized content */
  --text-xl: 1.25rem;    /* 20px - subheadings */
  --text-2xl: 1.5rem;    /* 24px - section headings */
  --text-3xl: 1.875rem;  /* 30px - page headings */
  --text-4xl: 2.25rem;   /* 36px - major headlines */
  
  /* Font weights for hierarchy */
  --font-normal: 400;    /* Regular text */
  --font-medium: 500;    /* Slightly emphasized text */
  --font-semibold: 600;  /* Subheadings */
  --font-bold: 700;      /* Headings */
  
  /* Spacing scale - follows 1.5 ratio */
  --space-xs: 0.25rem;   /* 4px - minimal spacing */
  --space-sm: 0.5rem;    /* 8px - tight spacing */
  --space-md: 0.75rem;   /* 12px - standard spacing */
  --space-lg: 1rem;      /* 16px - component spacing */
  --space-xl: 1.5rem;    /* 24px - section spacing */
  --space-2xl: 2.25rem;  /* 36px - major sections */
  
  /* Z-index scale for layering hierarchy */
  --z-base: 0;           /* Default content */
  --z-above: 10;         /* Elements above content */
  --z-dropdown: 20;      /* Dropdown menus */
  --z-sticky: 30;        /* Sticky elements */
  --z-modal: 40;         /* Modal dialogs */
  --z-toast: 50;         /* Notifications */
}
```

### Implementing Text Hierarchy

```css
/* Heading hierarchy */
h1, .h1 {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  line-height: 1.2;
  margin-top: var(--space-2xl);
  margin-bottom: var(--space-xl);
  color: var(--color-text-primary);
}

h2, .h2 {
  font-size: var(--text-2xl);
  font-weight: var(--font-semibold);
  line-height: 1.3;
  margin-top: var(--space-xl);
  margin-bottom: var(--space-lg);
  color: var(--color-text-primary);
}

h3, .h3 {
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  line-height: 1.4;
  margin-top: var(--space-lg);
  margin-bottom: var(--space-md);
  color: var(--color-text-primary);
}

p, .body {
  font-size: var(--text-base);
  font-weight: var(--font-normal);
  line-height: 1.5;
  margin-bottom: var(--space-lg);
  color: var(--color-text-secondary);
}

.caption {
  font-size: var(--text-xs);
  font-weight: var(--font-normal);
  line-height: 1.5;
  color: var(--color-text-tertiary);
}
```

### Implementing Button Hierarchy

```css
/* Button hierarchy */
.btn-primary {
  font-size: var(--text-base);
  font-weight: var(--font-medium);
  padding: var(--space-md) var(--space-xl);
  background-color: var(--color-primary);
  color: white;
  border-radius: 4px;
  border: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.btn-secondary {
  font-size: var(--text-sm);
  font-weight: var(--font-normal);
  padding: var(--space-sm) var(--space-lg);
  background-color: var(--color-secondary);
  color: var(--color-text-primary);
  border-radius: 4px;
  border: 1px solid var(--color-border);
}

.btn-tertiary {
  font-size: var(--text-sm);
  font-weight: var(--font-normal);
  padding: var(--space-sm) var(--space-md);
  background-color: transparent;
  color: var(--color-primary);
  border: none;
  text-decoration: underline;
}
```

### React Component Example

```jsx
const ContentSection = () => (
  <section className="content-section">
    <h2 className="section-title">Feature Overview</h2>
    
    <p className="section-intro">
      Our platform provides powerful analytics with an intuitive interface.
    </p>
    
    <div className="feature-list">
      {/* Primary feature - receives highest visual priority */}
      <FeatureCard 
        title="Real-time Data"
        description="Monitor your metrics as they happen with second-by-second updates"
        icon="chart-line"
        isPrimary={true}
      />
      
      {/* Secondary features - visually subordinate to primary */}
      <div className="secondary-features">
        <FeatureCard 
          title="Custom Reports"
          description="Create tailored reports for any metric"
          icon="file-chart"
          isPrimary={false}
        />
        <FeatureCard 
          title="Data Export"
          description="Download your data in multiple formats"
          icon="download"
          isPrimary={false}
        />
      </div>
    </div>
    
    {/* Action hierarchy */}
    <div className="action-container">
      <button className="btn-primary">Get Started</button>
      <button className="btn-secondary">Watch Demo</button>
      <button className="btn-tertiary">Learn More</button>
    </div>
  </section>
);
```

### Usage Example: Cards with Visual Hierarchy

```jsx
// Card component with built-in visual hierarchy
const Card = ({ title, content, importance = "medium" }) => {
  // Map importance level to visual properties
  const styles = {
    high: {
      containerClass: "card card-primary",
      titleClass: "card-title-large",
      spacing: "card-content-spacious"
    },
    medium: {
      containerClass: "card card-secondary",
      titleClass: "card-title",
      spacing: "card-content-normal"
    },
    low: {
      containerClass: "card card-tertiary",
      titleClass: "card-title-small",
      spacing: "card-content-compact"
    }
  }[importance];
  
  return (
    <div className={styles.containerClass}>
      <h3 className={styles.titleClass}>{title}</h3>
      <div className={styles.spacing}>
        {content}
      </div>
    </div>
  );
};
```

The code examples demonstrate how to implement visual hierarchy principles in a systematic way, creating consistent relationships between elements and reinforcing their relative importance.
</context>

<context name="visual_hierarchy_anti_patterns" priority="medium">
## Anti-Patterns and Common Mistakes

### 1. Competing Focal Points

**Problem:**
Multiple elements with equal visual weight compete for attention, creating confusion about where to look first.

**Example:**
```
LARGE HEADLINE       EQUALLY LARGE GRAPHIC
                     
Bold red button      Another bold red button
```

**Why It Fails:**
- Creates visual competition and indecision
- Dilutes the impact of truly important elements
- Increases cognitive load as users must determine priority

**Better Approach:**
```
LARGE HEADLINE
[Supporting image that's clearly secondary]
                     
Bold red button      [Gray secondary button]
```

### 2. Insufficient Contrast Between Hierarchy Levels

**Problem:**
Hierarchy levels are too similar, making it difficult to distinguish between primary, secondary, and tertiary content.

**Example:**
```
Heading (18px, 500 weight)
Subheading (16px, 500 weight)
Body text (15px, 400 weight)
```

**Why It Fails:**
- Too subtle differences don't register as meaningful hierarchy
- Users struggle to understand content organization
- Important information doesn't stand out appropriately

**Better Approach:**
```
Heading (24px, 700 weight)
Subheading (18px, 600 weight)
Body text (16px, 400 weight)
```

### 3. Hierarchy Inflation ("Everything Is Important")

**Problem:**
Overusing emphasis techniques dilutes the overall hierarchy system.

**Example:**
```
BOLD LARGE HEADING
ALSO BOLD SUBHEADING
EVEN THE BODY TEXT IS BOLD
BUTTONS ARE EXTRA BOLD AND COLORFUL
```

**Why It Fails:**
- When everything is emphasized, nothing stands out
- Creates visual fatigue and overwhelm
- Defeats the purpose of hierarchy

**Better Approach:**
Reserve strong emphasis for truly important elements, and create a clear progression of visual weight.

### 4. Inconsistent Signaling

**Problem:**
Using different visual signals for elements of the same importance across an interface.

**Example:**
On one screen, primary buttons are blue; on another, they're green. Or headings use different sizes/weights across similar pages.

**Why It Fails:**
- Creates confusion about element relationships
- Increases cognitive load as users must relearn hierarchy on each screen
- Damages the predictability of the interface

**Better Approach:**
Create a consistent visual language where similar elements have the same visual treatment across the entire interface.

### 5. Hierarchy Misalignment

**Problem:**
Visual hierarchy doesn't match actual content importance.

**Example:**
Making a "Cancel" button more prominent than "Submit," or giving marketing content more visual weight than the primary user task.

**Why It Fails:**
- Misleads users about what's actually important
- Can cause task completion errors
- Creates frustration when important content is visually minimized

**Better Approach:**
Ensure visual hierarchy accurately reflects true content priorities and user task flow.
</context>

<context name="visual_hierarchy_reasoning_principles" priority="low">
## Reasoning Principles

Understanding why visual hierarchy works helps create more effective designs:

### 1. Cognitive Processing Patterns
Visual hierarchy works because it aligns with how humans naturally process visual information:

- **Pre-attentive processing:** Some visual properties (size, color, contrast) are processed automatically before conscious attention
- **Pattern recognition:** Humans quickly recognize and categorize visual patterns
- **Information chunking:** We naturally group related items to process information more efficiently

### 2. Cognitive Load Reduction
Good hierarchy reduces mental effort by:

- **Pre-organizing content:** Users don't have to sort through information mentally
- **Creating clear entry points:** Users know where to start reading/scanning
- **Establishing content relationships:** The visual system communicates how information relates

### 3. Scanning vs. Reading Behavior
Users primarily scan rather than read digital interfaces:

- **F-pattern scanning:** Western users tend to scan in an F-shaped pattern for text-heavy content
- **Z-pattern scanning:** For less dense layouts, users often follow a Z-shaped pattern
- **Visual anchoring:** Strong visual elements serve as anchors during scanning

### 4. Design Grammar Expectations
Users develop expectations about how interfaces should look:

- **Conventional patterns:** Users expect certain elements (headings, buttons) to follow standard visual patterns
- **Learned associations:** Users associate visual treatments with specific meanings or functions
- **Consistency benefits:** Following established patterns reduces learning curves

### 5. Cultural and Contextual Factors
Hierarchy interpretation varies across contexts:

- **Reading direction:** Influences natural scanning patterns (LTR vs. RTL)
- **Cultural associations:** Color and symbol meanings vary across cultures
- **Context sensitivity:** The same hierarchy might be interpreted differently based on user context and goals
</context>

<context name="visual_hierarchy_model_specific_notes" priority="low">
## Model-Specific Implementation Notes

### For Claude (Anthropic)
- Claude excels at understanding spatial relationships described in visual hierarchy
- When using Claude for design tasks, be explicit about:
  - Exact sizing relationships (e.g., "Heading is 24px, subheading is 18px")
  - Precise color values with contrast ratios
  - Detailed layout specifications with exact spacing values
- Claude can generate CSS or component code that implements visual hierarchy correctly if given specific requirements

### For GPT (OpenAI)
- GPT has strong knowledge of design principles but may need more guidance on implementation details
- When using GPT for visual hierarchy tasks:
  - Provide more examples of desired outcomes
  - Specify measurement systems and units explicitly
  - Ask for explanations of reasoning behind hierarchy choices
- GPT may suggest creative applications of visual hierarchy principles not explicitly covered in this module

### For Local Models
- Local models may have more limited understanding of nuanced design principles
- For best results with local models:
  - Focus on core hierarchy principles rather than subtle details
  - Use more code examples and fewer abstract concepts
  - Break complex hierarchy systems into simpler components
</context>

<context name="visual_hierarchy_related_concepts" priority="low">
## Related Concepts

- **Information Architecture** - The structural design of information spaces and organization of content
- **Gestalt Principles** - Psychological principles explaining how humans perceive organized patterns in visual elements
- **Typography Systems** - Structured approaches to text organization, sizing, and styling
- **Color Theory** - Study of color relationships and their application for emphasis and meaning
- **Accessibility** - Ensuring interface elements maintain sufficient contrast and distinguishability for all users
- **Responsive Design** - Adapting visual hierarchy across different screen sizes and device types
- **White Space** - Strategic use of empty space to create emphasis and organization
- **Grid Systems** - Structural frameworks that help organize content in consistent, hierarchical ways
</context>

<context name="visual_hierarchy_practical_examples" priority="medium">
## Practical Examples

### Example 1: Product Landing Page Hierarchy

**Before**: A product page with competing elements and unclear hierarchy
```
[Logo]  [Navigation]  [Search]  [Cart]

PRODUCT NAME    BUY NOW BUTTON
Product image   Product price
                IN STOCK

Product description text spanning the width of the container, with all the same
visual weight and no clear organization of information.

Features listed without any hierarchy or organization.

Related products shown with the same visual weight as main product.
```

**After**: Improved hierarchy with clear priority
```
[Logo]  [Navigation]                [Search]  [Cart]

PRODUCT NAME
[Large, prominent product image]

$199.99         [BUY NOW BUTTON]
In stock        [Add to wishlist]

Product description with key benefits highlighted.

FEATURES
• Primary feature with emphasis
• Secondary features
• Additional specifications

RELATED PRODUCTS (smaller, less prominent section)
```

### Example 2: Form Design Hierarchy

**Before**: Form with flat hierarchy
```
Create Account

Name [input field]
Email [input field]
Password [input field]
Confirm Password [input field]
Terms and Conditions [checkbox]
Subscribe to newsletter [checkbox]

[Submit] [Cancel]
```

**After**: Form with improved visual hierarchy
```
CREATE ACCOUNT

Personal Information
Name [input field]
Email [input field]

Security
Password [input field]
Confirm Password [input field]
Password must be at least 8 characters (smaller helper text)

Options
[ ] I accept the Terms and Conditions (required)
[ ] Subscribe to newsletter (optional)

[CREATE ACCOUNT] [Cancel]
```

### Example 3: Dashboard Hierarchy

**Before**: Dashboard with unclear priorities
```
[Navigation] [User menu]

Dashboard  Reports  Settings

Widget 1   Widget 2   Widget 3
Widget 4   Widget 5   Widget 6

All widgets same size, same visual weight, no clear starting point
```

**After**: Dashboard with clear hierarchy
```
[Navigation]                      [User menu]

DASHBOARD

KEY METRICS (prominent section with largest elements)
[Primary KPI widget - largest]  [Secondary KPI widget]

RECENT ACTIVITY (medium prominence)
[Timeline of user actions]

DETAILED ANALYTICS (less prominent)
[Smaller widgets with detailed information]
```

These examples demonstrate how applying visual hierarchy principles transforms unclear interfaces into structured experiences with clear guidance for users.
</context>

## Using This Module

This module can be referenced when:
- Designing new interfaces or components
- Evaluating existing designs for effectiveness
- Creating design systems with consistent hierarchy
- Implementing component libraries with proper visual relationships
- Explaining design decisions to stakeholders

Apply these principles systematically to create interfaces that naturally guide users through content and interactions in the intended sequence.

Last Updated: April 13, 2025
