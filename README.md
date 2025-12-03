# RT-DETR 객체 탐지 API

RT-DETR(Real-Time Detection Transformer) 모델을 사용하여 이미지에서 객체를 탐지한 후 총 객체 수, 각 객체의 수를 반환해줍니다.

## 기술 스택

![FastAPI](https://img.shields.io/badge/FastAPI-0.115.5-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Ultralytics](https://img.shields.io/badge/Ultralytics-8.3.0+-0F4C81?logo=ultralytics&style=for-the-badge)

## 프로젝트 구조

```
assignment/
├── app/
│   ├── __init__.py
│   ├── controllers/              # 비즈니스 로직 및 모델 관리
│   │   ├── __init__.py
│   │   └── rtdetr_controller.py
│   ├── models/                   # 데이터 스키마 정의
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── routers/                  # API 엔드포인트 정의
│   │   ├── __init__.py
│   │   └── rtdetr_routers.py 
│   └── utils/                    # 유틸리티 함수
│       ├── __init__.py
│       └── image_utils.py        # 이미지 검증 및 로드 (비동기 스트림)
├── main.py                       # FastAPI 애플리케이션 진입점
├── requirements.txt              # Python 의존성
├── rtdetr-l.pt                   # RT-DETR 모델 가중치 파일
├── .env                          # 환경 변수 (MODEL_PATH 등)
└── .gitignore
```

## 주요 기능

- **객체 탐지**: RT-DETR 모델을 사용한 객체 탐지
- **헬스 체크**: 서버 및 모델 로드 상태 확인 API
- **비동기 스트림 처리**: 청크 단위(64KB)로 파일을 읽어 메모리 효율적 처리
- **자동 이미지 검증**: 파일 크기(최대 10MB) 및 형식 자동 검증

## 설치 및 실행

### 1. 가상환경 생성 및 활성화

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

**주요 의존성:**
- `fastapi==0.115.5`: 웹 프레임워크
- `ultralytics>=8.3.0`: RT-DETR 모델
- `pillow==11.0.0`: 이미지 처리
- `python-multipart==0.0.12`: 파일 업로드 지원
- `uvicorn[standard]==0.32.1`: ASGI 서버

### 3. 서버 실행

```bash
uvicorn main:app --reload
```

서버가 `http://localhost:8000`에서 실행됩니다.

## API 엔드포인트

### 1. 루트 엔드포인트
```
GET /
```
API 정보 및 사용 가능한 엔드포인트 목록을 반환합니다.

**응답 예시:**
```json
{
  "message": "RT-DETR 객체 탐지 API",
  "docs_url": "/docs",
  "health_check": "/api/v1/health"
}
```

### 2. 객체 탐지
```
POST /api/v1/detect
```
이미지 파일을 업로드하여 객체를 탐지합니다.

**요청:**
- Content-Type: `multipart/form-data`
- Body: `file` (이미지 파일, 최대 10MB)

**성공 응답 (200):**
```json
{
  "success": true,
  "summary": {
    "total_detections": 2,
    "class_counts": {
      "dog": 1,
      "cat": 1
    }
  },
  "detections": [
    {
      "class_name": "dog",
      "confidence": 0.955,
      "bounding_box": {
        "x1": 334.505,
        "y1": 235.96,
        "x2": 2779.528,
        "y2": 1838.912
      }
    },
    {
      "class_name": "cat",
      "confidence": 0.591,
      "bounding_box": {
        "x1": 322.392,
        "y1": 409.715,
        "x2": 1659.68,
        "y2": 1836.041
      }
    }
  ]
}
```

**에러 응답:**
```json
{
  "detail": "파일이 너무 큽니다 (최대 10MB)"
}
```

### 3. 헬스 체크
```
GET /api/v1/health
```
서버 및 모델 상태를 확인합니다.

**응답 예시:**
```json
{
  "status": "Healthy",
  "model_loaded": true
}
```

## 사용 예시

### cURL을 사용한 객체 탐지

```bash
curl -X POST "http://localhost:8000/api/v1/detect" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/image.jpg"
```

### Python을 사용한 객체 탐지

```python
import requests

url = "http://localhost:8000/api/v1/detect"
files = {"file": open("image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

### Postman 테스트

#### 정상 요청
1. `POST http://localhost:8000/api/v1/detect`
2. Body → form-data
3. Key: `file`, Type: File
4. 이미지 파일 선택 후 Send

#### 예외 처리 테스트
- **파일 없이 요청** → `422 Validation Error`
- **너무 큰 파일 (>10MB)** → `400 Bad Request`
- **잘못된 이미지 형식** → `400 Bad Request`
- **모델 미로드 상태** → `503 Service Unavailable`
- **잘못된 HTTP 메서드** → `405 Method Not Allowed`
- **없는 경로** → `404 Not Found`

## 아키텍처

### 데이터 흐름

```
1. 클라이언트 요청
   ↓
2. FastAPI Router (rtdetr_routers.py)
   - UploadFile 객체 수신
   ↓
3. Controller (rtdetr_controller.py)
   - detect_objects() 호출
   ↓
4. Image Utils (image_utils.py)
   - validate_and_load_image() 비동기 실행
   - 청크 단위(64KB)로 스트림 읽기
   - 파일 크기 검증 (최대 10MB)
   - PIL Image로 변환
   ↓
5. RT-DETR 모델
   - predict() 실행
   - 객체 탐지 수행
   - 결과 파싱 (바운딩 박스, 클래스, 신뢰도)
   ↓
6. 응답 생성
   - DetectionResponse 구성
   - 요약 정보 생성 (총 개수, 클래스별 개수)
   ↓
7. 클라이언트 응답
```

## 모델 설정

RT-DETR 모델은 다음 파라미터로 설정되어 있습니다:

- **모델**: RT-DETR (`rtdetr-l.pt`)
- **Confidence Threshold**: 0.60
- **IoU Threshold**: 0.70
- **Device**: MPS (Apple Silicon) → CUDA (NVIDIA GPU) → CPU (자동 선택)
- **모델 경로**: 환경 변수 `MODEL_PATH`로 설정 가능 (기본값: `rtdetr-l.pt`)

## 에러 처리

API는 FastAPI의 기본 HTTPException을 사용하여 에러를 처리합니다.

### 에러 응답 형식
모든 에러는 다음 형식으로 반환됩니다:
```json
{
  "detail": "에러 메시지"
}
```

### 상태 코드별 에러

| 상태 코드 | 설명 | 발생 상황 |
|---------|------|----------|
| **400** | Bad Request | 빈 파일, 큰 파일(>10MB), 잘못된 이미지 형식 |
| **404** | Not Found | 존재하지 않는 경로 |
| **405** | Method Not Allowed | 허용되지 않는 HTTP 메서드 |
| **422** | Validation Error | 필수 파라미터 누락 (file 없음) |
| **500** | Internal Server Error | 예상치 못한 서버 오류 |
| **503** | Service Unavailable | 모델이 로드되지 않음 |
