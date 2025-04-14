        className="tooltip"
        initial={{ opacity: 0, y: 5 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ 
          duration: AnimationSystem.duration.short,
          ease: AnimationSystem.ease.enter
        }}
      >
        Tooltip Content
      </motion.div>
    </div>
  );
};
```

**Severity:** Medium
**AI-Specific:** No

### 5. Non-Interruptible Animations [AP-ANIM-005]

**Problem:**
Creating animations that can't be interrupted, forcing users to wait for them to complete before continuing interaction.

**Example:**
```jsx
// Non-interruptible animation
const NonInterruptible = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isAnimating, setIsAnimating] = useState(false);
  
  const toggleMenu = () => {
    if (isAnimating) return; // Prevent interaction during animation
    
    setIsAnimating(true);
    setIsOpen(!isOpen);
    
    // Force users to wait for animation to complete
    setTimeout(() => {
      setIsAnimating(false);
    }, 1000); // Long animation duration
  };
  
  return (
    <div className="dropdown">
      <button 
        onClick={toggleMenu}
        disabled={isAnimating} // Button disabled during animation
      >
        {isOpen ? 'Close' : 'Open'} Menu
      </button>
      
      <div 
        className={`menu ${isOpen ? 'open' : 'closed'}`}
        style={{
          transition: 'all 1s cubic-bezier(0.34, 1.56, 0.64, 1)'
        }}
      >
        <ul>
          <li>Option 1</li>
          <li>Option 2</li>
          <li>Option 3</li>
        </ul>
      </div>
    </div>
  );
};
```

**Why It Fails:**
- Creates frustration for users who want to interact immediately
- Reduces perceived performance of the interface
- Violates the principle that user control should take precedence
- Makes quick interactions unnecessarily slow
- Creates a poor experience for power users

**Better Approach:**
```jsx
// Interruptible animation
const Interruptible = () => {
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <div className="dropdown">
      <button onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? 'Close' : 'Open'} Menu
      </button>
      
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
            className="menu"
          >
            <ul>
              <li>Option 1</li>
              <li>Option 2</li>
              <li>Option 3</li>
            </ul>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
```

**Severity:** Medium
**AI-Specific:** No

### 6. Unmaintainable Animation Code [AP-ANIM-006]

**Problem:**
Creating animations with hardcoded values, mixed responsibilities, and poor organization, making them difficult to maintain and update.

**Example:**
```jsx
// Unmaintainable animation code
const MessyAnimations = () => {
  useEffect(() => {
    // Direct DOM manipulation mixed with animation logic
    const header = document.querySelector('.header');
    const items = document.querySelectorAll('.item');
    
    // Hardcoded values
    gsap.from(header, {
      y: -50,
      opacity: 0,
      duration: 0.75,
      ease: 'power2.out'
    });
    
    // Animations scattered throughout the component
    items.forEach((item, i) => {
      gsap.from(item, {
        opacity: 0,
        y: 20, 
        delay: 0.75 + (i * 0.125),
        duration: 0.5,
        ease: 'back.out(1.7)'
      });
    });
    
    // More unrelated animations
    gsap.to('.background', {
      opacity: 0.8,
      duration: 2,
      ease: 'none'
    });
  }, []);
  
  return (
    <div className="animated-section">
      <div className="background"></div>
      <h2 className="header">Section Title</h2>
      <div className="items">
        <div className="item">Item 1</div>
        <div className="item">Item 2</div>
        <div className="item">Item 3</div>
      </div>
      {/* More content */}
    </div>
  );
};
```

**Why It Fails:**
- Mixes animation logic with component rendering
- Uses hardcoded values that are difficult to update consistently
- Creates tight coupling between animations and DOM structure
- Makes it hard to reuse animation patterns
- Becomes increasingly complex as more animations are added

**Better Approach:**
```jsx
// Well-organized, maintainable animation code
// animation-config.js - Centralized animation settings
const animations = {
  fadeIn: {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    transition: { duration: 0.3 }
  },
  slideUp: {
    initial: { y: 20, opacity: 0 },
    animate: { y: 0, opacity: 1 },
    transition: { duration: 0.5 }
  },
  staggered: (delayChildren, staggerChildren) => ({
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    transition: {
      delayChildren,
      staggerChildren
    }
  })
};

// Animation component
const AnimatedItem = ({ children, animation = 'fadeIn', delay = 0 }) => {
  const animationProps = animations[animation];
  
  return (
    <motion.div
      {...animationProps}
      transition={{
        ...animationProps.transition,
        delay
      }}
    >
      {children}
    </motion.div>
  );
};

