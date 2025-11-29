# FastAPI 메인 애플리케이션
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from app.routers.rtdetr_routers import router
from app.exceptions.handlers import (
    handle_api_exception,
    handle_validation_error,
    handle_general_error,
    handle_http_exception
)
from app.exceptions.custom_exceptions import APIException

# FastAPI 앱 생성
app = FastAPI(
    title="객체 탐지 API",
    description="RT-DETR 모델을 사용한 객체 탐지 API",
    version="1.0.0"
)

# 예외 핸들러 등록
app.add_exception_handler(HTTPException, handle_http_exception)
app.add_exception_handler(APIException, handle_api_exception)
app.add_exception_handler(RequestValidationError, handle_validation_error)
app.add_exception_handler(Exception, handle_general_error)

# API 라우터 포함
app.include_router(router, prefix="/api/v1", tags=["Detection"])

@app.get("/")
def root():
    return {
        "message": "RT-DETR 객체 탐지 API",
        "docs_url": "/docs",
        "health_check": "/api/v1/health"
    }