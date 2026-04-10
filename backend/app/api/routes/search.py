from fastapi import APIRouter, Query
from app.services.search_service import SearchService
from app.models.document import SearchResult

router = APIRouter()

@router.get("/search", response_model=SearchResult)
async def search(q: str = Query(..., min_length=1),page:int=1,limit:int=10):
    results = await SearchService.search(q)
    start = (page-1)*limit
    end = start + limit
    return  SearchResult(
        items= results[start:end],
        total= len(results),
        page= page,
        pages= (len(results) + limit - 1) // limit
        )
