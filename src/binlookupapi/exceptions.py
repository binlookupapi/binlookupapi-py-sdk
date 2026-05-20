from __future__ import annotations

from .models import QuotaInfo


class BINLookupAPIError(Exception):
    def __init__(
        self,
        message: str,
        *,
        code: str = "UNKNOWN_ERROR",
        status_code: int | None = None,
        quota: QuotaInfo | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.status_code = status_code
        self.quota = quota


class ValidationError(BINLookupAPIError):
    pass


class NetworkError(BINLookupAPIError):
    pass


def map_api_error(
    status_code: int,
    code: str | None,
    message: str | None,
    *,
    quota: QuotaInfo | None = None,
) -> BINLookupAPIError:
    normalized_code = code or _default_code_for_status(status_code)
    normalized_message = message or "Request failed"
    return BINLookupAPIError(
        normalized_message,
        code=normalized_code,
        status_code=status_code,
        quota=quota,
    )


def _default_code_for_status(status_code: int) -> str:
    return {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        402: "PAYMENT_REQUIRED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        429: "QUOTA_EXCEEDED",
        502: "SERVICE_ERROR",
    }.get(status_code, "UNKNOWN_ERROR")