// Main component
const OrganizedAnimations = () => {
  return (
    <div className="animated-section">
      <AnimatedItem>
        <div className="background"></div>
      </AnimatedItem>
      
      <AnimatedItem animation="slideUp">
        <h2 className="header">Section Title</h2>
      </AnimatedItem>
      
      <motion.div
        {...animations.staggered(0.2, 0.1)}
        className="items"
      >
        {['Item 1', 'Item 2', 'Item 3'].map((text, i) => (
          <motion.div
            key={i}
            variants={animations.slideUp}
            className="item"
          >
            {text}
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
};
```

**Severity:** Medium
**AI-Specific:** Yes - AI often generates monolithic animation code
</context>

<context name="animation_reasoning_principles" priority="low">
## Reasoning Principles

### Animation Purpose Hierarchy

Animations should be prioritized according to their functional value in the interface. This hierarchy provides a framework for making decisions about which animations to implement and their relative importance:

1. **Functional Feedback** (Highest Priority)
   - Confirming user actions (button clicks, form submissions)
   - Indicating progress (loading states, progress bars)
   - Revealing system status changes (success/error messages)

2. **Spatial Orientation**
   - Establishing relationships between elements
   - Communicating hierarchy and organization
   - Maintaining context during navigation

3. **Attention Guidance**
   - Directing users to important information
   - Highlighting changes or updates
   - Indicating required actions

4. **Educational Signifiers**
   - Teaching interaction patterns
   - Demonstrating available functionalities
   - Revealing hidden features

5. **Emotional Engagement** (Lowest Priority)
   - Brand expression through motion
   - Delight and personality
   - Purely decorative animations

This hierarchy helps determine which animations should be preserved even when performance or accessibility constraints arise. Functional feedback animations should rarely be compromised, while emotional engagement animations can be reduced or eliminated when necessary.

### Perceptual Principles for Animation

Human perception of motion follows certain psychological principles that effective animation design acknowledges:

1. **Continuity**: The brain perceives continuous motion even from discrete frames, but this perception breaks down below certain thresholds (typically 24fps). Animation systems must maintain consistent frame rates to preserve the illusion of motion.

2. **Object Permanence**: Users perceive elements that transform or move as the same object if the transition is smooth and logical. This underpins the effectiveness of shared element transitions and morphing animations.

3. **Motion Anticipation**: Natural motion rarely starts at full velocity. Adding slight delays or preparatory movements before primary motion creates more natural-feeling animations.

4. **Follow-through and Overlapping Action**: Different parts of an object don't all move at the same time or stop simultaneously. Implementing subtle variations in timing creates more realistic motion.

5. **Slow In and Slow Out (Ease)**: Natural objects accelerate and decelerate rather than moving at constant velocity. This principle explains why eased animations feel more natural than linear ones.

6. **Secondary Action**: Supplementary movements that complement the primary animation enhance realism and richness (e.g., a slight rotation accompanying a scale animation).

7. **Timing and Spacing**: The speed of an animation conveys important information about the physical properties of the object being animated (weight, size, importance).

### Performance vs. Fidelity Tradeoffs

Creating performant animations often requires making tradeoffs:

1. **Property Selection Principle**: Different CSS properties have different performance characteristics:
   - Transforms and opacity can often be GPU-accelerated
   - Layout properties (height, width, top, left) are more expensive
   - Paint properties (color, background, shadows) fall in between

2. **Animation Complexity Budget**: Each page or component should have a limited "budget" for animation complexity, with more important animations allocated more of this budget.

3. **Progressive Enhancement for Animation**: Implement animations in layers of increasing complexity:
   - Base layer: Essential animations for functionality and feedback
   - Enhancement layer: Orientation and context animations
   - Enrichment layer: Delight and brand animations

4. **Device-Aware Animation Scaling**: Performance characteristics vary widely across devices. Consider:
   - Reducing animation complexity on lower-end devices
   - Adjusting animation duration based on device capabilities
   - Simplifying animations on mobile to preserve battery life

5. **Perceptual Performance Principle**: Perceived performance often matters more than actual performance. Animations can make an interface feel faster even when actual task completion time remains constant.

### Animation Ethics and Responsibility

Animation designers have ethical responsibilities to consider:

1. **Attention Respect**: Animation captures attention forcefully. Respect this power by using it judiciously and avoiding manipulative patterns.

2. **Cognitive Load Consideration**: Each animation imposes cognitive processing requirements on users. Those with cognitive disabilities may struggle with complex or numerous animations.

3. **Vestibular Sensitivity Accommodation**: People with vestibular disorders can experience physical discomfort or nausea from certain animations. Always provide reduced motion alternatives.

4. **Battery and Resource Consumption**: Animations consume device resources and battery power. Consider the environmental and access implications of animation-heavy interfaces.

5. **Cultural Variability**: Animation perception and meaning can vary across cultures. Be aware of cultural differences in how motion is interpreted.
</context>

<context name="animation_model_specific_notes" priority="low">
## Model-Specific Implementation Notes

### For Claude (Anthropic)

When working with animated web components through Claude, consider these approaches:

- Ask Claude to explain animation concepts conceptually before requesting specific code implementations
- Request code segments that focus on specific animation techniques rather than entire applications
- For complex animations, ask for step-by-step explanations alongside the code
- Use Claude's code generation capabilities for animation configuration objects and pattern templates
- Provide clear specifications about performance constraints and accessibility requirements

Example prompt:
```
Explain how to implement a reusable fade-in animation component in React using Framer Motion. 
Include customization options for duration, easing, and delay, and ensure it respects 
prefers-reduced-motion preferences. Then show how this component would be used in a typical application.
```

### For GPT (OpenAI)

When working with animated web components through GPT models, consider:

- GPT excels at generating complete, working animation examples with different libraries
- Specify the exact animation library and version you're working with
- Ask for performance optimization strategies specific to your chosen approach
- Request comparative examples when deciding between different animation techniques
- For debugging, provide GPT with the exact error messages or performance issues you're experiencing

Example prompt:
```
I'm building a React application with GSAP 3.11.5 and need to create a staggered animation
effect for a list of items that animates when they enter the viewport. Please show me
the complete implementation with performance considerations and browser compatibility notes.
```

### For Cursor AI

When working with animated web components through Cursor AI, consider:

- Use Cursor AI for real-time suggestions while writing animation code
- Leverage its code completion to suggest animation parameters and properties
- Ask for specific animation configurations rather than entire components
- Use comments to guide Cursor AI toward the animation patterns you want
- Take advantage of its ability to refactor existing animation code for better performance

Example prompt:
```
// I want to create a smooth animation for this React component
// using Framer Motion's layout animations for the height transition
// Please help me implement it with proper performance considerations
```

### For Local Models

When working with animated web components through local code models:

- Focus on simpler, more standardized animation patterns
- Provide more context about the specific animation effect you're trying to achieve
- Break down complex animation requests into smaller, more manageable parts
- Be explicit about browser compatibility requirements
- Verify generated animation code more carefully, especially for performance issues

Example prompt:
```
Show me how to create a simple CSS transition animation for a button that changes
background color, size, and shadow on hover. The animation should be smooth with
an appropriate easing function and duration.
```
</context>

<context name="animation_related_concepts" priority="low">
## Related Concepts

- **Motion Design** - The broader field of designing meaningful movement for digital interfaces, extending beyond implementation to include motion principles and psychology.

- **CSS Transitions and Animations** - Fundamental web technologies for creating simple to complex animations using purely declarative CSS.

- **WebGL and Canvas** - Lower-level graphics APIs for creating more complex visual effects and animations beyond DOM manipulation.

- **Physics-Based Animation** - Animation approach that simulates physical forces like gravity, spring tension, and friction to create natural-feeling motion.

- **Gesture Recognition** - Systems for detecting and responding to user touch and pointer inputs with appropriate animations.

- **Scroll-Driven Interactions** - Techniques for creating animations and effects that respond to user scrolling behavior.

- **3D Transformations** - Using CSS or JavaScript to create three-dimensional effects through perspective, rotation, and translation.

- **GPU Acceleration** - Leveraging the graphics processing unit to improve animation performance by offloading certain operations from the CPU.

- **Keyframe Interpolation** - The technique of calculating intermediate frames between defined keyframes in an animation sequence.

- **Animation Choreography** - Planning and coordinating multiple animations to work together harmoniously within an interface.

- **Motion Accessibility** - Practices ensuring animations don't create barriers for users with motion sensitivity, cognitive disabilities, or those using assistive technologies.

- **Micro-Interactions** - Small, focused animations that provide feedback and enhance the user experience of specific interface elements.

- **Game Animation Techniques** - Animation approaches borrowed from game development, including sprite animations, particle systems, and procedural animation.

- **SVG Animation** - Techniques specific to animating Scalable Vector Graphics, including path morphing and stroke animations.

- **FLIP Animation Technique** - First-Last-Invert-Play methodology for creating performant animations, especially for layout changes.
</context>

<context name="animation_practical_examples" priority="medium">
## Practical Examples

### Example 1: Button Loading State

**Before**: Simple button with abrupt state changes.

```jsx
// Simple button without animation
function SubmitButton({ isLoading }) {
  return (
    <button disabled={isLoading}>
      {isLoading ? 'Loading...' : 'Submit'}
    </button>
  );
}
```

**After**: Button with smooth animation between states.

```jsx
// Animated button with loading state
import { motion } from 'framer-motion';
import { useState } from 'react';

function AnimatedButton({ isLoading, onClick, children }) {
  const [isMounted, setIsMounted] = useState(true);

  // Define animation variants
  const buttonVariants = {
    idle: {
      scale: 1,
      backgroundColor: '#3498db'
    },
    loading: {
      scale: 0.98,
      backgroundColor: '#2980b9'
    }
  };

  const textVariants = {
    idle: {
      opacity: 1,
      y: 0
    },
    loading: {
      opacity: 0,
      y: 5
    }
  };

  const spinnerVariants = {
    loading: {
      opacity: 1,
      rotate: 360,
      transition: {
        rotate: {
          loop: Infinity,
          ease: "linear",
          duration: 1.5
        }
      }
    },
    idle: {
      opacity: 0,
      rotate: 0
    }
  };

  return (
    <motion.button
      disabled={isLoading}
      onClick={onClick}
      variants={buttonVariants}
      initial="idle"
      animate={isLoading ? "loading" : "idle"}
      whileHover={{ scale: isLoading ? 0.98 : 1.05 }}
      whileTap={{ scale: 0.95 }}
      className="button"
    >
      <motion.span
        variants={textVariants}
        className="button-text"
      >
        {children}
      </motion.span>
      
      <motion.svg
        variants={spinnerVariants}
        className="spinner"
        viewBox="0 0 50 50"
        width="24"
        height="24"
      >
        <circle
          cx="25"
          cy="25"
          r="20"
          fill="none"
          stroke="white"
          strokeWidth="5"
          strokeLinecap="round"
          strokeDasharray="31.4 31.4"
        />
      </motion.svg>
    </motion.button>
  );
}

// CSS
.button {
  position: relative;
  padding: 10px 24px;
  border: none;
  border-radius: 4px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  overflow: hidden;
}

.button-text {
  display: inline-block;
}

.spinner {
  position: absolute;
  top: 50%;
  left: 50%;
  margin-top: -12px;
  margin-left: -12px;
}
```

Key improvements:
- Smooth transitions between states
- Visual feedback during loading
- Multiple animation elements (button scale, color, spinner)
- Proper handling of hover and tap states
- Maintains accessibility during state changes
- Visual continuity for better user experience

### Example 2: Accordion Component

**Before**: Simple accordion with abrupt open/close behavior.

```jsx
// Basic accordion without animation
import { useState } from 'react';

function Accordion({ title, children }) {
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <div className="accordion">
      <button 
        className="accordion-header" 
        onClick={() => setIsOpen(!isOpen)}
      >
        {title}
        <span className="icon">{isOpen ? '−' : '+'}</span>
      </button>
      
      {isOpen && (
        <div className="accordion-content">
          {children}
        </div>
      )}
    </div>
  );
}
```

**After**: Accordion with smooth animation and accessibility improvements.

```jsx
// Animated accordion with accessibility features
import { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useReducedMotion } from '../hooks/useReducedMotion';

function AnimatedAccordion({ title, children, id }) {
  const [isOpen, setIsOpen] = useState(false);
  const contentRef = useRef(null);
  const prefersReducedMotion = useReducedMotion();
  
  // Generate unique IDs for accessibility
  const headerId = `accordion-header-${id}`;
  const contentId = `accordion-content-${id}`;
  
  return (
    <div className="accordion">
      <motion.button 
        className={`accordion-header ${isOpen ? 'open' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-controls={contentId}
        id={headerId}
        whileHover={{ backgroundColor: isOpen ? '#e9e9e9' : '#f5f5f5' }}
        whileTap={{ scale: 0.995 }}
      >
        {title}
        <motion.span 
          className="icon"
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ 
            duration: prefersReducedMotion ? 0 : 0.2, 
            ease: "easeInOut" 
          }}
        >
          ↓
        </motion.span>
      </motion.button>
      
      <AnimatePresence initial={false}>
        {isOpen && (
          <motion.div
            ref={contentRef}
            className="accordion-content"
            id={contentId}
            role="region"
            aria-labelledby={headerId}
            initial={{ height: 0, opacity: 0 }}
            animate={{ 
              height: 'auto', 
              opacity: 1,
              transition: {
                height: { 
                  duration: prefersReducedMotion ? 0 : 0.3
                },
                opacity: { 
                  duration: prefersReducedMotion ? 0 : 0.2,
                  delay: prefersReducedMotion ? 0 : 0.1
                }
              }
            }}
            exit={{ 
              height: 0, 
              opacity: 0,
              transition: {
                height: { 
                  duration: prefersReducedMotion ? 0 : 0.3
                },
                opacity: { 
                  duration: prefersReducedMotion ? 0 : 0.2
                }
              }
            }}
          >
            <div className="content-inner">
              {children}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

// CSS
.accordion {
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 10px;
}

.accordion-header {
  width: 100%;
  text-align: left;
  padding: 15px;
  background: #f9f9f9;
  border: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  font-weight: 600;
}

.accordion-header.open {
  border-bottom: 1px solid #eee;
}

.accordion-content {
  overflow: hidden;
}

.content-inner {
  padding: 15px;
}
```

Key improvements:
- Smooth height animation using AnimatePresence
- Proper ARIA attributes for accessibility
- Visual feedback for interactions
- Respect for reduced motion preferences
- Icon rotation animation
- Properly handled exit animations
- Focus styles and keyboard accessibility

### Example 3: Page Transition

**Before**: Abrupt page changes in a single-page application.

```jsx
// Basic router without transitions
import { Routes, Route } from 'react-router-dom';

function App() {
  return (
    <div className="app">
      <Nav />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
      </Routes>
    </div>
  );
}
```

**After**: Smooth page transitions with shared layout elements.

```jsx
// Animated page transitions
import { Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import { useReducedMotion } from '../hooks/useReducedMotion';

// Page wrapper component
const PageTransition = ({ children }) => {
  const prefersReducedMotion = useReducedMotion();
  
  const variants = {
    initial: { 
      opacity: 0,
      x: prefersReducedMotion ? 0 : 20
    },
    animate: { 
      opacity: 1,
      x: 0,
      transition: {
        duration: prefersReducedMotion ? 0 : 0.4,
        ease: "easeOut",
        when: "beforeChildren",
        staggerChildren: prefersReducedMotion ? 0 : 0.1
      }
    },
    exit: { 
      opacity: 0,
      x: prefersReducedMotion ? 0 : -20,
      transition: {
        duration: prefersReducedMotion ? 0 : 0.3,
        ease: "easeIn"
      }
    }
  };
  
  // We can create child variants for staggered animations
  const childVariants = {
    initial: { 
      opacity: 0,
      y: prefersReducedMotion ? 0 : 20
    },
    animate: { 
      opacity: 1,
      y: 0
    }
  };
  
  return (
    <motion.div
      className="page-container"
      variants={variants}
      initial="initial"
      animate="animate"
      exit="exit"
    >
      {/* Page content container */}
      <motion.div 
        className="page-content"
        variants={childVariants}
      >
        {children}
      </motion.div>
    </motion.div>
  );
};

function AnimatedApp() {
  const location = useLocation();
  
  return (
    <div className="app">
      <Nav /> {/* Nav stays fixed across routes */}
      
      <AnimatePresence mode="wait">
        <Routes location={location} key={location.pathname}>
          <Route path="/" element={
            <PageTransition>
              <Home />
            </PageTransition>
          } />
          <Route path="/about" element={
            <PageTransition>
              <About />
            </PageTransition>
          } />
          <Route path="/contact" element={
            <PageTransition>
              <Contact />
            </PageTransition>
          } />
        </Routes>
      </AnimatePresence>
    </div>
  );
}

// CSS
.app {
  position: relative;
  overflow-x: hidden; /* Prevent horizontal scrollbars during animation */
}

.page-container {
  position: relative;
  width: 100%;
}
```

Key improvements:
- Smooth transitions between pages
- Consistent animation pattern for better predictability
- Staggered animation for page elements
- Exit animations for departing pages
- Respect for reduced motion preferences
- Maintained layout elements between page transitions
- Proper handling of route changes with keys
</context>

## Using This Module

This animated web components module can be referenced when:
- Designing and implementing animations for web applications
- Selecting appropriate animation libraries and techniques
- Optimizing animation performance
- Ensuring animations are accessible to all users
- Creating consistent motion design systems
- Troubleshooting animation issues
- Implementing specific animation patterns

The core concepts to focus on when working with animated web components are:
1. Purpose-driven animation that enhances rather than distracts
2. Performance optimization to maintain smooth 60fps animations
3. Accessibility considerations including respecting reduced motion preferences
4. Consistency in timing, easing, and animation patterns
5. State-based animation design for predictable user experiences

Remember that effective animations serve a purpose beyond decoration - they provide feedback, guide attention, explain relationships, and enhance engagement. By following the principles and patterns in this module, you can create animations that improve your application's user experience while maintaining performance and accessibility.

Last Updated: April 14, 2025

</context>

<context name="animation_libraries_comparison" priority="medium">
## Animation Libraries Comparison

Different animation libraries offer unique advantages for specific use cases. Here's a comparison of popular options:

### Framer Motion

Framer Motion is a React-specific animation library focused on declarative animations with an intuitive API.

**Strengths:**
- Seamless React integration with hooks and components
- Excellent for UI transitions and gesture-based interactions
- Built-in accessibility features (reduced motion)
- Powerful layout animations and shared element transitions
- Small bundle size compared to more comprehensive libraries

**Limitations:**
- React-only (not suitable for vanilla JavaScript projects)
- Less suitable for complex timeline animations
- Limited control over GPU optimization compared to GSAP

**Ideal for:**
- React applications with component-based animations
- Responsive interfaces with gesture support
- Teams looking for a declarative, component-oriented API

**Example Implementation:**
```jsx
import { motion } from 'framer-motion';

const TabContent = ({ isVisible, children }) => {
  return (
    <motion.div
      initial={{ opacity: 0, height: 0 }}
      animate={{ 
        opacity: isVisible ? 1 : 0,
        height: isVisible ? 'auto' : 0
      }}
      transition={{
        opacity: { duration: 0.3 },
        height: { duration: 0.4, ease: 'easeInOut' }
      }}
      style={{ overflow: 'hidden' }}
    >
      {children}
    </motion.div>
  );
};
```

### GSAP (GreenSock Animation Platform)

GSAP is a robust, framework-agnostic animation library with exceptional performance and flexibility.

**Strengths:**
- Framework-agnostic (works with any JavaScript project)
- Superior performance, especially for complex animations
- Advanced timeline control for sequencing animations
- Rich ecosystem of plugins (ScrollTrigger, Draggable, MorphSVG)
- Precise control over every aspect of animation

**Limitations:**
- Steeper learning curve compared to simpler libraries
- Imperative API that can be verbose
- Larger bundle size (though modular loading is possible)
- Commercial licensing for some advanced plugins

**Ideal for:**
- Complex, timeline-based animations
- Scroll-triggered effects and parallax
- Projects requiring cross-browser consistency
- SVG and canvas animations

**Example Implementation:**
```jsx
import { useRef, useEffect } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

// Register plugins
gsap.registerPlugin(ScrollTrigger);

const ScrollAnimation = () => {
  const sectionRef = useRef(null);
  const headingRef = useRef(null);
  const paragraphRef = useRef(null);
  
  useEffect(() => {
    const section = sectionRef.current;
    const heading = headingRef.current;
    const paragraph = paragraphRef.current;
    
    // Create timeline for sequenced animations
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: section,
        start: 'top 80%',
        end: 'bottom 20%',
        scrub: true,
        markers: false
      }
    });
    
    // Add animations to timeline
    tl.fromTo(heading, 
      { opacity: 0, y: 50 },
      { opacity: 1, y: 0, duration: 0.5 }
    ).fromTo(paragraph,
      { opacity: 0, y: 30 },
      { opacity: 1, y: 0, duration: 0.5 },
      '-=0.3' // Overlap with previous animation
    );
    
    // Cleanup
    return () => {
      if (tl.scrollTrigger) {
        tl.scrollTrigger.kill();
      }
      tl.kill();
    };
  }, []);
  
  return (
    <section ref={sectionRef} className="scroll-section">
      <h2 ref={headingRef}>Animated Section</h2>
      <p ref={paragraphRef}>
        This content animates as you scroll down the page.
      </p>
    </section>
  );
};
```

### React Spring

React Spring focuses on spring physics-based animations for natural motion, with hooks for React applications.

**Strengths:**
- Physics-based spring animations feel natural
- React hooks-based API (useSpring, useSprings, etc.)
- Declarative and imperative control options
- Good performance characteristics
- Solid TypeScript support

**Limitations:**
- React-only
- Limited built-in effects compared to GSAP
- Spring configuration can be challenging to master
- Less suitable for complex timelines

**Ideal for:**
- Interactive, gesture-driven interfaces
- Natural-feeling motion effects
- Teams comfortable with React hooks
- Drag, swipe, and pull interactions

**Example Implementation:**
```jsx
import { useSpring, animated } from 'react-spring';
import { useState } from 'react';

const ExpandableCard = () => {
  const [expanded, setExpanded] = useState(false);
  
  const springProps = useSpring({
    height: expanded ? 300 : 100,
    padding: expanded ? 30 : 15,
    backgroundColor: expanded 
      ? 'rgba(65, 105, 225, 0.8)' 
      : 'rgba(65, 105, 225, 0.4)',
    config: {
      tension: 280,
      friction: 20
    }
  });
  
  return (
    <animated.div 
      style={springProps}
      className="card"
      onClick={() => setExpanded(!expanded)}
    >
      <h3>Click to {expanded ? 'Collapse' : 'Expand'}</h3>
      {expanded && (
        <p>This content only appears when the card is expanded.</p>
      )}
    </animated.div>
  );
};
```

### Three.js and React Three Fiber

For 3D web animations, Three.js is the industry standard, with React Three Fiber providing React bindings.

**Strengths:**
- Full 3D animation capabilities
- WebGL rendering for hardware acceleration
- Extensive ecosystem and community
- React Three Fiber provides declarative React integration
- Capable of immersive experiences and visualizations

**Limitations:**
- Steep learning curve (requires 3D concepts understanding)
- Performance considerations for mobile devices
- Potentially large bundle size
- Complex setup for basic effects

**Ideal for:**
- 3D product showcases
- Data visualizations
- Interactive experiences
- Creative websites and portfolios

**Example Implementation:**
```jsx
import { Canvas, useFrame } from '@react-three/fiber';
import { useRef, useState } from 'react';
import { OrbitControls } from '@react-three/drei';

function RotatingCube(props) {
  const meshRef = useRef();
  const [hovered, setHover] = useState(false);
  const [active, setActive] = useState(false);
  
  // Animate on each frame
  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.rotation.x += 0.01;
      meshRef.current.rotation.y += 0.01;
    }
  });
  
  return (
    <mesh
      {...props}
      ref={meshRef}
      scale={active ? 1.5 : 1}
      onClick={() => setActive(!active)}
      onPointerOver={() => setHover(true)}
      onPointerOut={() => setHover(false)}
    >
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color={hovered ? 'hotpink' : 'orange'} />
    </mesh>
  );
}

const ThreeDScene = () => {
  return (
    <div className="canvas-container">
      <Canvas>
        <ambientLight intensity={0.5} />
        <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
        <pointLight position={[-10, -10, -10]} />
        <RotatingCube position={[0, 0, 0]} />
        <OrbitControls />
      </Canvas>
    </div>
  );
};
```

### Choosing the Right Animation Library

When selecting an animation library, consider these factors:

1. **Framework Compatibility**: Is it designed for your framework (React, Vue, etc.)?
2. **Animation Complexity**: Simple transitions vs. complex sequences
3. **Performance Requirements**: Mobile support, animation frequency
4. **Developer Experience**: Learning curve and API preferences
5. **Bundle Size Constraints**: Impact on application load times
6. **Animation Types**: 2D, 3D, SVG, DOM elements
7. **Special Requirements**: Scroll effects, physics, gestures

Here's a decision matrix to help choose:

| Requirement | Framer Motion | GSAP | React Spring | Three.js |
|-------------|---------------|------|--------------|----------|
| React Integration | Excellent | Good | Excellent | Good (with R3F) |
| Bundle Size | Moderate | Larger | Moderate | Large |
| Learning Curve | Low | Medium-High | Medium | High |
| Animation Complexity | Medium | High | Medium | Very High |
| Performance | Good | Excellent | Good | Varies |
| Gesture Support | Excellent | Requires Plugin | Good | Limited |
| 3D Capabilities | Limited | Limited | Limited | Excellent |
| Framework Agnostic | No | Yes | No | Yes |
</context>

<context name="animation_decision_logic" priority="medium">
## Decision Logic

When implementing animated components, use these decision frameworks to guide your approach:

### Choosing Animation Technique

```
What type of animation do you need?
├── Simple State Transitions (hover, active, etc.)
│   ├── Limited to 2-3 properties → CSS Transitions
│   └── Complex property changes → CSS Animations or React library
│
├── Entrance/Exit Animations
│   ├── React components → Framer Motion or React Transition Group
│   ├── Simple fade/slide effects → CSS Animations
│   └── Complex choreography → GSAP
│
├── Interactive/Gesture-based
│   ├── React app → Framer Motion
│   ├── Complex physics → React Spring
│   └── Framework-agnostic → GSAP + Draggable plugin
│
├── Scroll-based Animations
│   ├── Simple parallax/reveal → CSS Scroll-driven animations
│   ├── Complex scroll effects → GSAP ScrollTrigger
│   └── Scroll-linked animations → Intersection Observer + animation library
│
├── SVG Animations
│   ├── Simple path animations → CSS animations
│   ├── Complex path morphing → GSAP MorphSVG
│   └── Interactive SVG → Framer Motion or GSAP
│
└── 3D Animations
    ├── Simple 3D transforms → CSS 3D transforms
    ├── Complex 3D scenes → Three.js
    └── React 3D → React Three Fiber
```

### Performance Optimization Strategy

```
What performance concerns do you have?
├── Animation Jank/Stuttering
│   ├── Animate only transform and opacity properties
│   ├── Use will-change only when necessary
│   ├── Move animations off the main thread (CSS when possible)
│   └── Implement throttling/debouncing for scroll animations
│
├── Initial Load Performance
│   ├── Lazy load animation libraries
│   ├── Split code by route/component
│   ├── Avoid animations during initial page load
│   └── Consider critical path rendering
│
├── Battery Usage Concerns
│   ├── Pause animations when page is not visible
│   ├── Respect prefers-reduced-motion
│   ├── Reduce animation complexity for mobile
│   └── Use efficient requestAnimationFrame scheduling
│
├── Memory Usage
│   ├── Clean up animation instances on component unmount
│   ├── Cancel running animations when components update
│   ├── Reuse animation objects when possible
│   └── Avoid creating new functions in render
│
└── CPU Usage
    ├── Batch DOM reads/writes
    ├── Use GPU-accelerated properties
    ├── Implement FLIP technique for layout animations
    └── Consider canvas-based animations for many elements
```

### Accessibility Considerations

```
How can you ensure animations are accessible?
├── Motion Sensitivity
│   ├── Always implement prefers-reduced-motion media query
│   ├── Provide static alternatives for critical content
│   ├── Avoid excessive or unnecessary motion
│   └── Test with motion reduction settings enabled
│
├── Screen Reader Compatibility
│   ├── Avoid animations that impact focus order
│   ├── Ensure animations don't hide focusable content
│   ├── Use appropriate ARIA attributes for animated states
│   └── Test with screen readers during animation sequences
│
├── Cognitive Load
│   ├── Keep animations simple and purposeful
│   ├── Avoid multiple simultaneous animations
│   ├── Ensure animations complete in reasonable time
│   └── Provide user controls to pause/disable animations
│
└── Timing and Control
    ├── Allow sufficient time to read content before animating
    ├── Provide options to replay or review animated content
    ├── Enable keyboard control for interactive animations
    └── Consider alternative (non-animated) paths for critical tasks
```

### Animation Timing Selection

```
What timing parameters should you use?
├── Duration
│   ├── Micro-interactions (button effects) → 100-200ms
│   ├── UI transitions (panels, modals) → 200-300ms
│   ├── Page transitions → 300-500ms
│   └── Storytelling animations → 500ms+
│
├── Easing
│   ├── Element appearing → ease-out
│   ├── Element disappearing → ease-in
│   ├── Continuous/looping → linear
│   ├── Natural/playful motion → spring physics
│   └── Bounce/elastic effects → custom cubic-bezier curves
│
├── Delay
│   ├── Related elements → 50-100ms stagger
│   ├── Sequential steps → 100-300ms between steps
│   ├── Page load animations → 200-500ms after content loaded
│   └── Hover intent → 50-100ms to prevent accidental triggers
│
└── Sequence Choreography
    ├── Parent-child relationships → Parent before children
    ├── Information hierarchy → Important content first
    ├── User attention flow → Follow reading/scanning patterns
    └── Causal relationships → Cause before effect
```
</context>

<context name="animation_anti_patterns" priority="medium">
## Anti-Patterns and Common Mistakes

### 1. Excessive Animation [AP-ANIM-001]

**Problem:**
Overusing animations throughout an interface, creating visual noise and potentially disorienting or distracting users.

**Example:**
```jsx
// Too many simultaneous animations
const OveranimatedComponent = () => {
  return (
    <div className="card">
      <img className="floating-image" src="image.jpg" alt="Product" />
      <h2 className="pulsing-title">Product Name</h2>
      <p className="typing-text">Product description that types out letter by letter</p>
      <div className="spinning-badge">New!</div>
      <button className="wobbling-button">Add to Cart</button>
      <div className="scrolling-reviews">
        {/* Automatically scrolling reviews */}
      </div>
      <div className="particle-background">
        {/* Background with floating particles */}
      </div>
    </div>
  );
};
```

**Why It Fails:**
- Creates cognitive overload for users
- Distracts from important content and actions
- Can cause accessibility issues for users with vestibular disorders
- Negatively affects performance and battery life
- Creates a chaotic, unprofessional user experience

**Better Approach:**
```jsx
// Focused, purposeful animations
const BalancedComponent = () => {
  const [isHovered, setIsHovered] = useState(false);
  
  return (
    <div 
      className="card"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <img src="image.jpg" alt="Product" />
      <h2>Product Name</h2>
      <p>Product description that's clear and readable</p>
      {/* Single purposeful animation */}
      <motion.div 
        className="badge"
        animate={{ 
          scale: isHovered ? 1.1 : 1,
        }}
        transition={{ duration: 0.2 }}
      >
        New!
      </motion.div>
      <button className="button">Add to Cart</button>
    </div>
  );
};
```

**Severity:** High
**AI-Specific:** Yes - AI often generates decorative animations without considering their combined impact

### 2. Animation Performance Neglect [AP-ANIM-002]

**Problem:**
Creating animations that trigger expensive browser operations like layout and paint, causing jank and poor performance.

**Example:**
```jsx
// Performance-intensive animation
const PerformanceProblem = () => {
  const [position, setPosition] = useState(0);
  
  useEffect(() => {
    const interval = setInterval(() => {
      // Animating position with left/top triggers layout recalculation
      setPosition(prev => (prev + 1) % 100);
    }, 16); // ~60fps
    
    return () => clearInterval(interval);
  }, []);
  
  return (
    <div className="container">
      <div 
        className="animated-element"
        style={{
          left: `${position}px`,
          top: `${position / 2}px`,
          width: `${100 + position}px`,
          height: `${50 + position / 2}px`,
          // These properties trigger layout, paint, and composite
        }}
      >
        Animated Content
      </div>
    </div>
  );
};
```

**Why It Fails:**
- Triggers browser layout recalculation on every frame
- Causes browser repaints, which are expensive operations
- Creates visible stuttering on lower-end devices
- Drains battery on mobile devices
- Can make the entire page unresponsive

**Better Approach:**
```jsx
// Performance-optimized animation
const PerformanceOptimized = () => {
  const [position, setPosition] = useState(0);
  
  useEffect(() => {
    const element = document.querySelector('.animated-element');
    
    // Use requestAnimationFrame for smoother animation
    let animationFrame;
    const animate = () => {
      setPosition(prev => (prev + 1) % 100);
      animationFrame = requestAnimationFrame(animate);
    };
    
    animationFrame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animationFrame);
  }, []);
  
  return (
    <div className="container">
      <div 
        className="animated-element"
        style={{
          // Using transform instead of left/top
          transform: `translate(${position}px, ${position / 2}px) scale(${1 + position / 100})`,
          // transform only triggers compositing, not layout or paint
        }}
      >
        Animated Content
      </div>
    </div>
  );
};

// CSS
.animated-element {
  will-change: transform; /* Hint for browser optimization */
}
```

**Severity:** High
**AI-Specific:** Yes - AI often doesn't consider performance implications of animation choices

### 3. Ignoring Motion Preferences [AP-ANIM-003]

**Problem:**
Failing to respect users' motion preferences, potentially causing discomfort or accessibility issues for those with vestibular disorders or motion sensitivity.

**Example:**
```jsx
// Not respecting motion preferences
const MotionSensitiveComponent = () => {
  return (
    <div className="parallax-section">
      {/* Automatic parallax without respecting user preferences */}
      <div className="parallax-layer" style={{ animation: 'float 3s infinite' }}>
        Layer 1
      </div>
      <div className="parallax-layer" style={{ animation: 'float 4s infinite' }}>
        Layer 2
      </div>
      <div className="parallax-layer" style={{ animation: 'float 5s infinite' }}>
        Layer 3
      </div>
    </div>
  );
};
```

**Why It Fails:**
- Ignores accessibility needs for users with vestibular disorders
- Can cause motion sickness for sensitive users
- Fails to comply with WCAG guidelines
- Creates a poor experience for users who prefer reduced motion
- May be legally problematic in some jurisdictions

**Better Approach:**
```jsx
// Respecting motion preferences
import { useReducedMotion } from 'framer-motion';

const AccessibleMotionComponent = () => {
  // React hook to detect prefers-reduced-motion
  const prefersReducedMotion = useReducedMotion();
  
  return (
    <div className="parallax-section">
      {/* Conditional animation based on user preferences */}
      <motion.div
        className="parallax-layer"
        animate={{ 
          y: prefersReducedMotion ? 0 : [0, -10, 0],
        }}
        transition={
          prefersReducedMotion ? 
          { duration: 0 } : 
          { duration: 3, repeat: Infinity, ease: "easeInOut" }
        }
      >
        Layer 1
      </motion.div>
      {/* Additional layers following the same pattern */}
    </div>
  );
};

// For CSS-only approach:
/*
@media (prefers-reduced-motion: reduce) {
  .parallax-layer {
    animation: none !important;
    transform: none !important;
  }
}
*/
```

**Severity:** High
**AI-Specific:** Yes - AI often overlooks accessibility considerations

### 4. Animation Timing Inconsistency [AP-ANIM-004]

**Problem:**
Using inconsistent animation timing, easing, and duration throughout an interface, creating a disjointed and unprofessional user experience.

**Example:**
```jsx
// Inconsistent animation timing
const InconsistentAnimations = () => {
  return (
    <div className="interface">
      <button className="button button-primary" 
        style={{ transition: 'all 0.2s linear' }}>
        Primary Button
      </button>
      
      <button className="button button-secondary" 
        style={{ transition: 'all 0.5s ease-in-out' }}>
        Secondary Button
      </button>
      
      <motion.div 
        className="card"
        animate={{ scale: 1.05 }}
        transition={{ duration: 0.3, ease: 'easeOut' }}
      >
        Card Content
      </motion.div>
      
      <div className="tooltip" 
        style={{ animationDuration: '0.15s', animationTimingFunction: 'cubic-bezier(0.4, 0, 1, 1)' }}>
        Tooltip Content
      </div>
    </div>
  );
};
```

**Why It Fails:**
- Creates a disjointed user experience
- Fails to establish a coherent motion design language
- Makes the interface feel unprofessional and inconsistent
- Increases development complexity and maintenance burden
- Hinders user's ability to build a mental model of interface behavior

**Better Approach:**
```jsx
// Consistent animation system
const AnimationSystem = {
  duration: {
    short: 0.15,
    medium: 0.3,
    long: 0.5
  },
  ease: {
    enter: [0.0, 0.0, 0.2, 1],  // ease-out
    exit: [0.4, 0.0, 1, 1],     // ease-in
    standard: [0.4, 0.0, 0.2, 1] // ease-in-out
  }
};

const ConsistentAnimations = () => {
  return (
    <div className="interface">
      <motion.button 
        className="button button-primary"
        whileHover={{ scale: 1.05 }}
        transition={{ 
          duration: AnimationSystem.duration.short,
          ease: AnimationSystem.ease.standard
        }}
      >
        Primary Button
      </motion.button>
      
      <motion.button 
        className="button button-secondary"
        whileHover={{ scale: 1.05 }}
        transition={{ 
          duration: AnimationSystem.duration.short,
          ease: AnimationSystem.ease.standard
        }}
      >
        Secondary Button
      </motion.button>
      
      <motion.div 
        className="card"
        whileHover={{ scale: 1.02 }}
        transition={{ 
          duration: AnimationSystem.duration.medium,
          ease: AnimationSystem.ease.standard
        }}
      >
        Card Content
      </motion.div>
      
      <motion.div 
        className="tooltip"
        initial={{ opacity: 0# Animated Web Components

> A comprehensive guide to creating engaging, performant, and accessible animations for modern web applications.

## Metadata
- **Priority:** high
- **Domain:** development
- **Target Models:** claude, gpt, cursor-ai
- **Related Modules:** web-development, react-components, performance-optimization, accessibility

## Module Overview
This module explores the principles, techniques, and libraries for creating animated web components, with a focus on React-based implementations and current best practices for performance, accessibility, and user experience.

<context name="animation_principles_definition" priority="high">
## Conceptual Foundation

### What Are Animated Web Components?

Animated web components are interactive UI elements that incorporate motion design to enhance user experience, guide attention, provide feedback, and create engaging interfaces. These components use various animation techniques to transition between states, respond to user interactions, or convey information through motion.

Modern web animation encompasses several key approaches:

1. **CSS Animations and Transitions**: Declarative animations defined in stylesheets
2. **JavaScript Animation Libraries**: Programmatic control of animations using specialized libraries
3. **Web Animations API (WAAPI)**: Native browser API for controlling animations
4. **SVG Animations**: Vector-based animations for scalable graphics
5. **Canvas and WebGL**: Advanced graphics rendering for complex animations
6. **3D Animations**: Three-dimensional motion effects for immersive experiences

Animations serve several critical functions in modern interfaces:

- **Providing feedback**: Confirming user actions through visual responses
- **Guiding attention**: Directing users to important elements or changes
- **Explaining relationships**: Showing how elements relate to each other
- **Enhancing engagement**: Creating delightful, memorable experiences
- **Communicating brand identity**: Expressing personality through motion
- **Improving perceived performance**: Making waiting times feel shorter

Effective animated components balance aesthetics with functionality, performance, and accessibility to create experiences that enhance rather than detract from the user's goals.
</context>

<context name="animation_core_principles" priority="high">
## Core Principles

### 1. Purpose-Driven Animation

**Principle:** Every animation should serve a clear purpose that enhances the user experience rather than being purely decorative.

**Implementation Guidelines:**
- Begin by identifying the specific problem an animation will solve
- Ensure animations communicate information or guide users
- Test whether the animation improves or hinders task completion
- Use motion to reinforce your application's information hierarchy
- Avoid animations that distract from core functionality

**Example:**
```jsx
// ❌ Animation without clear purpose
const Decorative = () => {
  return (
    <div className="card" 
      style={{
        animation: "spin 2s linear infinite"
      }}>
      User Profile
    </div>
  );
};

// ✅ Purpose-driven animation providing feedback
const FeedbackButton = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  return (
    <button 
      className={`submit-button ${isSubmitting ? 'submitting' : ''}`}
      onClick={() => {
        setIsSubmitting(true);
        submitForm().finally(() => setIsSubmitting(false));
      }}
    >
      {isSubmitting ? 'Submitting...' : 'Submit'}
    </button>
  );
};
```

### 2. Performance Optimization

**Principle:** Animations should be optimized to run smoothly at 60fps without causing layout thrashing, excessive resource consumption, or battery drain.

**Implementation Guidelines:**
- Prioritize properties that only affect compositing (transform, opacity)
- Avoid animating properties that trigger layout (width, height, left, top)
- Use hardware acceleration through transform: translateZ(0) or will-change
- Implement throttling and debouncing for scroll or resize-based animations
- Test animations on low-powered devices to ensure wide compatibility
- Reduce JavaScript animation overhead when CSS can achieve the same effect

**Example:**
```jsx
// ❌ Performance-intensive animation
const BadPerformance = () => {
  const [size, setSize] = useState(100);
  
  useEffect(() => {
    const interval = setInterval(() => {
      // Causes layout thrashing
      setSize(prev => prev < 200 ? prev + 1 : 100);
    }, 16);
    return () => clearInterval(interval);
  }, []);
  
  return (
    <div style={{ 
      width: `${size}px`, 
      height: `${size}px`,
      left: `${size}px`,
      position: 'absolute',
      background: 'red'
    }} />
  );
};

// ✅ Performance-optimized animation
const GoodPerformance = () => {
  const [animated, setAnimated] = useState(false);
  
  return (
    <div 
      className={`box ${animated ? 'animated' : ''}`}
      onClick={() => setAnimated(!animated)}
    />
  );
};

// CSS
.box {
  width: 100px;
  height: 100px;
  background: red;
  transform: translateZ(0); /* Hardware acceleration */
  transition: transform 0.3s ease-out;
}

.box.animated {
  transform: scale(2) translateZ(0);
}
```

### 3. Animation Timing and Easing

**Principle:** Natural, well-timed animations with appropriate easing functions create more intuitive and pleasing user experiences.

**Implementation Guidelines:**
- Use ease-out for entering elements (fast start, slow end)
- Use ease-in for exiting elements (slow start, fast end)
- Implement ease-in-out for elements that both enter and exit
- Keep most UI animations between 200-500ms duration
- Use spring physics for interactive elements that respond to user input
- Create a consistent timing system across your application

**Example:**
```jsx
// Using consistent timing variables
const timing = {
  fast: 150,
  medium: 300,
  slow: 500
};

const easing = {
  enter: 'cubic-bezier(0.0, 0.0, 0.2, 1)', // ease-out
  exit: 'cubic-bezier(0.4, 0.0, 1, 1)',    // ease-in
  standard: 'cubic-bezier(0.4, 0.0, 0.2, 1)' // ease-in-out
};

// React component with proper timing and easing
const AnimatedModal = ({ isOpen, onClose, children }) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ 
        opacity: isOpen ? 1 : 0,
        transition: { 
          duration: timing.medium / 1000, 
          ease: isOpen ? easing.enter : easing.exit 
        }
      }}
      className="modal-backdrop"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ 
          scale: isOpen ? 1 : 0.8,
          opacity: isOpen ? 1 : 0, 
          transition: { 
            duration: timing.medium / 1000, 
            ease: isOpen ? easing.enter : easing.exit 
          }
        }}
        className="modal-content"
        onClick={e => e.stopPropagation()}
      >
        {children}
      </motion.div>
    </motion.div>
  );
};
```

### 4. Animation Accessibility

**Principle:** Animations must be accessible to all users, including those with vestibular disorders, motion sensitivity, or those using assistive technologies.

**Implementation Guidelines:**
- Honor user motion preferences with the prefers-reduced-motion media query
- Provide alternative static states for critical animated content
- Ensure animations don't interfere with screen readers
- Avoid rapid flashing or strobing effects (3 flashes per second or less)
- Make interactive animations keyboard accessible
- Maintain sufficient color contrast throughout animation states

**Example:**
```jsx
// Respecting user motion preferences
import { useReducedMotion } from 'framer-motion';

