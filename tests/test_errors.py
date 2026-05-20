import pytest
import respx
from httpx import Response

from binlookupapi import BINLookupAPIError, BINLookupClient


@respx.mock
def test_lookup_raises_api_error_with_code() -> None:
    respx.post("https://api.binlookupapi.com/v1/bin").mock(
        return_value=Response(
            401,
            json={
                "error": "UNAUTHORIZED",
                "message": "Missing, invalid, revoked, or expired API key",
            },
        )
    )

    client = BINLookupClient(apiKey="bad_key")
    with pytest.raises(BINLookupAPIError) as err:
        client.lookup("42467101")

    assert err.value.code == "UNAUTHORIZED"
    assert err.value.status_code == 401


@respx.mock
def test_quota_error_includes_quota_metadata() -> None:
    respx.post("https://api.binlookupapi.com/v1/bin").mock(
        return_value=Response(
            429,
            headers={
                "X-Quota-Limit": "500",
                "X-Quota-Remaining": "0",
                "X-Quota-Reset": "1706400000",
            },
            json={
                "error": "QUOTA_EXCEEDED",
                "message": "Daily request quota exceeded",
            },
        )
    )

    client = BINLookupClient(apiKey="test_key", maxRetries=0)
    with pytest.raises(BINLookupAPIError) as err:
        client.lookup("42467101")

    assert err.value.code == "QUOTA_EXCEEDED"
    assert err.value.quota is not None
    assert err.value.quota.remaining == 0
