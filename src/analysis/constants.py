from enum import Enum
from typing import Final, Dict


class AccountType(Enum):
    CHEQUING = "CHEQUING"
    CREDIT = "CREDIT"


class Institution(Enum):
    CIBC = "CIBC"
    SCOTIABANK = "Scotia"


AccountToTable: Final[Dict[AccountType, str]] = {
    AccountType.CHEQUING: "chequing",
    AccountType.CREDIT: "credit"
}

InstitutionMap: Final[Dict[Institution, str]] = {
    Institution.CIBC: "CIBC",
    Institution.SCOTIABANK: "Scotia"
}

AccountToDataFields: Final[Dict[AccountType, str]] = {
    AccountType.CHEQUING: ["UUID", "Institution", "TransDate", "TransDetails", "Withdrawals", "Deposits"],
    AccountType.CREDIT: ["UUID", "Institution", "TransDate", "TransDetails", "Debts", "Credits", "CardNumber"]
}
