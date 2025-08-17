"""
뉴스 관련 데이터 모델
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class NewsItem(BaseModel):
    """네이버 뉴스 아이템 모델"""
    title: str = Field(..., description="뉴스 제목")
    originallink: str = Field(..., description="원본 뉴스 링크")
    link: str = Field(..., description="네이버 뉴스 링크")
    description: str = Field(..., description="뉴스 요약")
    pubDate: str = Field(..., description="발행일시")
    source: str = Field(default="naver", description="뉴스 소스")


class DeepSearchNewsItem(BaseModel):
    """딥서치 뉴스 아이템 모델"""
    title: str = Field(..., description="뉴스 제목")
    url: str = Field(..., description="뉴스 URL")
    description: str = Field(..., description="뉴스 설명")
    published_at: str = Field(..., description="발행일시")
    source: str = Field(default="deepsearch", description="뉴스 소스")
    company_mentions: Optional[List[str]] = Field(default=None, description="기업 언급 목록")
    sentiment: Optional[str] = Field(default=None, description="감정 분석 결과")


class NewsResponse(BaseModel):
    """네이버 뉴스 응답 모델"""
    company: str = Field(..., description="검색한 기업명")
    total: int = Field(..., description="총 뉴스 개수")
    start: int = Field(..., description="시작 위치")
    display: int = Field(..., description="표시 개수")
    items: List[NewsItem] = Field(..., description="뉴스 아이템 목록")


class DeepSearchNewsResponse(BaseModel):
    """딥서치 뉴스 응답 모델"""
    company: str = Field(..., description="검색한 기업명")
    total: int = Field(..., description="총 뉴스 개수")
    items: List[DeepSearchNewsItem] = Field(..., description="뉴스 아이템 목록")


class CompanyNewsRequest(BaseModel):
    """기업 뉴스 요청 모델"""
    company_name: str = Field(..., description="검색할 기업명")
    display: Optional[int] = Field(default=10, ge=1, le=100, description="한 번에 가져올 뉴스 개수")
    start: Optional[int] = Field(default=1, ge=1, description="시작 위치")


class DeepSearchNewsRequest(BaseModel):
    """딥서치 뉴스 요청 모델"""
    company_name: str = Field(..., description="검색할 기업명")
    limit: Optional[int] = Field(default=10, ge=1, le=100, description="가져올 뉴스 개수")
    days_back: Optional[int] = Field(default=30, ge=1, le=365, description="검색 기간 (일)")


class CombinedNewsResponse(BaseModel):
    """통합 뉴스 응답 모델"""
    company: str = Field(..., description="검색한 기업명")
    naver_news: dict = Field(..., description="네이버 뉴스 결과")
    deepsearch_news: dict = Field(..., description="딥서치 뉴스 결과")
    combined_total: int = Field(..., description="총 뉴스 개수")


class HealthResponse(BaseModel):
    """헬스 체크 응답 모델"""
    status: str = Field(..., description="서비스 상태")
    message: str = Field(..., description="상태 메시지")
    timestamp: datetime = Field(default_factory=datetime.now, description="체크 시간")
