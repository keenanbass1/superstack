# Fullstack Application Template

This document outlines the implementation of a new Superstack template for full-stack applications.

## Template Structure

```
fullstack-app/
├── app/                      # Next.js App Router structure
│   ├── api/                  # API routes using Next.js API handling
│   │   ├── auth/             # Authentication endpoints
│   │   ├── [entityName]/     # Dynamic API endpoints
│   │   └── route.ts          # Root API handler
│   ├── (auth)/               # Authentication-related routes
│   │   ├── login/
│   │   ├── register/
│   │   └── forgot-password/
│   ├── (dashboard)/          # Protected dashboard routes
│   ├── layout.tsx            # Root layout
│   └── page.tsx              # Home page
├── components/               # Reusable components
│   ├── ui/                   # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── form.tsx
│   │   └── ...
│   ├── layout/               # Layout components
│   │   ├── header.tsx
│   │   ├── footer.tsx
│   │   └── sidebar.tsx
│   ├── auth/                 # Auth-related components
│   └── data/                 # Data display components
├── lib/                      # Core library code
│   ├── auth.ts               # Authentication utilities
│   ├── db/                   # Database utilities
│   │   ├── schema.ts         # Database schema
│   │   ├── seed.ts           # Database seeding
│   │   └── client.ts         # Database client
│   ├── api/                  # API utilities
│   │   ├── handlers.ts       # API handler utilities
│   │   └── validation.ts     # API validation
│   └── utils/                # Utility functions
├── public/                   # Static assets
├── config/                   # Application configuration
│   ├── site.ts               # Site configuration
│   └── navigation.ts         # Navigation structure
├── types/                    # TypeScript type definitions
│   ├── api.ts                # API related types
│   ├── auth.ts               # Auth related types
│   └── db.ts                 # Database related types
├── middleware.ts             # Next.js middleware
├── project-context.md        # AI context document
├── tsconfig.json             # TypeScript configuration
├── package.json              # Project dependencies
├── tailwind.config.js        # Tailwind configuration
├── prettier.config.js        # Code formatting configuration
├── .env.example              # Example environment variables
└── README.md                 # Project documentation
```

## Key Technologies

- **Framework**: Next.js with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **Database**: Prisma ORM with SQLite/PostgreSQL
- **Authentication**: NextAuth.js
- **Form Handling**: React Hook Form + Zod
- **State Management**: React Context + Hooks
- **API Structure**: RESTful with Next.js API routes
- **Testing**: Jest + React Testing Library

## Template Features

1. **Type Safety**: End-to-end type safety between frontend and backend
2. **Authentication**: Complete auth flow with protected routes
3. **Database Setup**: Prisma ORM with migrations and seeding
4. **Form Validation**: Zod schemas for both client and server validation
5. **Component Library**: Pre-configured shadcn/ui components
6. **Dark Mode**: Built-in theme support with system preference detection
7. **API Structure**: Well-organized API structure with error handling
8. **Responsive Design**: Mobile-first responsive layout
9. **Error Handling**: Comprehensive error boundaries and API error handling
10. **Accessibility**: Built-in a11y features and testing
11. **Documentation**: Inline documentation and project README

## Implementation Details

### Configuration Files

1. **package.json**
   - Core dependencies for Next.js, React, Prisma, etc.
   - Development dependencies for TypeScript, testing, etc.
   - Scripts for development, building, testing, etc.

2. **tsconfig.json**
   - TypeScript configuration with strict type checking
   - Path aliases for clean imports

3. **tailwind.config.js**
   - Extended theme with Superstack design system colors
   - Custom plugins and configuration

4. **prisma/schema.prisma**
   - Database schema with models for User, etc.
   - Relations between models

### Key Components

1. **Authentication**
   - Login/Register forms with validation
   - Protected routes using middleware
   - Session management with NextAuth.js

2. **Layout**
   - Responsive sidebar navigation
   - Header with user profile and actions
   - Footer with site information

3. **Data Management**
   - CRUD operations for entities
   - Data tables with sorting and filtering
   - Forms for data entry and editing

### API Structure

1. **RESTful Endpoints**
   - Resource-based routing
   - Proper HTTP status codes
   - Consistent error handling

2. **Validation**
   - Zod schemas for request validation
   - Type-safe response handling

3. **Authentication**
   - JWT-based authentication
   - Role-based access control

## Implementation Plan

1. **Phase 1: Scaffolding**
   - Create directory structure
   - Add configuration files
   - Set up base Next.js application

2. **Phase 2: Authentication**
   - Implement NextAuth.js with Prisma adapter
   - Create login/register forms
   - Set up protected routes

3. **Phase 3: Database**
   - Set up Prisma schema
   - Create seed script
   - Implement CRUD utilities

4. **Phase 4: UI Components**
   - Implement shadcn/ui components
   - Create layout components
   - Build form components

5. **Phase 5: Documentation**
   - Write project README
   - Add inline code documentation
   - Create AI context document

## Testing Considerations

1. **Unit Tests**
   - Test utilities and helpers
   - Test API handlers

2. **Integration Tests**
   - Test database operations
   - Test authentication flow

3. **Component Tests**
   - Test UI components
   - Test form validation

4. **End-to-End Tests**
   - Test complete user flows
   - Test API endpoints

## Security Considerations

1. **Authentication**
   - Secure password handling
   - CSRF protection
   - Rate limiting

2. **Data Validation**
   - Input sanitization
   - Type validation

3. **API Security**
   - Proper error handling
   - Request validation

4. **Environment Variables**
   - Secure storage
   - Validation at startup

## Modularity Principles

1. **Component Isolation**
   - Each component handles a single responsibility
   - Props define component API

2. **Feature-Based Organization**
   - Group related code by feature
   - Minimize cross-feature dependencies

3. **Type-Driven Development**
   - Define interfaces before implementation
   - Use TypeScript to enforce contracts

4. **Clean Dependency Management**
   - Minimal external dependencies
   - Clear import structure

## Performance Considerations

1. **Server Components**
   - Leverage Next.js Server Components for data fetching
   - Minimize client-side JavaScript

2. **Image Optimization**
   - Use Next.js Image component
   - Set appropriate sizes and loading strategies

3. **Code Splitting**
   - Dynamic imports for large components
   - Route-based code splitting

4. **Data Fetching**
   - Implement efficient data fetching patterns
   - Use SWR for client-side data fetching

## Accessibility Focus

1. **Semantic HTML**
   - Use appropriate HTML elements
   - Maintain proper heading hierarchy

2. **ARIA Attributes**
   - Add ARIA labels where needed
   - Ensure proper focus management

3. **Keyboard Navigation**
   - Ensure all interactive elements are keyboard accessible
   - Test tab order and focus indicators

4. **Color Contrast**
   - Maintain WCAG 2.1 AA compliance
   - Test with assistive technologies

## Template Integration

This template will be added to the Superstack CLI by:

1. Creating the template files in `~/dev/templates/project-types/fullstack-app/`
2. Updating the `PROJECT_TEMPLATES` object in `scripts/dev/src/commands/new.ts` to include the new template
3. Adding documentation about the template to the Workflow Guide

## Usage

```bash
# Create a new fullstack application
dev new my-fullstack-app --template=fullstack-app

# Change to the project directory
cd my-fullstack-app

# Install dependencies
npm install

# Set up the database
npx prisma migrate dev --name init

# Start the development server
npm run dev
```

The template will include a detailed README with instructions for:
- Setting up the development environment
- Database configuration
- Authentication setup
- Deployment strategies
- Testing and quality assurance
- Adding new features