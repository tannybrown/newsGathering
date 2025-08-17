"""
네이버 뉴스 API 서비스
"""
import requests
from typing import List
from fastapi import HTTPException
from ..core.settings import settings
from ..models.news import NewsItem, NewsResponse, CompanyNewsRequest


class NaverNewsService:
    """네이버 뉴스 API 서비스 클래스"""
    
    def __init__(self):
        self.api_url = settings.naver_news_api_url
        self.client_id = settings.naver_client_id
        self.client_secret = settings.naver_client_secret
    
    def _validate_credentials(self):
        """API 자격 증명 검증"""
        if not self.client_id or not self.client_secret:
            raise HTTPException(
                status_code=500,
                detail="네이버 API 키가 설정되지 않았습니다. .env 파일을 확인하세요."
            )
    
    def _clean_html_tags(self, text: str) -> str:
        """HTML 태그 제거"""
        return text.replace("<b>", "").replace("</b>", "")
    
    async def search_company_news(self, request: CompanyNewsRequest) -> NewsResponse:
        """기업 뉴스 검색"""
        self._validate_credentials()
        
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret
        }
        
        params = {
            "query": request.company_name,
            "display": request.display,
            "start": request.start,
            "sort": "date"  # 최신순으로 정렬
        }
        
        try:
            response = requests.get(self.api_url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # 뉴스 아이템들을 NewsItem 모델로 변환
            news_items = []
            for item in data.get("items", []):
                news_item = NewsItem(
                    title=self._clean_html_tags(item.get("title", "")),
                    originallink=item.get("originallink", ""),
                    link=item.get("link", ""),
                    description=self._clean_html_tags(item.get("description", "")),
                    pubDate=item.get("pubDate", ""),
                    source="naver"
                )
                news_items.append(news_item)
            
            return NewsResponse(
                company=request.company_name,
                total=data.get("total", 0),
                start=data.get("start", 1),
                display=data.get("display", 10),
                items=news_items
            )
            
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=500, 
                detail=f"네이버 API 호출 중 오류가 발생했습니다: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"서버 오류가 발생했습니다: {str(e)}"
            )
