import io
from PIL import Image
from fastapi import HTTPException, UploadFile


async def validate_and_load_image(file: UploadFile) -> Image.Image:
    """
    스트림 방식으로 이미지 파일을 검증하고 로드 (비동기 방식)

    체크 항목:
    1. 파일이 비어있는지
    2. 파일 크기가 10MB 이하인지
    3. PIL Image로 정상 로드 가능한지

    Args:
        file: 업로드된 파일 객체

    Returns:
        Image.Image: RGB 모드로 변환된 PIL Image 객체

    Raises:
        HTTPException: 파일 검증 실패 또는 이미지 로드 실패 시
    """
    try:
        # 스트림 방식으로 청크 단위 읽기
        max_size = 10 * 1024 * 1024  # 10MB
        chunk_size = 65536  # 64KB 청크
        total_size = 0
        chunks = []

        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break

            total_size += len(chunk)

            if total_size > max_size:
                raise HTTPException(
                    status_code=400,
                    detail="파일이 너무 큽니다 (최대 10MB)"
                )

            chunks.append(chunk)

        # 빈 파일 체크
        if total_size == 0:
            raise HTTPException(status_code=400, detail="빈 파일입니다")

        content = b''.join(chunks)
        image = Image.open(io.BytesIO(content))

        # RGB 모드로 변환
        if image.mode != 'RGB':
            image = image.convert('RGB')

        return image

    except HTTPException:
        # HTTPException은 그대로 전달
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"이미지 로드 실패: {str(e)}")
