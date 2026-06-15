"""
app/database.py - SQLAlchemy 설정 및 세션 관리
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import DATABASE_URL

# 데이터베이스 엔진 생성
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# 세션 팩토리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 모델의 기본 클래스
Base = declarative_base()

# 데이터베이스 세션 의존성 (FastAPI 라우트에서 사용)
def get_db():
    """
    FastAPI 라우트에서 DB 세션을 주입받기 위한 의존성
    예: async def get_stories(db: Session = Depends(get_db))
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 테이블 생성 (앱 시작 시 한 번 실행)
def create_tables():
    """모든 ORM 모델의 테이블을 데이터베이스에 생성"""
    Base.metadata.create_all(bind=engine)