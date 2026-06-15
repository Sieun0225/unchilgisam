from sqlalchemy.orm import Session
from app.models.vote import Vote
from app.schemas.vote import VoteCreate, VoteSummary


def get_vote(db: Session, vote_id: int) -> Vote | None:
    return db.query(Vote).filter(Vote.id == vote_id).first()


def get_vote_by_user_and_story(db: Session, user_id: int, story_id: int) -> Vote | None:
    return db.query(Vote).filter(
        Vote.user_id == user_id,
        Vote.story_id == story_id
    ).first()


def get_votes_by_story(db: Session, story_id: int) -> list[Vote]:
    return db.query(Vote).filter(Vote.story_id == story_id).all()


def create_vote(db: Session, vote: VoteCreate) -> Vote:
    db_vote = Vote(
        story_id=vote.story_id,
        user_id=vote.user_id,
        vote_type=vote.vote_type,
    )
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote


def delete_vote(db: Session, vote_id: int) -> Vote | None:
    db_vote = get_vote(db, vote_id)
    if db_vote:
        db.delete(db_vote)
        db.commit()
    return db_vote


def get_vote_summary(db: Session, story_id: int) -> VoteSummary:
    votes = get_votes_by_story(db, story_id)
    plus_count = sum(1 for v in votes if v.vote_type == "+")
    minus_count = sum(1 for v in votes if v.vote_type == "-")
    return VoteSummary(
        story_id=story_id,
        plus_count=plus_count,
        minus_count=minus_count,
        total_count=plus_count + minus_count,
    )
