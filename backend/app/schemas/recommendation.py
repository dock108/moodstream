from pydantic import BaseModel
from typing import List


class Recommendation(BaseModel):
    id: str
    title: str
    media_type: str  # movie, tv, game
    tags: List[str] = []