const AccessibleAnimation = () => {
  // Hook detects prefers-reduced-motion setting
  const prefersReducedMotion = useReducedMotion();
  
  return (
    <motion.div
      animate={{ 
        x: 100,
        // Skip animation if user prefers reduced motion
        transition: {
          duration: prefersReducedMotion ? 0 : 0.5
        } 
      }}
    >
      Animated Content
    </motion.div>
  );
};

// CSS approach
@media (prefers-reduced-motion: reduce) {
  .animated-element {
    /* Disable animations */
    animation: none !important;
    transition: none !important;
  }
}
```

### 5. Animation Consistency

**Principle:** Consistent animation patterns create a cohesive experience and reduce cognitive load by establishing predictable motion behaviors.

**Implementation Guidelines:**
- Create a motion design system with reusable animation patterns
- Establish consistent timing, easing, and distance values
- Use similar animations for similar actions across the application
- Document animation standards for team-wide implementation
- Create reusable animation components and hooks
- Maintain predictable cause-and-effect relationships

**Example:**
```jsx
// Animation design system
const animations = {
  fadeIn: {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    transition: { duration: 0.3, ease: 'easeOut' }
  },
  slideIn: {
    initial: { x: -20, opacity: 0 },
    animate: { x: 0, opacity: 1 },
    transition: { duration: 0.4, ease: 'easeOut' }
  },
  scale: {
    initial: { scale: 0.9, opacity: 0 },
    animate: { scale: 1, opacity: 1 },
    transition: { duration: 0.3, ease: [0.175, 0.885, 0.32, 1.275] }
  }
};

