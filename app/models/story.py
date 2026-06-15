"""
app/models/story.py - LuckStory 테이블 ORM 모델
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class LuckStory(Base):
    """
    LuckStory 테이블

    사용자가 작성한 학교생활 속 운빨 사연을 저장
    """
    __tablename__ = "luck_stories"

    # 필드
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(20), nullable=False, index=True)  # 시험운, 발표운, 급식운 등

    # 점수 (1~5)
    control_score = Column(Integer, nullable=False)  # 통제 가능성
    stress_score = Column(Integer, nullable=False)  # 스트레스 수준
    satisfaction_score = Column(Integer, nullable=False)  # 만족도

    views_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # 관계 설정
    author = relationship("User", back_populates="stories")
    votes = relationship("Vote", back_populates="story", cascade="all, delete-orphan")
    prediction = relationship("PredictionResult", back_populates="story", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<LuckStory(id={self.id}, title='{self.title}', category='{self.category}')>"