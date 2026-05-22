from enum import Enum


class ErrorResponseError(str, Enum):
    BAD_REQUEST = "BAD_REQUEST"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    PAYMENT_REQUIRED = "PAYMENT_REQUIRED"
    QUOTA_EXCEEDED = "QUOTA_EXCEEDED"
    SERVICE_ERROR = "SERVICE_ERROR"
    UNAUTHORIZED = "UNAUTHORIZED"

    def __str__(self) -> str:
        return str(self.value)
