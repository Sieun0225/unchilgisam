"""
app/models/vote.py - Vote 테이블 ORM 모델
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Vote(Base):
    """
    Vote 테이블

    사용자들이 운빨 사연에 대해 하는 투표 기록
    한 사용자가 같은 사연에 한 번만 투표 가능 (UniqueConstraint)
    """
    __tablename__ = "votes"

    # 필드
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    story_id = Column(Integer, ForeignKey("luck_stories.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    vote_type = Column(String(1), nullable=False)  # '+' 또는 '-'
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 제약조건: (story_id, user_id) 조합은 유니크 (한 사람이 한 사연에 한 번만 투표)
    __table_args__ = (
        UniqueConstraint('story_id', 'user_id', name='uq_story_user_vote'),
    )

    # 관계 설정
    story = relationship("LuckStory", back_populates="votes")
    voter = relationship("User", back_populates="votes")

    def __repr__(self):
        return f"<Vote(id={self.id}, story_id={self.story_id}, vote_type='{self.vote_type}')>"