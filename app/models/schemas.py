from typing import List, Dict
from pydantic import BaseModel


class BoundingBox(BaseModel):
    """바운딩 박스"""
    x1: float
    y1: float
    x2: float
    y2: float


class DetectedObject(BaseModel):
    """탐지된 객체"""
    class_name: str
    confidence: float
    bounding_box: BoundingBox


class DetectionSummary(BaseModel):
    """탐지 요약"""
    total_detections: int
    class_counts: Dict[str, int]


class DetectionResponse(BaseModel):
    """탐지 응답"""
    success: bool = True
    summary: DetectionSummary
    detections: List[DetectedObject]


class ErrorResponse(BaseModel):
    """에러 응답"""
    success: bool = False
    error: str
    message: str


class HealthResponse(BaseModel):
    """헬스 체크"""
    model_config = {"protected_namespaces": ()}

    status: str
    model_loaded: bool