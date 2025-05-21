import json
import types
import sys
import pytest

from app.services import recommender


@pytest.mark.asyncio
async def test_recommend_for_mood(monkeypatch):
    suggestions = [
        {"type": "movie", "title": "Back to the Future", "genre": "Science Fiction", "reason": "Time travel fun."},
        {"type": "game", "title": "Stardew Valley", "genre": "Simulation", "reason": "Relaxing farming."},
        {"type": "movie", "title": "The Breakfast Club", "genre": "Drama", "reason": "80s classic."},
    ]

    async def fake_acreate(**kwargs):
        return {"choices": [{"message": {"content": json.dumps(suggestions)}}]}

    fake_openai = types.SimpleNamespace(ChatCompletion=types.SimpleNamespace(acreate=fake_acreate))
    monkeypatch.setitem(sys.modules, "openai", fake_openai)

    async def fake_movie_search(title: str):
        return {"title": title, "genres": ["Drama"], "id": 1}

    async def fake_game_search(keyword: str):
        return [{"title": keyword, "genres": ["Sim"], "id": 2}]

    monkeypatch.setattr(recommender, "search_movie_by_title", fake_movie_search)
    monkeypatch.setattr(recommender, "search_games_by_genre_or_keyword", fake_game_search)

    recs = await recommender.recommend_for_mood("nostalgic and bored")
    assert len(recs) == 3
    assert recs[0]["title"] == "Back to the Future"
    assert recs[1]["type"] == "game"

