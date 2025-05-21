# MoodStream AI

MoodStream AI is an AI-driven entertainment recommendation platform. The project
includes a FastAPI backend and a Next.js frontend.

- See `PRD.md` for the full product requirements document.
- Supabase setup instructions are located in `docs/SUPABASE_SETUP.md`.
- Database schema and RLS policies can be found in `docs/db/schema.sql`.

## Environment Variables

1. Copy `.env.example` to `.env` and provide your `GPT_API_KEY`, `TMDB_API_KEY`
   and Twitch credentials (`TWITCH_CLIENT_ID`/`TWITCH_CLIENT_SECRET`).
2. Copy `backend/.env.example` to `backend/.env` and fill in your Supabase keys.
3. Copy `frontend/.env.local.example` to `frontend/.env.local` and supply the
   public Supabase URL and anon key.

## Running Locally

Start the backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

In a separate terminal start the frontend:

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000` in your browser. The backend will be available at
`http://localhost:8000`.

## Tests

Run backend unit tests with:

```bash
cd backend
pytest
```

The frontend stores user interactions ("Seen" or "Loved") in the Supabase
`user_content` table. Logged in users will see their saved status on the
recommendations page.
