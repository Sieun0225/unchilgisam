from sqlalchemy.orm import Session
from app.models.story import LuckStory
from app.schemas.story import StoryCreate


def get_story(db: Session, story_id: int) -> LuckStory | None:
    return db.query(LuckStory).filter(LuckStory.id == story_id).first()


def get_stories(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    category: str | None = None,
) -> list[LuckStory]:
    query = db.query(LuckStory)
    if category:
        query = query.filter(LuckStory.category == category)
    return query.order_by(LuckStory.created_at.desc()).offset(skip).limit(limit).all()


def get_stories_by_user(db: Session, user_id: int) -> list[LuckStory]:
    return db.query(LuckStory).filter(LuckStory.user_id == user_id).all()


def create_story(db: Session, story: StoryCreate, user_id: int) -> LuckStory:
    db_story = LuckStory(
        user_id=user_id,
        title=story.title,
        content=story.content,
        category=story.category,
        control_score=story.control_score,
        stress_score=story.stress_score,
        satisfaction_score=story.satisfaction_score,
    )
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    return db_story


def increment_views(db: Session, story_id: int) -> LuckStory | None:
    db_story = get_story(db, story_id)
    if db_story:
        db_story.views_count += 1
        db.commit()
        db.refresh(db_story)
    return db_story


def delete_story(db: Session, story_id: int) -> LuckStory | None:
    db_story = get_story(db, story_id)
    if db_story:
        db.delete(db_story)
        db.commit()
    return db_story


def get_top_stories_by_luck_score(db: Session, limit: int = 10) -> list[LuckStory]:
    return (
        db.query(LuckStory)
        .join(LuckStory.prediction)
        .order_by(LuckStory.prediction.property.mapper.class_.luck_score.desc())
        .limit(limit)
        .all()
    )
