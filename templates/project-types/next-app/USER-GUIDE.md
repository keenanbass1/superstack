# Next.js Template User Guide

This guide will help you understand how to use our Next.js template effectively, even if you're not a technical expert.

## 🚀 What This Template Provides

This template gives you a complete, ready-to-use Next.js application with:

- A modern, responsive design
- Type safety using TypeScript
- Beautiful styling with Tailwind CSS
- Backend services with Supabase (database, auth, storage)
- Testing setup with Jest
- Proper project organization
- Built-in components you can reuse

## 📋 Step-by-Step Guide for New Projects

### Creating Your Project

1. Open your terminal (Command Prompt on Windows or Terminal on Mac)

2. Run this command to create a new project:
   ```
   dev new my-project --template=next-app
   ```
   (Replace "my-project" with your preferred project name)

3. When the command finishes, you'll see instructions on how to proceed

### Setting Up Your Project

1. Navigate to your project folder:
   ```
   cd my-project
   ```

2. Install the necessary packages:
   ```
   npm install
   ```
   This might take a minute or two.

3. Set up Supabase:
   - Create a free account at [supabase.com](https://supabase.com)
   - Create a new project
   - In your Supabase dashboard, find your API keys
   - Copy the `.env.local.example` file to `.env.local`
   - Add your Supabase URL and anon key to this file

4. Start the development server:
   ```
   npm run dev
   ```

5. Open your browser and go to: [http://localhost:3000](http://localhost:3000)
   You should see your new website!

## 🧩 Understanding What You've Got

### Key Files and Folders

- **src/app/page.tsx**: This is your homepage. Edit this to change what visitors first see.
- **src/components/**: Contains reusable parts like buttons, headers, etc.
- **src/components/auth/**: Contains authentication-related components.
- **src/lib/supabase.ts**: The setup for connecting to your Supabase backend.
- **src/styles/globals.css**: Contains global styles for your entire site.
- **public/**: Place images and other files here that should be directly accessible.

### Pre-built Components

The template includes several components you can use:

- **Button**: A versatile button component with different styles
- **AuthForm**: Ready-to-use authentication form for sign-up and sign-in
- **Header**: A responsive page header with navigation
- **Footer**: A comprehensive page footer

## 🔐 Using Supabase Features

### Authentication

The template comes with a complete authentication system:

1. To add sign-in to a page, import the AuthForm component:
   ```jsx
   import AuthForm from '@/components/auth/AuthForm';
   
   export default function LoginPage() {
     return (
       <div className="container mx-auto py-12">
         <h1 className="text-2xl font-bold mb-6">Sign In</h1>
         <AuthForm />
       </div>
     );
   }
   ```

2. To protect a page so only logged-in users can see it:
   ```jsx
   import { createServerComponentClient } from '@supabase/auth-helpers-nextjs';
   import { cookies } from 'next/headers';
   import { redirect } from 'next/navigation';
   
   export default async function ProtectedPage() {
     const supabase = createServerComponentClient({ cookies });
     const { data: { session } } = await supabase.auth.getSession();
     
     if (!session) {
       redirect('/login');
     }
     
     return (
       <div>
         <h1>Protected Content</h1>
         <p>Welcome, {session.user.email}</p>
       </div>
     );
   }
   ```

### Database

To access your database:

1. Create tables in the Supabase dashboard
2. Access data in your components:
   ```jsx
   import { createClientComponentClient } from '@supabase/auth-helpers-nextjs';
   import { useEffect, useState } from 'react';
   
   export default function DataList() {
     const [data, setData] = useState([]);
     const supabase = createClientComponentClient();
     
     useEffect(() => {
       async function fetchData() {
         const { data, error } = await supabase
           .from('your_table')
           .select('*');
           
         if (!error) setData(data);
       }
       
       fetchData();
     }, []);
     
     return (
       <div>
         <h2>Your Data</h2>
         <ul>
           {data.map(item => (
             <li key={item.id}>{item.name}</li>
           ))}
         </ul>
       </div>
     );
   }
   ```

### File Storage

To store and retrieve files:

1. Create a bucket in the Supabase dashboard
2. Upload files:
   ```jsx
   const { data, error } = await supabase
     .storage
     .from('your_bucket')
     .upload('file_path', fileObject);
   ```

3. Retrieve file URLs:
   ```jsx
   const { data } = supabase
     .storage
     .from('your_bucket')
     .getPublicUrl('file_path');
     
   const imageUrl = data.publicUrl;
   ```

## 🎨 Customizing Your Project

### Changing Text and Content

1. Open `src/app/page.tsx` in your code editor
2. Look for text between quotes or tags like `<h1>` and `</h1>`
3. Change this text to your own content
4. Save the file and your browser will automatically update

### Changing Colors and Styling

1. The template uses Tailwind CSS, which applies styles using class names
2. To change colors, look for classes like `text-blue-600` and change `blue` to colors like `red`, `green`, `purple`, etc.
3. For background colors, look for classes like `bg-white` or `bg-gray-100`
4. For more advanced customization, edit `tailwind.config.js`

### Adding New Pages

1. In the `src/app` folder, create a new folder with the name of your page (e.g., `about`)
2. Inside that folder, create a file named `page.tsx`
3. Add your content, starting with this basic structure:

```tsx
export default function AboutPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold mb-6">About Us</h1>
      <p>Your content here...</p>
    </div>
  )
}
```

4. Visit `http://localhost:3000/about` to see your new page

## 🤖 Using AI Assistance

This template is designed to work with AI assistance through the Superstack system:

1. **Initialize AI Context**:
   ```
   dev context init
   ```
   This creates a file describing your project to AI assistants.

2. **Update the Context**:
   Edit the `project-context.md` file to include details about your project.

3. **Push Context to AI**:
   ```
   dev context push
   ```
   This updates the AI assistants with your project details.

4. **Get AI Help with Supabase**:
   ```
   dev ai solve "Create a Supabase query to get the latest posts with user data"
   ```
   The AI will generate code specifically for your project.

## 📱 Making Your Site Mobile-Friendly

The template is already responsive, meaning it works well on mobile devices. Key tips:

- Test your site by resizing your browser window
- Use `sm:`, `md:`, `lg:` prefixes with Tailwind classes to apply styles at different screen sizes
- Example: `class="text-sm md:text-base lg:text-lg"` makes text grow larger on bigger screens

## 🔍 Troubleshooting Common Issues

### Auth Issues

1. Make sure your `.env.local` file has the correct Supabase URL and anon key
2. Check that your Supabase project has Email auth enabled in the Authentication settings
3. For password reset and email verification, set up your Site URL in Supabase Auth settings

### Database Issues

1. Verify table names and column names match exactly in your queries
2. Check RLS (Row Level Security) policies in Supabase if queries return no data
3. Use the Network tab in browser dev tools to see the actual API requests

### Images Don't Appear

1. Make sure your images are in the `public` folder
2. Reference them starting with `/` like `<img src="/my-image.jpg" />`
3. For Supabase Storage, make sure your storage buckets have the correct permissions

## 📚 Learning More

- [Next.js Documentation](https://nextjs.org/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Supabase Integration Guide](./guides/supabase-integration-guide.md)

For specific questions about using this template, use:
```
dev ai query "How do I implement real-time updates with Supabase?"
```

## 🚀 Deploying Your Site

The easiest way to deploy your Next.js site is with [Vercel](https://vercel.com/):

1. Create a Vercel account
2. Connect your GitHub, GitLab, or Bitbucket repository
3. Add your environment variables from `.env.local`
4. Vercel will automatically deploy your site

---

We hope this guide helps you get started with your Next.js and Supabase project! If you have any questions, the AI assistance through the Superstack system is just a command away.
