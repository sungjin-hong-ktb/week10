# RT-DETR 객체 탐지 API
 
RT-DETR(Real-Time Detection Transformer) 모델을 사용하여 이미지에서 객체를 탐지한 후 총 객채 수, 각 객체의 수를 반환해줍니다.

## 기술 스택

![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Ultralytics](https://img.shields.io/badge/Ultralytics-RT--DETR-0F4C81?style=for-the-badge)
![Pydantic](https://img.shields.io/badge/Pydantic-2.0+-E92063?style=for-the-badge&logo=pydantic&logoColor=white)

## 프로젝트 구조

```
assignment/
├── app/
│   ├── __init__.py
│   ├── controllers/         # 비즈니스 로직
│   │   ├── __init__.py
│   │   └── rtdetr_controller.py
│   ├── models/              # 데이터 모델 및 스키마
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── routers/             # API 엔드포인트
│   │   ├── __init__.py
│   │   └── rtdetr_routers.py
│   └── utils/               # 유틸리티 함수
│       ├── __init__.py
│       └── image_utils.py
├── main.py                  # FastAPI 애플리케이션 진입점
├── requirements.txt         # Python 의존성
├── rtdetr-l.pt              # RT-DETR 모델 가중치
└── .gitignore
```

## 주요 기능

- **객체 탐지**: 이미지를 업로드하여 RT-DETR 모델로 객체 탐지
- **헬스 체크**: 서버 및 모델 로드 상태 확인

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

### 3. 서버 실행

```bash
python main.py
```

또는

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
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
  "docs": "/docs",
  "health": "/api/v1/health"
}
```

### 2. 객체 탐지
```
POST /api/v1/detect
```
이미지 파일을 업로드하여 객체를 탐지합니다.

**요청:**
- Content-Type: `multipart/form-data`
- Body: `file` (이미지 파일)

**응답 예시:**
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
1. POST http://localhost:8000/api/v1/detect
2. Body - form-data
3. Key: file, Type: File
4. 이미지 파일 선택

#### 예외 처리 테스트
- 파일 없이 요청 → 422 Validation Error
- 너무 큰 파일 → 400 Bad Request
- 잘못된 HTTP 메서드 → 405 Method Not Allowed
- 없는 경로 → 404 Not Found

## 아키텍처

### 계층 구조

1. **Routers** (`app/routers/`): API 엔드포인트 정의
2. **Controllers** (`app/controllers/`): 비즈니스 로직 및 모델 처리
3. **Models** (`app/models/`): 데이터 스키마 정의
4. **Utils** (`app/utils/`): 이미지 처리 유틸리티

### 주요 컴포넌트

- **RTDETRController**: RT-DETR 모델 관리 및 객체 탐지 수행
- **Detection Router**: 객체 탐지 및 헬스 체크 엔드포인트
- **Image Utils**: 이미지 검증 및 로드 유틸리티

## 모델 설정

RT-DETR 모델은 다음 파라미터로 설정되어 있습니다:

- **Confidence Threshold**: 0.50
- **IoU Threshold**: 0.70
- **Device**: MPS (Apple Silicon) 또는 CUDA 또는 CPU

## 에러 처리

API는 다음과 같은 에러를 처리합니다:

- **400**: 잘못된 요청 (이미지 형식, 크기 등)
- **404**: 페이지를 찾을 수 없음
- **405**: 허용되지 않는 HTTP 메서드
- **422**: 유효성 검증 실패
- **500**: 서버 내부 오류
- **503**: 모델이 로드되지 않음

## 개발 환경

- Python 3.11+