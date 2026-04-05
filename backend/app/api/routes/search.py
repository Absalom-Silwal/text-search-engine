from fastapi import APIRouter, Query
from app.services.search_service import SearchService
from app.models.document import SearchResult
from typing import List

router = APIRouter()

@router.get("/search", response_model=List[SearchResult])
async def search(q: str = Query(..., min_length=1)):
    results = await SearchService.search(q)
    print(results)
    return results
