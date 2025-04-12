# Superstack Fullstack Application

This is a fullstack application bootstrapped with the Superstack template, featuring Next.js, Prisma, NextAuth.js, and shadcn/ui.

## 🚀 Features

- **Next.js 14+** with App Router
- **TypeScript** for type safety
- **Prisma ORM** for database access
- **NextAuth.js** for authentication
- **Tailwind CSS** for styling
- **shadcn/ui** components
- **React Hook Form** with Zod validation
- **ESLint** and **Prettier** for code quality
- **Jest** and **React Testing Library** for testing

## 📋 Getting Started

### Prerequisites

- Node.js 18.17 or later
- npm or yarn
- Git

### Installation

1. Clone this repository
   ```bash
   git clone https://github.com/yourusername/my-fullstack-app.git
   cd my-fullstack-app
   ```

2. Install dependencies
   ```bash
   npm install
   # or
   yarn install
   ```

3. Set up your environment variables
   ```bash
   cp .env.example .env
   ```

4. Set up the database
   ```bash
   npx prisma migrate dev --name init
   ```

5. Start the development server
   ```bash
   npm run dev
   # or
   yarn dev
   ```

6. Open [http://localhost:3000](http://localhost:3000) in your browser

## 🏗️ Project Structure

```
my-fullstack-app/
├── app/                      # Next.js App Router
├── components/               # UI components
├── lib/                      # Core library code
├── prisma/                   # Database schema and migrations
├── public/                   # Static assets
├── styles/                   # Global styles
├── types/                    # TypeScript types
├── middleware.ts             # Next.js middleware
└── ...configuration files
```

## 🔑 Authentication

This template comes with NextAuth.js pre-configured for authentication:

- Email/Password authentication
- OAuth providers (Google, GitHub)
- Protected routes
- User session management

To configure additional providers, edit `app/api/auth/[...nextauth]/route.ts`.

## 💾 Database

Prisma is set up with a basic schema including:

- User model
- Authentication-related models
- Example content models

To modify your database schema:

1. Edit `prisma/schema.prisma`
2. Run migrations:
   ```bash
   npx prisma migrate dev --name your_migration_name
   ```
3. Generate Prisma client:
   ```bash
   npx prisma generate
   ```

## 🧩 Components

UI components are built with shadcn/ui and Tailwind CSS:

- Pre-built components in `components/ui/`
- Layout components in `components/layout/`
- Feature-specific components in their respective directories

To add new shadcn/ui components:

```bash
npx shadcn-ui@latest add button
```

## 🔄 State Management

This template uses:

- React Context for global state
- React Query for server state
- Local state with `useState` for component state

## 🧪 Testing

Run tests with:

```bash
npm run test
# or
yarn test
```

## 🚢 Deployment

This application can be deployed to Vercel with minimal configuration:

1. Push your code to GitHub
2. Import your repository in Vercel
3. Configure environment variables
4. Deploy

For other platforms, build the application with:

```bash
npm run build
# or
yarn build
```

## 📚 Learn More

To learn more about the technologies used:

- [Next.js Documentation](https://nextjs.org/docs)
- [Prisma Documentation](https://www.prisma.io/docs)
- [NextAuth.js Documentation](https://next-auth.js.org)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.