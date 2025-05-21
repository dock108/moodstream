import asyncio

import pytest

from app.services import igdb_client


@pytest.mark.asyncio
async def test_parse_and_search(monkeypatch):
    sample = [
        {
            "id": 1,
            "name": "Stardew Valley",
            "genres": [{"name": "RPG"}],
            "cover": {"url": "//example.com/cover.jpg"},
            "summary": "A farming game",
            "platforms": [{"name": "PC"}],
        }
    ]

    async def fake_request(endpoint: str, query: str):
        return sample

    monkeypatch.setattr(igdb_client, "_igdb_request", fake_request)

    results = await igdb_client.search_games_by_genre_or_keyword("stardew")
    assert results[0]["title"] == "Stardew Valley"
    assert results[0]["genres"] == ["RPG"]
    assert results[0]["cover_image"].startswith("https://")

    game = await igdb_client.get_game_by_id(1)
    assert game["title"] == "Stardew Valley"


