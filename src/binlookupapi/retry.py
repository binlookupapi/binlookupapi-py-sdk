from __future__ import annotations

RETRY_DELAYS_SECONDS = (1, 2, 4, 8, 16)


def should_retry_status(status_code: int) -> bool:
    return status_code == 429 or status_code >= 500


def retry_delay_seconds(
    attempt: int, max_retries: int, retry_after_seconds: float | None = None
) -> float | None:
    if attempt >= max_retries:
        return None
    if retry_after_seconds is not None and retry_after_seconds > 0:
        return retry_after_seconds
    if attempt < len(RETRY_DELAYS_SECONDS):
        return float(RETRY_DELAYS_SECONDS[attempt])
    return float(RETRY_DELAYS_SECONDS[-1])
