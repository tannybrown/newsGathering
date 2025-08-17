from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional
import json

# 환경 변수 로드
load_dotenv()

app = FastAPI(
    title="기업 뉴스 API",
    description="네이버 API와 딥서치 뉴스 API를 활용한 기업 뉴스 검색 서비스",
    version="1.0.0"
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 네이버 API 설정
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
NAVER_NEWS_API_URL = "https://openapi.naver.com/v1/search/news.json"

# 딥서치 뉴스 API 설정
DEEPSEARCH_API_KEY = os.getenv("DEEPSEARCH_API_KEY")
DEEPSEARCH_NEWS_API_URL = "https://api.deepsearch.com/v1/news/search"

class NewsItem(BaseModel):
    title: str
    originallink: str
    link: str
    description: str
    pubDate: str
    source: str = "naver"  # 뉴스 소스 구분

class DeepSearchNewsItem(BaseModel):
    title: str
    url: str
    description: str
    published_at: str
    source: str = "deepsearch"
    company_mentions: Optional[List[str]] = None
    sentiment: Optional[str] = None

class NewsResponse(BaseModel):
    company: str
    total: int
    start: int
    display: int
    items: List[NewsItem]

class DeepSearchNewsResponse(BaseModel):
    company: str
    total: int
    items: List[DeepSearchNewsItem]

class CompanyNewsRequest(BaseModel):
    company_name: str
    display: Optional[int] = 10
    start: Optional[int] = 1

class DeepSearchNewsRequest(BaseModel):
    company_name: str
    limit: Optional[int] = 10
    days_back: Optional[int] = 30

@app.get("/")
async def root():
    return {"message": "기업 뉴스 API 서비스입니다. /docs에서 API 문서를 확인하세요."}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "서비스가 정상적으로 작동 중입니다."}

@app.post("/news/company", response_model=NewsResponse)
async def get_company_news(request: CompanyNewsRequest):
    """
    특정 기업에 대한 최신 뉴스를 검색합니다 (네이버 API).
    """
    if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
        raise HTTPException(
            status_code=500, 
            detail="네이버 API 키가 설정되지 않았습니다. env.example 파일을 참고하여 .env 파일을 생성하세요."
        )
    
    # 네이버 뉴스 API 호출
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    
    params = {
        "query": request.company_name,
        "display": request.display,
        "start": request.start,
        "sort": "date"  # 최신순으로 정렬
    }
    
    try:
        response = requests.get(NAVER_NEWS_API_URL, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # 뉴스 아이템들을 NewsItem 모델로 변환
        news_items = []
        for item in data.get("items", []):
            news_item = NewsItem(
                title=item.get("title", "").replace("<b>", "").replace("</b>", ""),
                originallink=item.get("originallink", ""),
                link=item.get("link", ""),
                description=item.get("description", "").replace("<b>", "").replace("</b>", ""),
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
        raise HTTPException(status_code=500, detail=f"네이버 API 호출 중 오류가 발생했습니다: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류가 발생했습니다: {str(e)}")

@app.post("/news/deepsearch", response_model=DeepSearchNewsResponse)
async def get_deepsearch_news(request: DeepSearchNewsRequest):
    """
    딥서치 뉴스 API를 통해 특정 기업에 대한 뉴스를 검색합니다.
    """
    if not DEEPSEARCH_API_KEY:
        # API 키가 없을 때 모의 데이터 반환
        print("딥서치 API 키가 설정되지 않아 모의 데이터를 반환합니다.")
        return await get_mock_deepsearch_news(request)
    
    # 딥서치 뉴스 API 호출
    headers = {
        "Authorization": f"Bearer {DEEPSEARCH_API_KEY}",
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
        response = requests.post(DEEPSEARCH_NEWS_API_URL, headers=headers, json=payload)
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
        raise HTTPException(status_code=500, detail=f"딥서치 API 호출 중 오류가 발생했습니다: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류가 발생했습니다: {str(e)}")

async def get_mock_deepsearch_news(request: DeepSearchNewsRequest):
    """
    딥서치 API 키가 없을 때 사용하는 모의 데이터 생성 함수
    """
    import random
    from datetime import datetime, timedelta
    
    # 모의 뉴스 데이터
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

@app.get("/news/company/{company_name}")
async def get_company_news_simple(
    company_name: str, 
    display: int = 10, 
    start: int = 1
):
    """
    GET 요청으로 기업 뉴스를 검색합니다 (네이버 API, 간단한 버전).
    """
    request = CompanyNewsRequest(
        company_name=company_name,
        display=display,
        start=start
    )
    return await get_company_news(request)

@app.get("/news/deepsearch/{company_name}")
async def get_deepsearch_news_simple(
    company_name: str,
    limit: int = 10,
    days_back: int = 30
):
    """
    GET 요청으로 딥서치 뉴스를 검색합니다 (간단한 버전).
    """
    request = DeepSearchNewsRequest(
        company_name=company_name,
        limit=limit,
        days_back=days_back
    )
    return await get_deepsearch_news(request)

@app.get("/news/combined/{company_name}")
async def get_combined_news(
    company_name: str,
    naver_limit: int = 5,
    deepsearch_limit: int = 5,
    deepsearch_days_back: int = 30
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
        naver_news = await get_company_news(naver_request)
        
        # 딥서치 뉴스 가져오기
        deepsearch_request = DeepSearchNewsRequest(
            company_name=company_name,
            limit=deepsearch_limit,
            days_back=deepsearch_days_back
        )
        deepsearch_news = await get_deepsearch_news(deepsearch_request)
        
        return {
            "company": company_name,
            "naver_news": {
                "total": naver_news.total,
                "items": naver_news.items
            },
            "deepsearch_news": {
                "total": deepsearch_news.total,
                "items": deepsearch_news.items
            },
            "combined_total": naver_news.total + deepsearch_news.total
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"통합 뉴스 검색 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port)
