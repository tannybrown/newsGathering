"""
API v1 라우터 연결
"""
from fastapi import APIRouter
from .endpoints import news, health

api_router = APIRouter()

# 헬스 체크 라우터
api_router.include_router(health.router, prefix="/health", tags=["health"])

# 뉴스 라우터
api_router.include_router(news.router, prefix="/news", tags=["news"])
