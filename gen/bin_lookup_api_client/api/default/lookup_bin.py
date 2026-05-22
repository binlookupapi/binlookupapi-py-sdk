from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bin_lookup_request import BinLookupRequest
from ...models.bin_lookup_response import BinLookupResponse
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    *,
    body: BinLookupRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/bin",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> BinLookupResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = BinLookupResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 402:
        response_402 = ErrorResponse.from_dict(response.json())

        return response_402

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429

    if response.status_code == 502:
        response_502 = ErrorResponse.from_dict(response.json())

        return response_502

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[BinLookupResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: BinLookupRequest,
) -> Response[BinLookupResponse | ErrorResponse]:
    """Look up a BIN

     Returns card metadata for a given Bank Identification Number (BIN) — the first 4 to 8
    digits of a payment card number. Use 8 digits when available for better accuracy.

    Args:
        body (BinLookupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BinLookupResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: BinLookupRequest,
) -> BinLookupResponse | ErrorResponse | None:
    """Look up a BIN

     Returns card metadata for a given Bank Identification Number (BIN) — the first 4 to 8
    digits of a payment card number. Use 8 digits when available for better accuracy.

    Args:
        body (BinLookupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BinLookupResponse | ErrorResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: BinLookupRequest,
) -> Response[BinLookupResponse | ErrorResponse]:
    """Look up a BIN

     Returns card metadata for a given Bank Identification Number (BIN) — the first 4 to 8
    digits of a payment card number. Use 8 digits when available for better accuracy.

    Args:
        body (BinLookupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BinLookupResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: BinLookupRequest,
) -> BinLookupResponse | ErrorResponse | None:
    """Look up a BIN

     Returns card metadata for a given Bank Identification Number (BIN) — the first 4 to 8
    digits of a payment card number. Use 8 digits when available for better accuracy.

    Args:
        body (BinLookupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BinLookupResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
