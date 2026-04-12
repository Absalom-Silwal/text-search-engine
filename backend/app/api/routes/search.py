from fastapi import APIRouter, Query
from app.services.search_service import SearchService
from app.models.document import SearchResult

router = APIRouter()

@router.get("/search", response_model=SearchResult)
async def search(q: str = Query(..., min_length=1), page: int = Query(1, ge=1), limit: int = Query(10, ge=1)):
    skip = (page - 1) * limit
    items, total = await SearchService.search(q, skip=skip, limit=limit)
    
    return SearchResult(
        items=items,
        total=total,
        page=page,
        pages=(total + limit - 1) // limit if total > 0 else 0
    )
