from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BINLookupClientConfig:
    apiKey: str
    baseUrl: str = "https://api.binlookupapi.com"
    maxRetries: int = 5
    timeout: float = 10.0


def normalize_config(
    config: Mapping[str, Any] | None = None, **kwargs: Any
) -> BINLookupClientConfig:
    raw: dict[str, Any] = {}
    if config:
        raw.update(dict(config))
    raw.update(kwargs)

    if "apiKey" not in raw and "api_key" in raw:
        raw["apiKey"] = raw["api_key"]
    if "baseUrl" not in raw and "base_url" in raw:
        raw["baseUrl"] = raw["base_url"]
    if "maxRetries" not in raw and "max_retries" in raw:
        raw["maxRetries"] = raw["max_retries"]

    api_key = raw.get("apiKey")
    if not isinstance(api_key, str) or not api_key.strip():
        raise ValueError("apiKey is required")

    base_url = raw.get("baseUrl", "https://api.binlookupapi.com")
    max_retries = raw.get("maxRetries", 5)
    timeout = raw.get("timeout", 10.0)

    if not isinstance(base_url, str) or not base_url.strip():
        raise ValueError("baseUrl must be a non-empty string")
    if not isinstance(max_retries, int) or max_retries < 0:
        raise ValueError("maxRetries must be an integer >= 0")

    return BINLookupClientConfig(
        apiKey=api_key.strip(),
        baseUrl=base_url.rstrip("/"),
        maxRetries=max_retries,
        timeout=float(timeout),
    )
