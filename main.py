from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.database import create_tables

app = FastAPI(title="운칠기삼", description="학교생활 속 운빨 사연 공유 플랫폼")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)

create_tables()
app.include_router(api_router)
