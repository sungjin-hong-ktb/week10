# FastAPI 메인 애플리케이션
from fastapi import FastAPI

from app.routers.rtdetr_routers import router

# FastAPI 앱 생성
app = FastAPI(
    title="객체 탐지 API",
    description="RT-DETR 모델을 사용한 객체 탐지 API",
    version="1.0.0"
)

# API 라우터 포함
app.include_router(router, prefix="/api/v1", tags=["Detection"])

@app.get("/")
def root():
    return {
        "message": "RT-DETR 객체 탐지 API",
        "docs_url": "/docs",
        "health_check": "/api/v1/health"
    }