# MoodStream AI Backend

This directory contains the FastAPI backend for MoodStream AI. It exposes a REST API for fetching entertainment recommendations.

## Development

Install dependencies and run the server:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Copy `.env.example` to `.env` and configure your Supabase credentials before
running the server. See `../docs/SUPABASE_SETUP.md` for full setup steps.
