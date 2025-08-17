"""
딥서치 뉴스 API 서비스
"""
import requests
import random
from datetime import datetime, timedelta
from typing import List
from fastapi import HTTPException
from ..core.settings import settings
from ..models.news import DeepSearchNewsItem, DeepSearchNewsResponse, DeepSearchNewsRequest


class DeepSearchNewsService:
    """딥서치 뉴스 API 서비스 클래스"""
    
    def __init__(self):
        self.api_url = settings.deepsearch_news_api_url
        self.api_key = settings.deepsearch_api_key
    
    def _validate_credentials(self):
        """API 자격 증명 검증"""
        if not self.api_key:
            raise HTTPException(
                status_code=500,
                detail="딥서치 API 키가 설정되지 않았습니다. .env 파일을 확인하세요."
            )
    
    async def search_company_news(self, request: DeepSearchNewsRequest) -> DeepSearchNewsResponse:
        """기업 뉴스 검색"""
        if not self.api_key:
            # API 키가 없을 때 모의 데이터 반환
            print("딥서치 API 키가 설정되지 않아 모의 데이터를 반환합니다.")
            return await self._get_mock_news(request)
        
        self._validate_credentials()
        
        # 실제 딥서치 뉴스 API 호출
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "query": request.company_name,
            "limit": request.limit,
            "days_back": request.days_back,
            "include_company_mentions": True,
            "include_sentiment": True
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            # 딥서치 뉴스 아이템들을 DeepSearchNewsItem 모델로 변환
            news_items = []
            for item in data.get("articles", []):
                news_item = DeepSearchNewsItem(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    description=item.get("description", ""),
                    published_at=item.get("published_at", ""),
                    source="deepsearch",
                    company_mentions=item.get("company_mentions", []),
                    sentiment=item.get("sentiment", "")
                )
                news_items.append(news_item)
            
            return DeepSearchNewsResponse(
                company=request.company_name,
                total=len(news_items),
                items=news_items
            )
            
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=500, 
                detail=f"딥서치 API 호출 중 오류가 발생했습니다: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"서버 오류가 발생했습니다: {str(e)}"
            )
    
    async def _get_mock_news(self, request: DeepSearchNewsRequest) -> DeepSearchNewsResponse:
        """모의 뉴스 데이터 생성 (API 키가 없을 때 사용)"""
        
        # 모의 뉴스 데이터 템플릿
        mock_news_templates = [
            {
                "title": f"{request.company_name}, 새로운 기술 혁신 발표",
                "description": f"{request.company_name}이 혁신적인 기술을 발표하여 업계의 주목을 받고 있습니다. 이번 발표는 회사의 미래 전략에 중요한 의미를 가집니다.",
                "sentiment": "positive"
            },
            {
                "title": f"{request.company_name} 실적 전망 긍정적",
                "description": f"분석가들은 {request.company_name}의 실적 전망을 긍정적으로 평가하고 있습니다. 시장에서의 경쟁력이 지속적으로 향상되고 있다고 분석됩니다.",
                "sentiment": "positive"
            },
            {
                "title": f"{request.company_name}, 글로벌 시장 진출 확대",
                "description": f"{request.company_name}이 글로벌 시장 진출을 확대하고 있습니다. 해외 시장에서의 성과가 기대되고 있습니다.",
                "sentiment": "neutral"
            },
            {
                "title": f"{request.company_name} 신제품 출시 예정",
                "description": f"{request.company_name}이 곧 새로운 제품을 출시할 예정입니다. 소비자들의 관심이 집중되고 있습니다.",
                "sentiment": "positive"
            },
            {
                "title": f"{request.company_name}, 지속가능 경영 강화",
                "description": f"{request.company_name}이 지속가능 경영을 강화하고 있습니다. ESG 경영에 대한 투자가 확대되고 있습니다.",
                "sentiment": "neutral"
            }
        ]
        
        # 요청된 개수만큼 뉴스 생성
        news_items = []
        for i in range(min(request.limit, len(mock_news_templates))):
            template = mock_news_templates[i]
            
            # 랜덤 날짜 생성 (최근 N일 내)
            days_ago = random.randint(0, request.days_back)
            pub_date = datetime.now() - timedelta(days=days_ago)
            
            news_item = DeepSearchNewsItem(
                title=template["title"],
                url=f"https://mock-news.com/{request.company_name}/news-{i+1}",
                description=template["description"],
                published_at=pub_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                source="deepsearch (mock)",
                company_mentions=[request.company_name, request.company_name[:2]],
                sentiment=template["sentiment"]
            )
            news_items.append(news_item)
        
        return DeepSearchNewsResponse(
            company=request.company_name,
            total=len(news_items),
            items=news_items
        )
