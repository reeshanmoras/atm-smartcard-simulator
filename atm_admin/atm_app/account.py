# atm_app/account.py

from datetime import datetime


class Account:
    """
    Simple bank account representation.
    """

    def __init__(self, acc_no: str, name: str, pin: str, balance: float = 0.0):
        self.acc_no = acc_no
        self.name = name
        self.pin = pin
        self.balance = balance
        self.created_at = datetime.now()

    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            return False
        self.balance += amount
        return True

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            return False
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def to_dict(self) -> dict:
        return {
            "acc_no": self.acc_no,
            "name": self.name,
            "pin": self.pin,
            "balance": self.balance,
            "created_at": self.created_at.isoformat(timespec="seconds"),
        }

    @staticmethod
    def from_dict(d: dict) -> "Account":
        acc = Account(
            acc_no=d["acc_no"],
            name=d["name"],
            pin=d["pin"],
            balance=float(d["balance"]),
        )
        # created_at is not strictly needed for logic; we keep it if present
        return acc
