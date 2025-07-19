from fastapi import HTTPException, status

class BaseAPIException(HTTPException):
    status_code: int

    def __init__(self, detail: str = None):
        super().__init__(
            status_code=self.status_code,
            detail=detail
        )

class NotFoundException(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND

class BadRequestException(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST

class UnauthorizedException(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED

class ForbiddenException(BaseAPIException):
    status_code = status.HTTP_403_FORBIDDEN