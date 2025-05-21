# MoodStream AI Backend

This directory contains the FastAPI backend for MoodStream AI. It exposes a REST
API used by the frontend.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `backend/.env.example` to `backend/.env` and add your Supabase keys.
3. Copy `../.env.example` to `../.env` (or include the same values in
   `backend/.env`) for `GPT_API_KEY`, `TMDB_API_KEY` and Twitch credentials.
   See `../docs/SUPABASE_SETUP.md` for full details on the required variables.

## Running

Start the development server from the `backend` directory:

```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/ping` to verify the server is running. The backend
uses IGDB and TMDB for metadata; provide `TWITCH_CLIENT_ID`,
`TWITCH_CLIENT_SECRET` and `TMDB_API_KEY` to enable those features. Supplying a
`GPT_API_KEY` will enable GPT‑4 powered recommendations.
