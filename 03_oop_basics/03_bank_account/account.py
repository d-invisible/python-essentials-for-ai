"""A small, production-shaped `BankAccount` class.

Demonstrates all of the OOP-basics concepts in one file:
  - validation in __init__
  - instance methods (deposit, withdraw)
  - a @classmethod alternative constructor (open)
  - a @staticmethod utility (is_valid_currency)
  - a class attribute counter (total_accounts_opened)
  - __repr__ vs __str__
"""

from __future__ import annotations


class BankAccount:
    # ---- class attributes (shared across all instances) ----
    # Immutable scalars are safe as class attributes.
    SUPPORTED_CURRENCIES: tuple[str, ...] = ("USD", "EUR", "INR", "GBP")
    total_accounts_opened: int = 0    # bumped each time .open() succeeds

    # ---- construction ----
    def __init__(
        self,
        owner: str,
        balance: float = 0.0,
        currency: str = "USD",
    ) -> None:
        # Validate at construction time so we never build an invalid object.
        if not owner or not owner.strip():
            raise ValueError("owner must be a non-empty string")
        if balance < 0:
            raise ValueError(f"opening balance cannot be negative: {balance}")
        if not BankAccount.is_valid_currency(currency):
            raise ValueError(f"unsupported currency: {currency!r}")

        # Instance attributes — per-account state.
        self.owner = owner.strip()
        self.balance = float(balance)
        self.currency = currency

    # ---- alternative constructor ----
    @classmethod
    def open(cls, owner: str, currency: str = "USD") -> BankAccount:
        """Open a new zero-balance account. Bumps the class-level counter."""
        account = cls(owner=owner, balance=0.0, currency=currency)
        # Reassigning via the class — lands on the class, visible to all.
        cls.total_accounts_opened += 1
        return account

    # ---- static utility ----
    @staticmethod
    def is_valid_currency(code: str) -> bool:
        """Pure check, no instance state needed — hence @staticmethod."""
        return code in BankAccount.SUPPORTED_CURRENCIES

    # ---- instance behavior ----
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError(f"deposit must be positive: {amount}")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError(f"withdraw must be positive: {amount}")
        if amount > self.balance:
            raise ValueError(
                f"insufficient funds: tried to withdraw {amount}, balance is {self.balance}"
            )
        self.balance -= amount

    # ---- printability ----
    def __repr__(self) -> str:
        return (
            f"BankAccount(owner={self.owner!r}, "
            f"balance={self.balance!r}, currency={self.currency!r})"
        )

    def __str__(self) -> str:
        return f"{self.owner}: {self.balance:.2f} {self.currency}"


if __name__ == "__main__":
    # Tiny smoke test when run directly.
    a = BankAccount.open("Alice", "EUR")
    a.deposit(100)
    a.withdraw(30)
    print(repr(a))
    print(a)
    print("accounts opened so far:", BankAccount.total_accounts_opened)
