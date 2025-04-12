# Project Context: Fullstack Application

## Project Overview

This is a Next.js-based fullstack application built with the Superstack template. It includes a complete authentication system, database integration with Prisma, and a UI component library using shadcn/ui components.

### Key Technologies

- **Frontend**: Next.js with App Router, React 18, TypeScript, Tailwind CSS
- **Backend**: Next.js API Routes, Prisma ORM
- **Authentication**: NextAuth.js with credential and OAuth providers
- **Database**: SQLite (development), PostgreSQL (production)
- **Form Management**: React Hook Form with Zod validation
- **Styling**: Tailwind CSS with shadcn/ui components
- **State Management**: React Context API and React Query

## Architecture Overview

### Directory Structure

The application follows a feature-based organization with clear separation of concerns:

- `app/`: Next.js App Router pages and layouts
- `components/`: Reusable UI components
- `lib/`: Core library code and utilities
- `prisma/`: Database schema and migrations
- `public/`: Static assets
- `styles/`: Global styles and Tailwind configuration
- `types/`: TypeScript type definitions

### Data Flow

1. Data is stored in the database managed by Prisma
2. API routes handle CRUD operations and business logic
3. Server Components fetch data directly when possible
4. Client Components use React Query for client-side data fetching
5. Forms use React Hook Form with Zod validation

### Authentication Flow

1. User authentication is handled by NextAuth.js
2. Protected routes are managed through middleware
3. User sessions are maintained using JWT or database sessions
4. Role-based access control determines permissions

## Design Principles

### UI/UX Principles

1. **Responsive Design**: Mobile-first approach with responsive layouts
2. **Accessibility**: WCAG 2.1 AA compliance with semantic HTML
3. **Performance**: Optimized loading with Server Components
4. **Consistency**: Unified design language with shadcn/ui components

### Code Principles

1. **Type Safety**: Strong typing with TypeScript
2. **Modularity**: Encapsulated components with clear interfaces
3. **DRY (Don't Repeat Yourself)**: Reuse code through abstractions
4. **Testing**: Unit and integration tests for critical functionality

## Development Guidelines

### Adding New Features

1. Create necessary database schema updates
2. Implement API endpoints with validation
3. Build UI components following the component architecture
4. Add tests for new functionality

### Component Structure

Components should:

1. Have a single responsibility
2. Accept props with TypeScript interfaces
3. Use composition over inheritance
4. Include proper error handling

### API Implementation

API routes should:

1. Use proper HTTP methods and status codes
2. Validate input with Zod schemas
3. Handle errors gracefully with appropriate responses
4. Include proper authentication checks

### Database Operations

Database interactions should:

1. Use Prisma Client for type-safe queries
2. Include transaction support for multi-step operations
3. Handle errors with appropriate logging
4. Use optimistic updates for better UX

## Common Patterns

### Form Handling

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const formSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
});

type FormValues = z.infer<typeof formSchema>;

export function ExampleForm() {
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      email: "",
    },
  });
  
  function onSubmit(data: FormValues) {
    // Handle form submission
  }
  
  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  );
}
```

### Data Fetching

```tsx
// In a Server Component
export default async function Page() {
  const data = await prisma.post.findMany();
  return <DataDisplay data={data} />;
}

// In a Client Component
"use client";

import { useQuery } from "@tanstack/react-query";

export function ClientDataFetch() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["posts"],
    queryFn: () => fetch("/api/posts").then(res => res.json())
  });
  
  if (isLoading) return <Loading />;
  if (error) return <Error />;
  
  return <DataDisplay data={data} />;
}
```

### Authentication Check

```tsx
import { useSession } from "next-auth/react";

export function ProtectedComponent() {
  const { data: session, status } = useSession();
  
  if (status === "loading") return <Loading />;
  if (status === "unauthenticated") return <AccessDenied />;
  
  return <AuthenticatedContent user={session.user} />;
}
```

## Common Issues and Solutions

### Problem: Authentication Issues

**Solution**: Check that:
- NextAuth.js is properly configured in `app/api/auth/[...nextauth]/route.ts`
- Middleware is correctly set up for protected routes
- Environment variables are properly set

### Problem: Database Connection Issues

**Solution**: Verify:
- Database URL in `.env`
- Prisma schema is synced with the database
- Required migrations have been applied

### Problem: UI Inconsistencies

**Solution**: Ensure:
- Components use the shadcn/ui styling conventions
- Tailwind classes follow the project's naming conventions
- Responsive design patterns are consistently applied

## Development Workflow

1. **Set up the environment**:
   ```bash
   npm install
   npx prisma migrate dev
   ```

2. **Run the development server**:
   ```bash
   npm run dev
   ```

3. **Testing**:
   ```bash
   npm run test
   ```

4. **Database Management**:
   ```bash
   npx prisma studio
   ```

5. **Building for production**:
   ```bash
   npm run build
   ```

## Deployment Guidelines

1. **Environment Setup**:
   - Set up database connection strings
   - Configure authentication providers
   - Set API keys and secrets

2. **Database Migration**:
   - Run production migrations
   - Backup data before significant changes

3. **Monitoring**:
   - Set up error tracking
   - Configure performance monitoring
   - Implement health checks