"""
app/models/__init__.py - 모든 ORM 모델을 한 곳에서 import
"""
from app.models.user import User
from app.models.story import LuckStory
from app.models.vote import Vote
from app.models.prediction import PredictionResult

__all__ = ["User", "LuckStory", "Vote", "PredictionResult"]