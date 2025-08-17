"""
헬스 체크 엔드포인트
"""
from fastapi import APIRouter
from ...models.news import HealthResponse

router = APIRouter()


@router.get("/", response_model=HealthResponse)
async def health_check():
    """서비스 상태 확인"""
    return HealthResponse(
        status="healthy",
        message="서비스가 정상적으로 작동 중입니다."
    )
