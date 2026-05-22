from enum import Enum


class BinDataFunding(str, Enum):
    CREDIT = "credit"
    DEBIT = "debit"
    PREPAID = "prepaid"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
