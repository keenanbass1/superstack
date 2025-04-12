# Using v0 Components with Your Next.js Application

This guide explains how to use [v0](https://v0.dev/) by Vercel to generate UI components and integrate them seamlessly into your Next.js application created with the Superstack template.

## What is v0?

v0 is an AI-powered UI design tool by Vercel that generates React components based on text descriptions. It creates modern, responsive components using React and Tailwind CSS—perfectly matching our Next.js template configuration.

## Prerequisites

- A Next.js project created using the Superstack template
- Access to v0 (via paid plan)
- Basic understanding of React components

## Step-by-Step Integration Guide

### 1. Generate a Component with v0

1. Go to [v0.dev](https://v0.dev/) and sign in
2. Create a new component by entering a detailed description, for example:
   ```
   A product card with image, title, price, rating stars, and an "Add to Cart" button
   ```
3. Refine the component until you're satisfied with the result

### 2. Export the Component

1. Once your component looks good, click the **"Code"** button in v0
2. v0 will show you the React code for your component
3. Click the **"Copy"** button to copy the code to your clipboard

### 3. Prepare Your Project

1. Open your Next.js project in your code editor (Cursor recommended)
2. Navigate to the appropriate folder based on component type:
   - UI components: `src/components/ui/`
   - Layout components: `src/components/layout/`
   - Feature components: Create `src/components/features/` if it doesn't exist

### 4. Create the Component File

1. Create a new file with a descriptive name, using PascalCase:
   - Example: `src/components/ui/ProductCard.tsx`

2. Paste the v0-generated code into this file

### 5. Modify the Component (If Needed)

The v0 component may need some adjustments:

1. **Add TypeScript Types**:
   ```tsx
   interface ProductCardProps {
     title: string;
     price: number;
     image: string;
     rating: number;
     onAddToCart: () => void;
   }

   export function ProductCard({ title, price, image, rating, onAddToCart }: ProductCardProps) {
     // v0 component code
   }
   ```

2. **Fix Imports**:
   - v0 may generate components that use libraries not in your project
   - Either install those libraries or replace with alternatives
   - Common additions needed: `npm install lucide-react` for icons

3. **Adjust Styling**:
   - The template already includes Tailwind CSS
   - You may want to adjust colors/styling to match your project theme
   - Modify Tailwind classes directly in the component

### 6. Fix Dependencies

Check if the component uses any external dependencies:

1. Icons (most common):
   ```bash
   npm install lucide-react
   ```

2. UI libraries like Radix UI or Headless UI:
   ```bash
   npm install @radix-ui/react-dropdown-menu
   ```

### 7. Use the Component

Now you can use your component in any page:

```tsx
// src/app/page.tsx or any other page
import { ProductCard } from '@/components/ui/ProductCard';

export default function Page() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Our Products</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <ProductCard 
          title="Wireless Headphones"
          price={99.99}
          image="/headphones.jpg"
          rating={4.5}
          onAddToCart={() => console.log('Added to cart')}
        />
        {/* Add more product cards as needed */}
      </div>
    </div>
  );
}
```

## Common Patterns and Best Practices

### Component Organization

Organize v0 components based on their purpose:

- `src/components/ui/` - Basic UI elements (buttons, cards, inputs)
- `src/components/layout/` - Structural components (headers, sidebars, layouts)
- `src/components/features/` - Feature-specific components (product listings, checkout forms)

### Managing Assets

If your v0 component references images:

1. Place images in the `public` folder
2. Reference them with paths starting with `/`:
   ```tsx
   <img src="/product-image.jpg" alt="Product" />
   ```

### Creating Component Libraries

To build a reusable collection of v0 components:

1. Create component variations in separate files
2. Export them from a central index file
3. Document props and usage

### Tailwind Customization

To customize how v0 components look:

1. Modify `tailwind.config.js` to add your brand colors
   ```js
   theme: {
     extend: {
       colors: {
         brand: {
           light: "#a7f3d0",
           DEFAULT: "#059669",
           dark: "#064e3b",
         }
       }
     }
   }
   ```

2. Replace colors in v0 components:
   - Change `bg-blue-600` to `bg-brand`
   - Change `text-blue-500` to `text-brand`

## Troubleshooting Common Issues

### Components Look Different Than in v0

- **Problem**: Styling doesn't match the v0 preview
- **Solution**: Check for missing Tailwind plugins or configurations

### Missing Dependencies

- **Problem**: Errors about missing imports
- **Solution**: Install the necessary packages or replace with alternatives

### Type Errors

- **Problem**: TypeScript errors in v0 components
- **Solution**: Add proper type definitions or use type assertions temporarily

## Advanced Integration

### Creating a v0 Component Library

For more organized use of v0:

1. Create a dedicated directory for v0 components:
   ```
   src/components/v0/
   ```

2. Add documentation to each component:
   ```tsx
   /**
    * ProductCard - A card displaying product information
    * 
    * Generated with v0.dev (prompt: "A product card with...")
    * 
    * @example
    * <ProductCard 
    *   title="Headphones"
    *   price={99.99}
    *   image="/headphones.jpg"
    *   rating={4.5}
    *   onAddToCart={() => {}}
    * />
    */
   ```

3. Create an index file to export all components:
   ```tsx
   // src/components/v0/index.ts
   export * from './ProductCard';
   export * from './Navbar';
   // etc.
   ```

### Using v0 for Page Layouts

You can use v0 to generate entire page layouts:

1. Generate a complex layout in v0
2. Split it into smaller components
3. Assemble them in your page files

---

With this guide, you should be able to seamlessly integrate v0-generated components into your Next.js application. The Superstack template is specifically designed to work well with v0's output, making it easy to build beautiful UIs quickly.