// Reusable animation component
const Animate = ({ children, type = 'fadeIn', delay = 0 }) => {
  const animation = animations[type];
  
  return (
    <motion.div
      initial={animation.initial}
      animate={animation.animate}
      transition={{
        ...animation.transition,
        delay
      }}
    >
      {children}
    </motion.div>
  );
};

// Usage
const Page = () => (
  <>
    <Animate type="fadeIn">
      <Header />
    </Animate>
    <Animate type="slideIn" delay={0.1}>
      <MainContent />
    </Animate>
    <Animate type="scale" delay={0.2}>
      <Footer />
    </Animate>
  </>
);
```

### 6. State-Based Animation Design

**Principle:** Design animations around component states to create predictable, manageable transitions between different visual representations.

**Implementation Guidelines:**
- Identify all possible states a component can have
- Define clear transitions between each state pair
- Ensure each state is visually distinct but connected by animation
- Handle interrupted animations gracefully
- Consider animation choreography for multiple state changes
- Use finite state machines for complex animation sequences

**Example:**
```jsx
// Button with multiple states and animations
const SubmitButton = () => {
  // Define possible states
  const [state, setState] = useState('idle');
  // idle -> loading -> success/error -> idle
  
  const handleClick = async () => {
    setState('loading');
    try {
      await submitForm();
      setState('success');
      setTimeout(() => setState('idle'), 2000);
    } catch (error) {
      setState('error');
      setTimeout(() => setState('idle'), 2000);
    }
  };
  
  // Animation variants for each state
  const variants = {
    idle: { scale: 1, backgroundColor: '#3498db' },
    loading: { scale: 0.95, backgroundColor: '#3498db' },
    success: { scale: 1.05, backgroundColor: '#2ecc71' },
    error: { scale: 1, backgroundColor: '#e74c3c' }
  };
  
  return (
    <motion.button
      animate={state}
      variants={variants}
      transition={{ duration: 0.3 }}
      onClick={handleClick}
      disabled={state !== 'idle'}
    >
      {state === 'idle' && 'Submit'}
      {state === 'loading' && 'Submitting...'}
      {state === 'success' && 'Success!'}
      {state === 'error' && 'Try Again'}
    </motion.button>
  );
};
```
</context>

<context name="animation_implementation_patterns" priority="medium">
## Implementation Patterns

### CSS Animation Patterns

CSS provides powerful, declarative ways to create animations with minimal JavaScript overhead.

#### Transition Pattern

The simplest form of CSS animation, transitions interpolate between property values based on state changes.

```css
.button {
  background-color: blue;
  transform: scale(1);
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.button:hover {
  background-color: darkblue;
  transform: scale(1.05);
}
```

```jsx
// React implementation
import { useState } from 'react';
import './button-styles.css';

const TransitionButton = () => {
  const [isActive, setIsActive] = useState(false);
  
  return (
    <button 
      className={`button ${isActive ? 'active' : ''}`}
      onClick={() => setIsActive(!isActive)}
    >
      Click Me
    </button>
  );
};
```

#### Keyframe Animation Pattern

For more complex animations with multiple steps, CSS keyframes provide fine-grained control.

```css
@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.7;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.notification {
  animation: pulse 2s infinite;
}

/* Respect user preferences */
@media (prefers-reduced-motion: reduce) {
  .notification {
    animation: none;
  }
}
```

```jsx
// React implementation
const Notification = ({ count }) => {
  return (
    <div className="icon-wrapper">
      <svg className="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
        <path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6v-5c0-3.07-1.63-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.64 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2zm-2 1H8v-6c0-2.48 1.51-4.5 4-4.5s4 2.02 4 4.5v6z"/>
      </svg>
      {count > 0 && <span className="notification">{count}</span>}
    </div>
  );
};
```

#### Scroll-Driven Animation Pattern

Modern CSS now supports scroll-driven animations, allowing elements to animate based on scroll position.

```css
@keyframes reveal {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.scroll-reveal {
  view-timeline: --reveal-timeline block;
  animation: reveal linear both;
  animation-timeline: --reveal-timeline;
  animation-range: entry 10% cover 30%;
}
```

```jsx
// React implementation with fallback for browsers without support
import { useInView } from 'react-intersection-observer';

const ScrollReveal = ({ children }) => {
  // Check for scroll-driven animation support
  const supportsScrollTimeline = CSS.supports('animation-timeline: scroll()');
  
  // Fallback for browsers without support
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });
  
  if (supportsScrollTimeline) {
    return <div className="scroll-reveal">{children}</div>;
  }
  
  // Fallback implementation
  return (
    <div 
      ref={ref} 
      className={`reveal-fallback ${inView ? 'visible' : ''}`}
    >
      {children}
    </div>
  );
};
```

### React Animation Patterns

React's component model offers unique approaches to animation through state management and component lifecycle.

#### Mount/Unmount Animation Pattern

Using Framer Motion to animate components as they enter or leave the DOM.

```jsx
import { AnimatePresence, motion } from 'framer-motion';

