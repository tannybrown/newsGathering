"""
뉴스 관련 엔드포인트
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from ...models.news import (
    CompanyNewsRequest, DeepSearchNewsRequest,
    NewsResponse, DeepSearchNewsResponse, CombinedNewsResponse
)
from ...services.naver_news import NaverNewsService
from ...services.deepsearch_news import DeepSearchNewsService

router = APIRouter()


def get_naver_service() -> NaverNewsService:
    """네이버 뉴스 서비스 의존성 주입"""
    return NaverNewsService()


def get_deepsearch_service() -> DeepSearchNewsService:
    """딥서치 뉴스 서비스 의존성 주입"""
    return DeepSearchNewsService()


@router.post("/company", response_model=NewsResponse)
async def get_company_news(
    request: CompanyNewsRequest,
    naver_service: NaverNewsService = Depends(get_naver_service)
):
    """
    특정 기업에 대한 최신 뉴스를 검색합니다 (네이버 API).
    """
    return await naver_service.search_company_news(request)


@router.post("/deepsearch", response_model=DeepSearchNewsResponse)
async def get_deepsearch_news(
    request: DeepSearchNewsRequest,
    deepsearch_service: DeepSearchNewsService = Depends(get_deepsearch_service)
):
    """
    딥서치 뉴스 API를 통해 특정 기업에 대한 뉴스를 검색합니다.
    """
    return await deepsearch_service.search_company_news(request)


@router.get("/company/{company_name}", response_model=NewsResponse)
async def get_company_news_simple(
    company_name: str,
    display: int = 10,
    start: int = 1,
    naver_service: NaverNewsService = Depends(get_naver_service)
):
    """
    GET 요청으로 기업 뉴스를 검색합니다 (네이버 API, 간단한 버전).
    """
    request = CompanyNewsRequest(
        company_name=company_name,
        display=display,
        start=start
    )
    return await naver_service.search_company_news(request)


@router.get("/deepsearch/{company_name}", response_model=DeepSearchNewsResponse)
async def get_deepsearch_news_simple(
    company_name: str,
    limit: int = 10,
    days_back: int = 30,
    deepsearch_service: DeepSearchNewsService = Depends(get_deepsearch_service)
):
    """
    GET 요청으로 딥서치 뉴스를 검색합니다 (간단한 버전).
    """
    request = DeepSearchNewsRequest(
        company_name=company_name,
        limit=limit,
        days_back=days_back
    )
    return await deepsearch_service.search_company_news(request)


@router.get("/combined/{company_name}", response_model=CombinedNewsResponse)
async def get_combined_news(
    company_name: str,
    naver_limit: int = 5,
    deepsearch_limit: int = 5,
    deepsearch_days_back: int = 30,
    naver_service: NaverNewsService = Depends(get_naver_service),
    deepsearch_service: DeepSearchNewsService = Depends(get_deepsearch_service)
):
    """
    네이버와 딥서치 API를 모두 사용하여 통합된 뉴스 결과를 반환합니다.
    """
    try:
        # 네이버 뉴스 가져오기
        naver_request = CompanyNewsRequest(
            company_name=company_name,
            display=naver_limit,
            start=1
        )
        naver_news = await naver_service.search_company_news(naver_request)
        
        # 딥서치 뉴스 가져오기
        deepsearch_request = DeepSearchNewsRequest(
            company_name=company_name,
            limit=deepsearch_limit,
            days_back=deepsearch_days_back
        )
        deepsearch_news = await deepsearch_service.search_company_news(deepsearch_request)
        
        return CombinedNewsResponse(
            company=company_name,
            naver_news={
                "total": naver_news.total,
                "items": naver_news.items
            },
            deepsearch_news={
                "total": deepsearch_news.total,
                "items": deepsearch_news.items
            },
            combined_total=naver_news.total + deepsearch_news.total
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"통합 뉴스 검색 중 오류가 발생했습니다: {str(e)}"
        )
