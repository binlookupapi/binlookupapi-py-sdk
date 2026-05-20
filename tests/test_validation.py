import pytest

from binlookupapi import BINLookupClient, ValidationError


def test_lookup_rejects_non_numeric_bin() -> None:
    client = BINLookupClient(apiKey="test_key")
    with pytest.raises(ValidationError):
        client.lookup("4246ABCD")


def test_lookup_rejects_short_bin() -> None:
    client = BINLookupClient(apiKey="test_key")
    with pytest.raises(ValidationError):
        client.lookup("123")
