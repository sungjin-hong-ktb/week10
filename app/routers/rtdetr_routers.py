# API 라우터 (엔드포인트 정의)
from fastapi import APIRouter, File, UploadFile

from app.models.schemas import DetectionResponse, HealthResponse, DetectionSummary
from app.controllers.rtdetr_controller import rtdetr_service
from app.utils.image_utils import load_image, validate_image
from app.exceptions.custom_exceptions import APIException

router = APIRouter()


@router.post("/detect", response_model=DetectionResponse)
async def detect_objects(file: UploadFile = File(...)):
    """
    객체 탐지 API

    동작 순서:
    1. 모델이 로드되어 있는지 확인
    2. 업로드된 파일 읽기
    3. 이미지 검증 (크기, 형식 등)
    4. 이미지 로드
    5. RT-DETR로 객체 탐지
    6. 결과 반환
    """
    # 1. 모델 확인
    if not rtdetr_service.is_loaded:
        raise APIException("모델이 로드되지 않았습니다", 503)

    # 2. 파일 읽기
    file_content = await file.read()

    # 3. 이미지 검증
    validate_image(file_content)

    # 4. 이미지 로드
    image = load_image(file_content)

    # 5. 객체 탐지 (서비스 사용)
    detections = rtdetr_service.predict(image)
    
    # 6. 결과 요약 생성
    class_counts = {}
    for d in detections:
        class_counts[d.class_name] = class_counts.get(d.class_name, 0) + 1

    summary = DetectionSummary(
        total_detections=len(detections),
        class_counts=class_counts
    )

    # 7. 결과 반환
    return DetectionResponse(
        summary=summary,
        detections=detections
    )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    헬스 체크 - 서버와 모델 상태 확인
    """
    return HealthResponse(
        status="Healthy" if rtdetr_service.is_loaded else "Unhealthy",
        model_loaded=rtdetr_service.is_loaded
    )