# 커스텀 예외 클래스

class APIException(Exception):
    """
    API 에러용 커스텀 예외

    사용법:
        raise APIException("에러 메시지", 400)  # 상태코드 400
    """
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)
