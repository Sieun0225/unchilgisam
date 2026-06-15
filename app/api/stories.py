from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.story import StoryCreate, StoryResponse, StoryListItem
from app.crud import story as story_crud
from app.crud import user as user_crud
from app.crud import prediction as prediction_crud
from app.ml.model import predict_luck

router = APIRouter(prefix="/stories", tags=["stories"])


@router.get("/", response_model=list[StoryListItem])
def list_stories(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: str | None = Query(None),
    db: Session = Depends(get_db),
):
    return story_crud.get_stories(db, skip=skip, limit=limit, category=category)


@router.get("/{story_id}", response_model=StoryResponse)
def get_story(story_id: int, db: Session = Depends(get_db)):
    db_story = story_crud.increment_views(db, story_id)
    if not db_story:
        raise HTTPException(status_code=404, detail="사연을 찾을 수 없습니다.")
    return db_story


@router.post("/", response_model=StoryResponse, status_code=201)
def create_story(
    story: StoryCreate,
    user_id: int = Query(...),
    db: Session = Depends(get_db),
):
    if not user_crud.get_user(db, user_id):
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    db_story = story_crud.create_story(db, story=story, user_id=user_id)

    result = predict_luck(db_story)
    prediction_crud.create_or_update_prediction(
        db,
        story_id=db_story.id,
        luck_score=result["luck_score"],
        confidence=result["confidence"],
        model_version=result["model_version"],
    )
    db.refresh(db_story)
    return db_story


@router.delete("/{story_id}", response_model=StoryResponse)
def delete_story(story_id: int, db: Session = Depends(get_db)):
    db_story = story_crud.delete_story(db, story_id)
    if not db_story:
        raise HTTPException(status_code=404, detail="사연을 찾을 수 없습니다.")
    return db_story
