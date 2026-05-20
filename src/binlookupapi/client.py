from __future__ import annotations

import time
from collections.abc import Mapping
from typing import Any

import httpx

from .config import BINLookupClientConfig, normalize_config
from .exceptions import NetworkError, ValidationError, map_api_error
from .models import BINLookupResponse, parse_quota, parse_response_payload
from .retry import retry_delay_seconds, should_retry_status


class BINLookupClient:
    def __init__(
        self,
        config: BINLookupClientConfig | Mapping[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        if isinstance(config, BINLookupClientConfig):
            self._config = config
        else:
            self._config = normalize_config(config, **kwargs)
        self._http = httpx.Client(timeout=self._config.timeout)

    def lookup(self, bin: int | str) -> BINLookupResponse:
        number = self._validate_bin(bin)
        attempts = 0

        while True:
            try:
                response = self._http.post(
                    f"{self._config.baseUrl}/v1/bin",
                    headers={
                        "Authorization": f"Bearer {self._config.apiKey}",
                        "Content-Type": "application/json",
                    },
                    json={"number": int(number)},
                )
            except (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError) as exc:
                delay = retry_delay_seconds(attempts, self._config.maxRetries)
                if delay is None:
                    raise NetworkError(
                        f"Network error: {exc}",
                        code="SERVICE_ERROR",
                    ) from exc
                time.sleep(delay)
                attempts += 1
                continue

            quota = parse_quota(response.headers)

            if response.status_code == 200:
                payload = response.json()
                return parse_response_payload(payload, quota)

            code: str | None = None
            message: str | None = None
            try:
                error_payload = response.json()
                if isinstance(error_payload, dict):
                    code = error_payload.get("error")
                    message = error_payload.get("message")
            except ValueError:
                pass

            error = map_api_error(response.status_code, code, message, quota=quota)
            if should_retry_status(response.status_code):
                retry_after = _parse_retry_after(response.headers.get("Retry-After"))
                delay = retry_delay_seconds(attempts, self._config.maxRetries, retry_after)
                if delay is not None:
                    time.sleep(delay)
                    attempts += 1
                    continue
            raise error

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> BINLookupClient:
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    @staticmethod
    def _validate_bin(value: int | str) -> str:
        if isinstance(value, int):
            normalized = str(value)
        elif isinstance(value, str):
            normalized = value.strip()
        else:
            raise ValidationError(
                "BIN must be an integer or numeric string between 4 and 8 digits",
                code="BAD_REQUEST",
                status_code=400,
            )

        if not normalized.isdigit():
            raise ValidationError(
                "BIN must be an integer or numeric string between 4 and 8 digits",
                code="BAD_REQUEST",
                status_code=400,
            )
        if len(normalized) < 4 or len(normalized) > 8:
            raise ValidationError(
                "BIN must be an integer or numeric string between 4 and 8 digits",
                code="BAD_REQUEST",
                status_code=400,
            )
        return normalized


def _parse_retry_after(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        retry_after = float(value)
    except ValueError:
        return None
    return retry_after if retry_after >= 0 else None
