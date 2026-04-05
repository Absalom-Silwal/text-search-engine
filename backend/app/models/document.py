from pydantic import BaseModel, Field
from typing import Optional

class SearchDocument(BaseModel):
    id: str = Field(alias="_id")
    title: str
    content: str

class SearchResult(BaseModel):
    id: str
    title: str
    snippet: str
    score: float
    explanation: str
