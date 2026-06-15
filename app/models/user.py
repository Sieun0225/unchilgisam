"""
app/models/user.py - Users 테이블 ORM 모델
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """
    Users 테이블

    학교 학생들의 익명 계정 정보를 저장
    """
    __tablename__ = "users"

    # 필드
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nickname = Column(String(50), unique=True, nullable=False, index=True)
    grade = Column(Integer, nullable=False)  # 1, 2, 3
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 관계 설정 (역참조)
    # LuckStory: 사용자가 작성한 사연들
    stories = relationship("LuckStory", back_populates="author", cascade="all, delete-orphan")

    # Vote: 사용자가 한 투표들
    votes = relationship("Vote", back_populates="voter", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, nickname='{self.nickname}', grade={self.grade})>"