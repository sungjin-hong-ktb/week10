# RT-DETR 서비스 (비즈니스 로직)
import os

from typing import List
from PIL import Image
import torch
from ultralytics import RTDETR

from app.models.schemas import DetectedObject, BoundingBox

# PyTorch 설정
try:
    from ultralytics.nn.tasks import DetectionModel
    torch.serialization.add_safe_globals([DetectionModel])
except:
    pass


class RTDETRService:
    """
    RT-DETR 모델 서비스

    역할:
    - RT-DETR 모델 로드 및 관리
    - 이미지에서 객체 탐지 수행
    """
    _instance = None
    _model = None
    _device = None
    _model_path = os.getenv("MODEL_PATH", "rtdetr-l.pt")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._model is None:
            if torch.mps.is_available():
                self._device = 'mps'
                print(f"Device '{self._device}'")
            elif torch.cuda.is_available():
                self._device = 'cuda'
                print(f"Device '{self._device}'")
            else:
                self._device = 'cpu'
                print(f"Device '{self._device}'")

            # RT-DETR 모델 로드 및 디바이스로 이동
            self._model = RTDETR(self._model_path)
            self._model.to(self._device)

    def predict(self, image: Image.Image) -> List[DetectedObject]:
        """이미지에서 객체 탐지"""
        results = self._model.predict(
            source=image, 
            device=self._device, 
            verbose=False,
            conf=0.60,
            iou=0.70,
        )
        result = results[0]

        # 결과 파싱
        detections = []
        for box in result.boxes:
            coords = box.xyxy[0].cpu().numpy()
            confidence = float(box.conf[0].cpu().numpy())
            class_id = int(box.cls[0].cpu().numpy())
            class_name = result.names[class_id]

            obj = DetectedObject(
                class_name=class_name,
                confidence=round(confidence, 3),
                bounding_box=BoundingBox(
                    x1=round(float(coords[0]), 3),
                    y1=round(float(coords[1]), 3),
                    x2=round(float(coords[2]), 3),
                    y2=round(float(coords[3]), 3)
                )
            )
            detections.append(obj)

        return detections

    @property
    def is_loaded(self) -> bool:
        """모델 로드 여부"""
        return self._model is not None


rtdetr_service = RTDETRService()
