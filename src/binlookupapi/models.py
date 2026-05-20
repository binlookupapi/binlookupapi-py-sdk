from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Country:
    code: str
    name: str


@dataclass(frozen=True)
class Issuer:
    name: str | None
    website: str | None
    phone: str | None


@dataclass(frozen=True)
class BinData:
    bin: str
    scheme: str
    funding: str
    brand: str | None
    category: str | None
    country: Country
    issuer: Issuer
    currency: str | None
    prepaid: bool
    commercial: bool


@dataclass(frozen=True)
class QuotaInfo:
    limit: int | None = None
    remaining: int | None = None
    reset: int | None = None


@dataclass(frozen=True)
class BINLookupResponse:
    data: BinData
    quota: QuotaInfo | None = None


def parse_quota(headers: Any) -> QuotaInfo | None:
    def _to_int(value: str | None) -> int | None:
        if value is None:
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    limit = _to_int(headers.get("X-Quota-Limit"))
    remaining = _to_int(headers.get("X-Quota-Remaining"))
    reset = _to_int(headers.get("X-Quota-Reset"))
    if limit is None and remaining is None and reset is None:
        return None
    return QuotaInfo(limit=limit, remaining=remaining, reset=reset)


def parse_response_payload(payload: dict[str, Any], quota: QuotaInfo | None) -> BINLookupResponse:
    data = payload.get("data")
    if not isinstance(data, dict):
        raise ValueError("Invalid response payload: missing data object")

    country = data.get("country") or {}
    issuer = data.get("issuer") or {}

    return BINLookupResponse(
        data=BinData(
            bin=str(data.get("bin", "")),
            scheme=str(data.get("scheme", "unknown")),
            funding=str(data.get("funding", "unknown")),
            brand=data.get("brand"),
            category=data.get("category"),
            country=Country(
                code=str(country.get("code", "")),
                name=str(country.get("name", "")),
            ),
            issuer=Issuer(
                name=issuer.get("name"),
                website=issuer.get("website"),
                phone=issuer.get("phone"),
            ),
            currency=data.get("currency"),
            prepaid=bool(data.get("prepaid", False)),
            commercial=bool(data.get("commercial", False)),
        ),
        quota=quota,
    )
