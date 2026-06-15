"""
app/models/prediction.py - PredictionResult 테이블 ORM 모델
"""
from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class PredictionResult(Base):
    """
    PredictionResult 테이블

    ML 모델이 계산한 각 사연의 Luck Score를 저장
    각 사연마다 최신 예측 결과 1개만 보유 (1:1 관계)
    """
    __tablename__ = "prediction_results"

    # 필드
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    story_id = Column(Integer, ForeignKey("luck_stories.id"), unique=True, nullable=False, index=True)

    luck_score = Column(Float, nullable=False)  # 0~100 (운의 영향도)
    confidence = Column(Float, nullable=False)  # 0~1 (모델 신뢰도)
    model_version = Column(String(20), default="v1.0")  # 사용된 모델 버전

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 관계 설정
    story = relationship("LuckStory", back_populates="prediction")

    def __repr__(self):
        return f"<PredictionResult(story_id={self.story_id}, luck_score={self.luck_score:.2f}, confidence={self.confidence:.3f})>"