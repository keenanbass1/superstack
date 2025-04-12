# Supabase Integration Guide

This guide explains how to use Supabase with your Next.js application for authentication, database, and storage needs.

## What is Supabase?

Supabase is an open-source Firebase alternative that provides:
- PostgreSQL Database
- Authentication system
- Storage for files
- Realtime subscriptions
- Edge Functions
- Auto-generated APIs

## Setting Up Supabase

### 1. Create a Supabase Project

1. Sign up at [supabase.com](https://supabase.com)
2. Create a new project and note your project URL and anon key

### 2. Configure Environment Variables

Create or update your `.env.local` file with Supabase credentials:

```env
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

### 3. Initialize Supabase Client

The template includes a pre-configured Supabase client at `src/lib/supabase.ts`.

## Authentication

### Basic Authentication Flow

```tsx
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs'
import { useState } from 'react'

export default function LoginForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const supabase = createClientComponentClient()

  const handleSignIn = async (e) => {
    e.preventDefault()
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })
    if (error) {
      console.error('Error signing in:', error.message)
    } else {
      // Redirect or update UI
    }
  }
  
  // Form JSX...
}
```

### Auth UI Component

For a ready-made UI, use the Supabase Auth UI:

```tsx
import { Auth } from '@supabase/auth-ui-react'
import { ThemeSupa } from '@supabase/auth-ui-shared'
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs'

export default function AuthPage() {
  const supabase = createClientComponentClient()
  
  return (
    <Auth
      supabaseClient={supabase}
      appearance={{ theme: ThemeSupa }}
      providers={['google', 'github']}
      redirectTo={`${window.location.origin}/auth/callback`}
    />
  )
}
```

### Server-Side Authentication

For server components and route handlers:

```tsx
import { createServerComponentClient } from '@supabase/auth-helpers-nextjs'
import { cookies } from 'next/headers'

export default async function ProtectedPage() {
  const supabase = createServerComponentClient({ cookies })
  const { data: { session } } = await supabase.auth.getSession()
  
  if (!session) {
    // Handle unauthenticated state
    return <div>Please sign in</div>
  }
  
  // Authenticated content
}
```

## Database

### Querying Data

```tsx
// Client component
const { data, error } = await supabase
  .from('table_name')
  .select('*')
  .order('created_at', { ascending: false })
```

### Inserting Data

```tsx
const { data, error } = await supabase
  .from('table_name')
  .insert([
    { column1: 'value1', column2: 'value2' },
  ])
  .select()
```

### Updating Data

```tsx
const { data, error } = await supabase
  .from('table_name')
  .update({ column1: 'new_value' })
  .eq('id', record_id)
  .select()
```

### Deleting Data

```tsx
const { error } = await supabase
  .from('table_name')
  .delete()
  .eq('id', record_id)
```

## Storage

### Uploading Files

```tsx
const { data, error } = await supabase
  .storage
  .from('bucket_name')
  .upload('file_path', file)
```

### Downloading Files

```tsx
const { data, error } = await supabase
  .storage
  .from('bucket_name')
  .download('file_path')
```

### Getting Public URL

```tsx
const { data } = supabase
  .storage
  .from('bucket_name')
  .getPublicUrl('file_path')

const publicUrl = data.publicUrl
```

## Realtime Subscriptions

```tsx
const channel = supabase
  .channel('table_changes')
  .on(
    'postgres_changes',
    { event: '*', schema: 'public', table: 'table_name' },
    (payload) => {
      console.log('Change received!', payload)
      // Update UI based on the change
    }
  )
  .subscribe()
```

## Edge Functions

Deploy serverless functions to Supabase:

1. Install Supabase CLI: `npm install -g supabase`
2. Login: `supabase login`
3. Initialize: `supabase init`
4. Create function: `supabase functions new my-function`
5. Deploy: `supabase functions deploy my-function`

## Common Patterns

### Data Fetching with SWR

```tsx
import useSWR from 'swr'
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs'

const fetcher = async (url, table) => {
  const supabase = createClientComponentClient()
  const { data, error } = await supabase.from(table).select('*')
  if (error) throw error
  return data
}

export default function DataComponent() {
  const { data, error, isLoading } = useSWR(
    ['api/data', 'table_name'], 
    ([url, table]) => fetcher(url, table)
  )
  
  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error loading data</div>
  
  return (
    <div>
      {data.map(item => (
        <div key={item.id}>{item.name}</div>
      ))}
    </div>
  )
}
```

### Protected API Routes

```tsx
// src/app/api/protected/route.ts
import { createRouteHandlerClient } from '@supabase/auth-helpers-nextjs'
import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

export async function GET() {
  const supabase = createRouteHandlerClient({ cookies })
  const { data: { session } } = await supabase.auth.getSession()
  
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }
  
  // Process authenticated request
  return NextResponse.json({ data: 'Protected data' })
}
```

## Database Schema Management

For managing your database schema:

1. Create a `supabase/migrations` folder in your project
2. Add SQL migration files like `20230101000000_create_tables.sql`
3. Use the Supabase CLI to apply migrations: `supabase db push`

Example migration file:
```sql
-- Create a table
CREATE TABLE public.profiles (
  id UUID REFERENCES auth.users PRIMARY KEY,
  updated_at TIMESTAMP WITH TIME ZONE,
  username TEXT UNIQUE,
  avatar_url TEXT,
  
  CONSTRAINT username_length CHECK (char_length(username) >= 3)
);

-- Create a secure RLS policy
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public profiles are viewable by everyone." ON public.profiles
  FOR SELECT USING (true);

CREATE POLICY "Users can insert their own profile." ON public.profiles
  FOR INSERT WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can update their own profile." ON public.profiles
  FOR UPDATE USING (auth.uid() = id);
```

## Troubleshooting

### Authentication Issues

- Ensure environment variables are set correctly
- Check browser console for CORS errors
- Verify redirect URLs in Supabase dashboard settings

### Database Query Problems

- Use `.single()` when expecting exactly one row
- Add error handling for all database operations
- Check RLS policies if queries return no data

### Deployment Considerations

- Set environment variables in your hosting platform
- Add your site URL to Supabase Auth settings
- Use production API keys for deployed applications

## Learn More

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase GitHub Examples](https://github.com/supabase/supabase/tree/master/examples)
- [Next.js Auth Helpers](https://supabase.com/docs/guides/auth/auth-helpers/nextjs)
