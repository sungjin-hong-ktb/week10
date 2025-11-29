# 예외 핸들러
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from app.exceptions.custom_exceptions import APIException


async def handle_http_exception(request: Request, exc: HTTPException):
    """
    HTTP 예외 처리 (404, 405 등)
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail
        }
    )


async def handle_api_exception(request: Request, exc: APIException):
    """
    APIException 처리
    -> {"success": false, "error": "이미지가 너무 큽니다"}
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.message
        }
    )


async def handle_validation_error(request: Request, exc: RequestValidationError):
    """
    FastAPI의 검증 에러 처리
    -> {"success": false, "error": "입력값이 올바르지 않습니다"}
    """
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "입력값이 올바르지 않습니다"
        }
    )


async def handle_general_error(request: Request, exc: Exception):
    """
    예상치 못한 모든 에러 처리
    -> {"success": false, "error": "서버 에러가 발생했습니다"}
    """
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "서버 에러가 발생했습니다"
        }
    )