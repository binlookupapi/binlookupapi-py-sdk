from unittest.mock import patch

import pytest
import respx
from httpx import Response

from binlookupapi import BINLookupAPIError, BINLookupClient


@respx.mock
def test_lookup_retries_then_succeeds() -> None:
    route = respx.post("https://api.binlookupapi.com/v1/bin")
    route.side_effect = [
        Response(502, json={"error": "SERVICE_ERROR", "message": "Try again"}),
        Response(
            200,
            json={
                "data": {
                    "bin": "42467101",
                    "scheme": "visa",
                    "funding": "debit",
                    "brand": "VISA",
                    "category": "CLASSIC",
                    "country": {"code": "PL", "name": "POLAND"},
                    "issuer": {"name": "ING BANK SLASKI SA", "website": None, "phone": None},
                    "currency": "PLN",
                    "prepaid": False,
                    "commercial": False,
                }
            },
        ),
    ]

    client = BINLookupClient(apiKey="test_key", maxRetries=5)
    with patch("binlookupapi.client.time.sleep") as sleep_mock:
        result = client.lookup("42467101")

    assert route.call_count == 2
    assert result.data.bin == "42467101"
    sleep_mock.assert_called_once_with(1.0)


@respx.mock
def test_lookup_stops_after_max_retries() -> None:
    respx.post("https://api.binlookupapi.com/v1/bin").mock(
        return_value=Response(502, json={"error": "SERVICE_ERROR", "message": "Try again"})
    )

    client = BINLookupClient(apiKey="test_key", maxRetries=1)
    with patch("binlookupapi.client.time.sleep") as sleep_mock:
        with pytest.raises(BINLookupAPIError):
            client.lookup("42467101")

    sleep_mock.assert_called_once_with(1.0)
