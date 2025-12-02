from fastapi import APIRouter, File, UploadFile

from app.models.schemas import DetectionResponse, HealthResponse
from app.controllers.rtdetr_controller import rtdetr_service

router = APIRouter()


@router.post("/detect", response_model=DetectionResponse)
async def detect_objects(file: UploadFile = File(...)):
    """
    객체 탐지 API

    동작 순서:
    1. 업로드된 파일 객체 받기
    2. Controller에서 비즈니스 로직 처리 (스트림 방식)
    3. 결과 반환
    """
    # 1. Controller 호출 (파일 객체 직접 전달)
    return await rtdetr_service.detect_objects(file)


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    헬스 체크 - 서버와 모델 상태 확인
    """
    return HealthResponse(
        status="Healthy" if rtdetr_service.is_loaded else "Unhealthy",
        model_loaded=rtdetr_service.is_loaded
    )