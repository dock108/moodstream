# MoodStream AI

MoodStream AI is an AI-driven entertainment recommendation platform. The project consists of a FastAPI backend and a Next.js frontend.

See `PRD.md` for the full product requirements document.

Supabase configuration instructions are available in `docs/SUPABASE_SETUP.md`.

The backend can fetch video game metadata using the IGDB API. Set your Twitch
client ID and secret in `.env` to enable these features.
=======
Database schema and RLS policies are defined in `docs/db/schema.sql`.

The frontend stores user interactions ("Seen" or "Loved") in Supabase using the
`user_content` table. Logged in users will see their saved status on the
recommendations page.

