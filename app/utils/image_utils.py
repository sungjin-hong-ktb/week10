import io
from PIL import Image
from fastapi import HTTPException, UploadFile


async def validate_image(file: UploadFile) -> None:
    """
    이미지 파일 검증 (비동기 방식)

    체크 항목:
    1. 파일이 비어있는지
    2. 파일 크기가 10MB 이하인지
    """
    content = await file.read()
    size = len(content)

    # 파일 포인터를 처음으로 되돌림
    await file.seek(0)

    # 빈 파일 체크
    if size == 0:
        raise HTTPException(status_code=400, detail="빈 파일입니다")

    # 파일 크기 체크 (10MB)
    max_size = 10 * 1024 * 1024
    if size > max_size:
        raise HTTPException(status_code=400, detail="파일이 너무 큽니다 (최대 10MB)")


async def load_image(file: UploadFile) -> Image.Image:
    """
    UploadFile 객체에서 PIL Image 로드 (비동기 방식)
    """
    try:
        content = await file.read()
        image = Image.open(io.BytesIO(content))

        if image.mode != 'RGB':
            image = image.convert('RGB')

        return image

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"이미지 로드 실패: {str(e)}")
