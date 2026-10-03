from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.search import SearchRequest, SearchResponse
from app.services.search_service import search_shows


router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.post(
    "",
    response_model=SearchResponse,
)
async def search_movies(
    request: SearchRequest,
    db: Session = Depends(get_db),
):
    return search_shows(request, db)
