from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base class for business errors. Subclass it and set status_code + code."""

    status_code = 500
    code = "internal_error"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class AccountNotFoundError(AppError):
    status_code = 404
    code = "account_not_found"


class FeatureNotImplementedError(AppError):
    """Raised by the placeholder services. Remove usages as you build each feature."""

    status_code = 501
    code = "not_implemented"


async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )
