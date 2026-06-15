"""
app/config.py - 프로젝트 설정
"""
import os
from dotenv import load_dotenv

load_dotenv()

# 데이터베이스
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./unchilgi.db")

# 개발 환경
DEBUG = os.getenv("DEBUG", "True") == "True"