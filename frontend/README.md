# MoodStream AI Frontend

This folder contains the Next.js application for MoodStream AI. The project uses
TypeScript and can be deployed to Vercel.

## Local Development

1. Install dependencies:
   ```bash
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:3000`.

Copy `.env.local.example` to `.env.local` and provide your Supabase project URL
and anon key:

```
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
```

The frontend expects the FastAPI backend to be running locally at
`http://localhost:8000` when developing.

## Vercel Deployment

Connect this repository to Vercel using the GitHub integration. Vercel will
automatically deploy every push to the `main` branch.

1. In Vercel, create a new project and import this repository.
2. Set the same environment variables in the Vercel dashboard.
3. Deploy. Visiting `/` should show the homepage with navigation links.

Push new commits to trigger automatic previews.
