# Next.js Application Template

This template provides a pre-configured Next.js application with all the essential tools and settings for building modern web applications.

## What's Included

- **Next.js 14** - The React framework for production
- **TypeScript** - For type safety and better developer experience
- **Tailwind CSS** - Utility-first CSS framework
- **Supabase** - Backend-as-a-Service with PostgreSQL, Auth, and Storage
- **ESLint** - Code linting for consistent code quality
- **Jest & React Testing Library** - For comprehensive testing
- **Pre-configured project structure** - Organized folders for components, pages, and more
- **AI-ready context** - Built-in support for AI-assisted development

## Getting Started

You can create a new project using this template with:

```bash
dev new my-project --template=next-app
```

After creating your project:

1. Navigate to your project folder:
   ```bash
   cd my-project
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up Supabase:
   - Create a Supabase project at [supabase.com](https://supabase.com)
   - Copy `.env.local.example` to `.env.local` and add your Supabase URL and anon key
   
4. Start the development server:
   ```bash
   npm run dev
   ```

5. Open your browser and visit: `http://localhost:3000`

## Project Structure

```
my-project/
├── .env.local.example   # Environment variables template
├── .eslintrc.json       # ESLint configuration
├── .gitignore           # Git ignore rules
├── jest.config.js       # Jest testing configuration
├── next.config.js       # Next.js configuration
├── package.json         # Project dependencies and scripts
├── project-context.md   # AI context document
├── README.md            # Project documentation
├── middleware.ts        # Supabase auth middleware
├── tailwind.config.js   # Tailwind CSS configuration
├── tsconfig.json        # TypeScript configuration
├── public/              # Static files
└── src/                 # Source code
    ├── app/             # Next.js App Router
    │   ├── api/         # API routes
    │   │   └── auth/    # Auth API endpoints
    │   ├── layout.tsx   # Root layout
    │   └── page.tsx     # Home page
    ├── components/      # Reusable components
    │   ├── auth/        # Authentication components
    │   ├── ui/          # UI components
    │   └── layout/      # Layout components
    ├── lib/             # Utility functions
    │   └── supabase.ts  # Supabase client
    ├── styles/          # Global styles
    └── types/           # TypeScript type definitions
        └── supabase.ts  # Supabase type definitions
```

## Available Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build the application for production
- `npm run start` - Start the production server
- `npm run lint` - Check for linting issues
- `npm run test` - Run tests
- `npm run test:watch` - Run tests in watch mode

## Supabase Integration

This template comes pre-configured with Supabase for:

- **Authentication** - Sign-up, sign-in, and session management
- **Database** - PostgreSQL database access with type safety
- **Storage** - File storage with proper access control
- **Realtime** - Realtime subscriptions for live updates

To learn more about using Supabase with this template, see the [Supabase Integration Guide](./guides/supabase-integration-guide.md).

## AI Context

This template includes a `project-context.md` file that provides AI assistants with information about your project. To update the AI assistants with your project details:

```bash
dev context push
```

## Customizing

You can customize any part of this template to fit your needs. The most common customizations are:

1. **Adding dependencies** - Install additional packages as needed
2. **Modifying the theme** - Update the Tailwind configuration
3. **Updating database schema** - Configure your Supabase tables and relationships
4. **Customizing authentication** - Modify the auth components and flows

## Troubleshooting

If you encounter any issues with this template, try these steps:

1. Make sure you have Node.js 18.17.0 or later installed
2. Clear your npm cache with `npm cache clean --force`
3. Delete the `node_modules` folder and run `npm install` again
4. Check the Next.js and Supabase documentation for specific errors

For more help, run:
```bash
dev help next-app
```

See also our guides:
- [Supabase Integration Guide](./guides/supabase-integration-guide.md)
- [Cursor AI Guide](./guides/cursor-ai-guide.md)
- [v0 Integration Guide](./guides/v0-integration-guide.md)