const Modal = ({ isOpen, onClose, children }) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="modal-backdrop"
        >
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 50, opacity: 0 }}
            transition={{ type: 'spring', damping: 25 }}
            className="modal-content"
          >
            <button onClick={onClose}>Close</button>
            {children}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
```

#### List Animation Pattern

Animating items within a list, including additions and removals.

```jsx
import { AnimatePresence, motion } from 'framer-motion';

const AnimatedList = ({ items }) => {
  return (
    <ul className="list-container">
      <AnimatePresence>
        {items.map((item) => (
          <motion.li
            key={item.id}
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
            className="list-item"
          >
            {item.content}
          </motion.li>
        ))}
      </AnimatePresence>
    </ul>
  );
};
```

#### Gesture Animation Pattern

Creating animations that respond to user interactions like drag, hover, or tap.

```jsx
import { motion } from 'framer-motion';
import { useState } from 'react';

const DraggableCard = () => {
  const [isDragging, setIsDragging] = useState(false);
  
  return (
    <motion.div
      drag
      dragConstraints={{ left: -100, right: 100, top: -50, bottom: 50 }}
      whileDrag={{ scale: 1.05, boxShadow: '0 10px 25px rgba(0,0,0,0.1)' }}
      onDragStart={() => setIsDragging(true)}
      onDragEnd={() => setIsDragging(false)}
      animate={{ 
        backgroundColor: isDragging ? '#f8f9fa' : '#ffffff'
      }}
      className="card"
    >
      <h3>Drag Me</h3>
      <p>This card can be dragged within constraints</p>
    </motion.div>
  );
};
```

#### Animation Orchestration Pattern

Coordinating complex sequences of animations with staggered timing.

```jsx
import { motion } from 'framer-motion';

