from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.story import StoryListItem
from app.crud import story as story_crud

router = APIRouter(prefix="/rankings", tags=["rankings"])


@router.get("/luck", response_model=list[StoryListItem])
def get_luck_ranking(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """Luck Score 상위 사연 랭킹"""
    return story_crud.get_top_stories_by_luck_score(db, limit=limit)


@router.get("/views", response_model=list[StoryListItem])
def get_views_ranking(
    limit: int = Query(10, ge=1, le=50),
    category: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """조회수 상위 사연 랭킹"""
    stories = story_crud.get_stories(db, skip=0, limit=limit, category=category)
    return sorted(stories, key=lambda s: s.views_count, reverse=True)
