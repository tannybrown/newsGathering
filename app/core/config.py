"""
애플리케이션 설정 초기화
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings import settings


def create_app() -> FastAPI:
    """FastAPI 애플리케이션 인스턴스 생성"""
    
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        debug=settings.debug
    )
    
    # CORS 미들웨어 추가
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
    
    return app
