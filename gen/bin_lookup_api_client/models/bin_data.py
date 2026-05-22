from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.bin_data_funding import BinDataFunding
from ..models.bin_data_scheme import BinDataScheme
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.country import Country
    from ..models.issuer import Issuer


T = TypeVar("T", bound="BinData")


@_attrs_define
class BinData:
    """
    Attributes:
        bin_ (str): The BIN that was looked up Example: 42467101.
        scheme (BinDataScheme): Card network Example: visa.
        funding (BinDataFunding): Funding type Example: debit.
        country (Country):
        issuer (Issuer):
        prepaid (bool): Whether the card is prepaid
        commercial (bool): Whether the card is a commercial/business card
        brand (None | str | Unset): Card brand or product name Example: VISA.
        category (None | str | Unset): Card category Example: CLASSIC.
        currency (None | str | Unset): ISO 4217 currency code Example: PLN.
    """

    bin_: str
    scheme: BinDataScheme
    funding: BinDataFunding
    country: Country
    issuer: Issuer
    prepaid: bool
    commercial: bool
    brand: None | str | Unset = UNSET
    category: None | str | Unset = UNSET
    currency: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bin_ = self.bin_

        scheme = self.scheme.value

        funding = self.funding.value

        country = self.country.to_dict()

        issuer = self.issuer.to_dict()

        prepaid = self.prepaid

        commercial = self.commercial

        brand: None | str | Unset
        if isinstance(self.brand, Unset):
            brand = UNSET
        else:
            brand = self.brand

        category: None | str | Unset
        if isinstance(self.category, Unset):
            category = UNSET
        else:
            category = self.category

        currency: None | str | Unset
        if isinstance(self.currency, Unset):
            currency = UNSET
        else:
            currency = self.currency

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bin": bin_,
                "scheme": scheme,
                "funding": funding,
                "country": country,
                "issuer": issuer,
                "prepaid": prepaid,
                "commercial": commercial,
            }
        )
        if brand is not UNSET:
            field_dict["brand"] = brand
        if category is not UNSET:
            field_dict["category"] = category
        if currency is not UNSET:
            field_dict["currency"] = currency

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.country import Country
        from ..models.issuer import Issuer

        d = dict(src_dict)
        bin_ = d.pop("bin")

        scheme = BinDataScheme(d.pop("scheme"))

        funding = BinDataFunding(d.pop("funding"))

        country = Country.from_dict(d.pop("country"))

        issuer = Issuer.from_dict(d.pop("issuer"))

        prepaid = d.pop("prepaid")

        commercial = d.pop("commercial")

        def _parse_brand(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        brand = _parse_brand(d.pop("brand", UNSET))

        def _parse_category(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        category = _parse_category(d.pop("category", UNSET))

        def _parse_currency(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        currency = _parse_currency(d.pop("currency", UNSET))

        bin_data = cls(
            bin_=bin_,
            scheme=scheme,
            funding=funding,
            country=country,
            issuer=issuer,
            prepaid=prepaid,
            commercial=commercial,
            brand=brand,
            category=category,
            currency=currency,
        )

        bin_data.additional_properties = d
        return bin_data

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