const SequencedAnimation = () => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        when: "beforeChildren",
        staggerChildren: 0.1
      }
    }
  };
  
  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: { type: "spring", stiffness: 300 }
    }
  };
  
  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="container"
    >
      {Array.from({ length: 5 }).map((_, i) => (
        <motion.div
          key={i}
          variants={itemVariants}
          className="item"
        >
          Item {i + 1}
        </motion.div>
      ))}
    </motion.div>
  );
};
```

#### Reusable Animation Hook Pattern

Creating custom hooks for reusable animation logic.

```jsx
import { useState, useEffect } from 'react';
import { useSpring, animated } from 'react-spring';
import { useReducedMotion } from '../hooks/useReducedMotion';

// Custom animation hook
const useAnimatedNumber = (value, duration = 1000) => {
  const prefersReducedMotion = useReducedMotion();
  
  const spring = useSpring({
    from: { number: 0 },
    to: { number: value },
    config: { 
      duration: prefersReducedMotion ? 0 : duration 
    }
  });
  
  return spring;
};

// Component using the hook
const AnimatedCounter = ({ value }) => {
  const { number } = useAnimatedNumber(value);
  
  return (
    <div className="counter">
      <animated.span>
        {number.to(n => Math.floor(n))}
      </animated.span>
    </div>
  );
};
```

### Advanced Animation Patterns

#### Shared Element Transition Pattern

Creating smooth transitions between different views by animating shared elements.

```jsx
import { useState } from 'react';
import { motion, AnimateSharedLayout } from 'framer-motion';

