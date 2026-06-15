from fastapi import APIRouter
from app.api import stories, votes, rankings

api_router = APIRouter(prefix="/api")

api_router.include_router(stories.router)
api_router.include_router(votes.router)
api_router.include_router(rankings.router)
