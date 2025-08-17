"""
기업 뉴스 API 메인 애플리케이션
"""
from .core.config import create_app
from .api.v1.api import api_router
from .core.settings import settings

# FastAPI 애플리케이션 생성
app = create_app()

# API 라우터 등록
app.include_router(api_router, prefix="/api/v1")

# 루트 엔드포인트
@app.get("/")
async def root():
    return {
        "message": f"{settings.app_name} 서비스입니다. /docs에서 API 문서를 확인하세요.",
        "version": settings.app_version,
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host=settings.host, 
        port=settings.port, 
        reload=settings.debug
    )