const Gallery = ({ images }) => {
  const [selectedId, setSelectedId] = useState(null);
  
  return (
    <AnimateSharedLayout type="crossfade">
      <div className="gallery">
        {images.map(image => (
          <motion.div
            layoutId={`image-${image.id}`}
            onClick={() => setSelectedId(image.id)}
            className="thumbnail"
            key={image.id}
          >
            <motion.img
              src={image.thumbnail}
              alt={image.alt}
              layoutId={`image-src-${image.id}`}
            />
          </motion.div>
        ))}
      </div>
      
      {selectedId && (
        <motion.div
          layoutId={`image-${selectedId}`}
          className="full-image-container"
        >
          <motion.img
            src={images.find(img => img.id === selectedId).full}
            layoutId={`image-src-${selectedId}`}
            alt={images.find(img => img.id === selectedId).alt}
          />
          <motion.button
            onClick={() => setSelectedId(null)}
            className="close-button"
          >
            Close
          </motion.button>
        </motion.div>
      )}
    </AnimateSharedLayout>
  );
};
```

#### Parallax Scroll Pattern

Creating depth and dimension through different scroll speeds.

```jsx
import { useRef, useEffect } from 'react';

const ParallaxSection = () => {
  const containerRef = useRef(null);
  const foregroundRef = useRef(null);
  const middlegroundRef = useRef(null);
  const backgroundRef = useRef(null);
  
  useEffect(() => {
    const container = containerRef.current;
    const foreground = foregroundRef.current;
    const middleground = middlegroundRef.current;
    const background = backgroundRef.current;
    
    const handleScroll = () => {
      const scrollY = window.pageYOffset;
      const containerRect = container.getBoundingClientRect();
      
      // Only animate when in view
      if (containerRect.top < window.innerHeight && containerRect.bottom > 0) {
        const containerY = containerRect.top;
        
        // Different speed for each layer
        background.style.transform = `translateY(${containerY * 0.1}px)`;
        middleground.style.transform = `translateY(${containerY * 0.2}px)`;
        foreground.style.transform = `translateY(${containerY * 0.3}px)`;
      }
    };
    
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);
  
  return (
    <div ref={containerRef} className="parallax-container">
      <div ref={backgroundRef} className="parallax-layer background">
        {/* Background content */}
      </div>
      <div ref={middlegroundRef} className="parallax-layer middleground">
        {/* Middleground content */}
      </div>
      <div ref={foregroundRef} className="parallax-layer foreground">
        {/* Foreground content */}
      </div>
    </div>
  );
};
```

#### 3D Card Effect Pattern

Creating pseudo-3D effects with CSS transforms based on mouse position.

```jsx
import { useRef, useState } from 'react';

const Card3D = () => {
  const cardRef = useRef(null);
  const [rotateX, setRotateX] = useState(0);
  const [rotateY, setRotateY] = useState(0);
  
  const handleMouseMove = (e) => {
    if (!cardRef.current) return;
    
    const card = cardRef.current;
    const rect = card.getBoundingClientRect();
    
    // Calculate mouse position relative to card center
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    const mouseX = e.clientX - centerX;
    const mouseY = e.clientY - centerY;
    
    // Convert to rotation degrees with a maximum of 10 degrees
    const rotateY = (mouseX / (rect.width / 2)) * 10;
    const rotateX = -(mouseY / (rect.height / 2)) * 10;
    
    setRotateX(rotateX);
    setRotateY(rotateY);
  };
  
  const handleMouseLeave = () => {
    // Reset rotation when mouse leaves
    setRotateX(0);
    setRotateY(0);
  };
  
  return (
    <div
      ref={cardRef}
      className="card-3d"
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{
        transform: `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`,
        transition: 'transform 0.1s ease'
      }}
    >
      <div className="card-content">
        <h3>3D Card Effect</h3>
        <p>Move your mouse over this card to see the 3D effect</p>
      </div>
    </div>
  );
};
```

#### FLIP Animation Pattern

Using the FLIP technique (First, Last, Invert, Play) to create performant animations for layout changes.

```jsx
import { useRef, useEffect, useState } from 'react';

