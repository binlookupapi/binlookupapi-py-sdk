# BINLookupAPI Python SDK

A production-ready, typed Python SDK for [BINLookupAPI.com](https://binlookupapi.com). Retrieve card network, issuer, country, funding, and quota information from Bank Identification Numbers (BINs).

## Features

- Type hints for request and response objects.
- Resilient retry logic with fixed exponential delays: `1s, 2s, 4s, 8s, 16s`.
- Detailed error handling with `BINLookupAPIError` and API error codes.
- Quota monitoring via `X-Quota-Limit`, `X-Quota-Remaining`, and `X-Quota-Reset`.

## Installation

```bash
pip install binlookupapi
```

## Quick Start

Sign up and get your free API key: <https://app.binlookupapi.com/sign-in>

```python
from binlookupapi import BINLookupAPIError, BINLookupClient

client = BINLookupClient(apiKey="your_api_key_here")

try:
    result = client.lookup("42467101")

    print(f"Scheme: {result.data.scheme}")
    print(f"Bank: {result.data.issuer.name}")
    print(f"Country: {result.data.country.name}")
    print(f"Quota remaining: {result.quota.remaining if result.quota else None}")
except BINLookupAPIError as error:
    print(f"API Error [{error.code}]: {error}")
finally:
    client.close()
```

## Configuration

`BINLookupClient` accepts TypeScript-parity options:

- `apiKey` (`str`, required): your API key.
- `baseUrl` (`str`, default: `https://api.binlookupapi.com`): optional custom endpoint.
- `maxRetries` (`int`, default: `5`): max retries for transient errors.

Python-style aliases are also supported:
- `api_key`, `base_url`, `max_retries`

## API Reference

### `lookup(bin: int | str) -> BINLookupResponse`

Performs a `POST` request to `/v1/bin`. BIN must be between 4 and 8 digits.

### `BINLookupResponse`

- `data.bin`
- `data.scheme`
- `data.funding`
- `data.brand`
- `data.category`
- `data.country.code`
- `data.country.name`
- `data.issuer.name`
- `data.issuer.website`
- `data.issuer.phone`
- `data.currency`
- `data.prepaid`
- `data.commercial`
- `quota.limit`
- `quota.remaining`
- `quota.reset`

## Error Handling

The SDK raises `BINLookupAPIError` for non-200 API responses.

Common `error.code` values:
- `BAD_REQUEST`
- `UNAUTHORIZED`
- `PAYMENT_REQUIRED`
- `FORBIDDEN`
- `NOT_FOUND`
- `QUOTA_EXCEEDED`
- `SERVICE_ERROR`

## Best Practices

- Cache BIN results for 24 to 48 hours.
- Use environment variables for API keys.
- Prefer 8-digit BINs for best accuracy.
