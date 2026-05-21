import respx
from httpx import Response

from binlookupapi import BINLookupClient


@respx.mock
def test_lookup_success_parses_data_and_quota() -> None:
    route = respx.post("https://api.binlookupapi.com/v1/bin").mock(
        return_value=Response(
            200,
            headers={
                "X-Quota-Limit": "10000",
                "X-Quota-Remaining": "7482",
                "X-Quota-Reset": "1706400000",
            },
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
        )
    )

    client = BINLookupClient(apiKey="test_key")
    result = client.lookup("42467101")

    assert route.called
    assert result.data.scheme == "visa"
    assert result.data.country.name == "POLAND"
    assert result.quota is not None
    assert result.quota.remaining == 7482


@respx.mock
def test_lookup_sends_user_agent_header() -> None:
    route = respx.post("https://api.binlookupapi.com/v1/bin").mock(
        return_value=Response(200, json={"data": {"bin": "424671", "scheme": "visa", "funding": "debit", "brand": "VISA", "category": "CLASSIC", "country": {"code": "US", "name": "USA"}, "issuer": {"name": "BANK", "website": None, "phone": None}, "currency": "USD", "prepaid": False, "commercial": False}})
    )

    client = BINLookupClient(apiKey="test_key")
    client.lookup("424671")

    request = route.calls.last.request
    assert request.headers["user-agent"] == "binlookupapi-python/0.1.0"
