from typing import List
from pydantic import BaseModel, Field
from typing import Optional

class SearchDocument(BaseModel):
    id: str = Field(alias="_id")
    title: str
    content: str

class SearchItem(BaseModel):
    id: str
    title: str
    snippet: str
    score: float
    explanation: str
    link: str

class SearchResult(BaseModel):
    items: List[SearchItem]
    total: int
    page: int
    pages: int
