# 이미지 처리 유틸리티

from PIL import Image
import io
from app.exceptions.custom_exceptions import APIException


def validate_image(file_content: bytes) -> None:
    """
    이미지 파일 검증

    체크 항목:
    1. 파일이 비어있는지
    2. 파일 크기가 10MB 이하인지
    """
    # 빈 파일 체크
    if len(file_content) == 0:
        raise APIException("빈 파일입니다", 400)

    # 파일 크기 체크 (10MB)
    max_size = 10 * 1024 * 1024
    if len(file_content) > max_size:
        raise APIException("파일이 너무 큽니다 (최대 10MB)", 400)


def load_image(image_bytes: bytes) -> Image.Image:
    """
    바이트 데이터를 PIL Image로 변환
    """
    try:
        # 이미지 열기
        image = Image.open(io.BytesIO(image_bytes))

        # RGB로 변환
        if image.mode != 'RGB':
            image = image.convert('RGB')

        return image

    except Exception as e:
        raise APIException(f"이미지 로드 실패: {str(e)}", 400)
