"""
애플리케이션 설정 관리
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """애플리케이션 설정 클래스"""
    
    # 애플리케이션 기본 설정
    app_name: str = "기업 뉴스 API"
    app_description: str = "네이버 API와 딥서치 뉴스 API를 활용한 기업 뉴스 검색 서비스"
    app_version: str = "1.0.0"
    
    # 서버 설정
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # 네이버 API 설정
    naver_client_id: Optional[str] = None
    naver_client_secret: Optional[str] = None
    naver_news_api_url: str = "https://openapi.naver.com/v1/search/news.json"
    
    # 딥서치 뉴스 API 설정
    deepsearch_api_key: Optional[str] = None
    deepsearch_news_api_url: str = "https://api.deepsearch.com/v1/news/search"
    
    # CORS 설정
    cors_origins: list = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        
        # 환경 변수 매핑
        fields = {
            "naver_client_id": {"env": "NAVER_CLIENT_ID"},
            "naver_client_secret": {"env": "NAVER_CLIENT_SECRET"},
            "deepsearch_api_key": {"env": "DEEPSEARCH_API_KEY"},
            "host": {"env": "HOST"},
            "port": {"env": "PORT"}
        }


# 전역 설정 인스턴스
settings = Settings()
