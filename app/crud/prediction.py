from sqlalchemy.orm import Session
from app.models.prediction import PredictionResult


def get_prediction_by_story(db: Session, story_id: int) -> PredictionResult | None:
    return db.query(PredictionResult).filter(PredictionResult.story_id == story_id).first()


def create_or_update_prediction(
    db: Session,
    story_id: int,
    luck_score: float,
    confidence: float,
    model_version: str = "v1.0",
) -> PredictionResult:
    db_pred = get_prediction_by_story(db, story_id)
    if db_pred:
        db_pred.luck_score = luck_score
        db_pred.confidence = confidence
        db_pred.model_version = model_version
    else:
        db_pred = PredictionResult(
            story_id=story_id,
            luck_score=luck_score,
            confidence=confidence,
            model_version=model_version,
        )
        db.add(db_pred)
    db.commit()
    db.refresh(db_pred)
    return db_pred


def delete_prediction(db: Session, story_id: int) -> PredictionResult | None:
    db_pred = get_prediction_by_story(db, story_id)
    if db_pred:
        db.delete(db_pred)
        db.commit()
    return db_pred
