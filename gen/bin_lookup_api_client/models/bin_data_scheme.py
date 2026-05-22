from enum import Enum


class BinDataScheme(str, Enum):
    AMEX = "amex"
    DINERS = "diners"
    DISCOVER = "discover"
    JCB = "jcb"
    MASTERCARD = "mastercard"
    UNIONPAY = "unionpay"
    UNKNOWN = "unknown"
    VISA = "visa"

    def __str__(self) -> str:
        return str(self.value)
