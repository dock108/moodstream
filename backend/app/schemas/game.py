from pydantic import BaseModel
from typing import List, Optional


class Game(BaseModel):
    id: int
    title: str
    genres: List[str] = []
    cover_image: Optional[str] = None
    summary: Optional[str] = None
    platforms: List[str] = []

