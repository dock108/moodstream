# MoodStream AI Backend

This directory contains the FastAPI backend for MoodStream AI. It exposes a REST API for fetching entertainment recommendations.

## Development

Copy `.env.example` to `.env` and fill in your API keys.

Install dependencies and run the server:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Copy `.env.example` to `.env` and configure your Supabase credentials before
running the server. See `../docs/SUPABASE_SETUP.md` for full setup steps.

The backend also integrates the IGDB API for video game metadata. Provide your
Twitch client credentials in `.env` as `TWITCH_CLIENT_ID` and
`TWITCH_CLIENT_SECRET`.

You should be able to access `http://localhost:8000/ping` and receive a
`{"message": "pong"}` response.

