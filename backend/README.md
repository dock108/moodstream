# MoodStream AI Backend

This directory contains the FastAPI backend for MoodStream AI. It exposes a REST API for fetching entertainment recommendations.

## Development

Copy `.env.example` to `.env` and fill in your Supabase and TMDB API keys.

Install dependencies and run the server:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Copy `.env.example` to `.env` and configure your Supabase credentials before
running the server. See `../docs/SUPABASE_SETUP.md` for full setup steps.
=======
You should be able to access `http://localhost:8000/ping` and receive a
`{"message": "pong"}` response.