const FlipAnimation = ({ items, layout }) => {
  const containerRef = useRef(null);
  const positions = useRef(new Map());
  const [isAnimating, setIsAnimating] = useState(false);
  
  // Record positions before update
  useEffect(() => {
    if (!containerRef.current) return;
    
    const children = Array.from(containerRef.current.children);
    
    // Skip first render
    if (positions.current.size === 0) {
      children.forEach(child => {
        positions.current.set(child.dataset.id, child.getBoundingClientRect());
      });
      return;
    }
    
    // Record First position
    const firstPositions = new Map();
    children.forEach(child => {
      firstPositions.set(child.dataset.id, child.getBoundingClientRect());
    });
    
    // Force immediate update to Last position
    // This happens with the new layout
    
    // Calculate Invert
    requestAnimationFrame(() => {
      setIsAnimating(true);
      
      children.forEach(child => {
        const id = child.dataset.id;
        const firstRect = firstPositions.get(id);
        const lastRect = child.getBoundingClientRect();
        
        // Calculate the difference
        const deltaX = firstRect.left - lastRect.left;
        const deltaY = firstRect.top - lastRect.top;
        
        // Apply Invert transform
        child.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
        child.style.transition = 'none';
        
        // Force browser to acknowledge the transform
        void child.offsetWidth;
        
        // Play animation to final position
        child.style.transform = '';
        child.style.transition = 'transform 0.3s ease';
      });
      
      // Update positions for next time
      setTimeout(() => {
        children.forEach(child => {
          positions.current.set(child.dataset.id, child.getBoundingClientRect());
        });
        setIsAnimating(false);
      }, 300); // Match transition duration
    });
  },