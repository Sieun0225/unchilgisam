from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.vote import VoteCreate, VoteResponse, VoteSummary
from app.crud import vote as vote_crud
from app.crud import story as story_crud

router = APIRouter(prefix="/votes", tags=["votes"])


@router.get("/{story_id}/summary", response_model=VoteSummary)
def get_vote_summary(story_id: int, db: Session = Depends(get_db)):
    if not story_crud.get_story(db, story_id):
        raise HTTPException(status_code=404, detail="사연을 찾을 수 없습니다.")
    return vote_crud.get_vote_summary(db, story_id)


@router.post("/", response_model=VoteResponse, status_code=201)
def create_vote(vote: VoteCreate, db: Session = Depends(get_db)):
    if not story_crud.get_story(db, vote.story_id):
        raise HTTPException(status_code=404, detail="사연을 찾을 수 없습니다.")

    existing = vote_crud.get_vote_by_user_and_story(db, vote.user_id, vote.story_id)
    if existing:
        raise HTTPException(status_code=409, detail="이미 이 사연에 투표했습니다.")

    return vote_crud.create_vote(db, vote)


@router.delete("/{vote_id}", response_model=VoteResponse)
def delete_vote(vote_id: int, db: Session = Depends(get_db)):
    db_vote = vote_crud.delete_vote(db, vote_id)
    if not db_vote:
        raise HTTPException(status_code=404, detail="투표를 찾을 수 없습니다.")
    return db_vote
