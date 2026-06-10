"""Demo of `BankAccount`.

Run:
    python 03_oop_basics\\03_bank_account\\demo.py
"""

from account import BankAccount


def main() -> None:
    # ---- alternative constructor ----
    alice = BankAccount.open("Alice", currency="EUR")
    bob = BankAccount.open("Bob")  # defaults to USD

    # ---- ordinary instance methods ----
    alice.deposit(500)
    alice.withdraw(75.5)
    bob.deposit(1000)

    # ---- printing via __str__ and __repr__ ----
    print("user-facing (__str__):")
    print(f"  {alice}")
    print(f"  {bob}")
    print()
    print("dev-facing (__repr__):")
    print(f"  {alice!r}")
    print(f"  {bob!r}")
    print()

    # ---- static method usable without an instance ----
    print("'USD' valid? ", BankAccount.is_valid_currency("USD"))
    print("'XYZ' valid? ", BankAccount.is_valid_currency("XYZ"))
    print()

    # ---- class attribute shared across instances ----
    print("accounts opened so far:", BankAccount.total_accounts_opened)

    # ---- demonstrating validation ----
    print()
    print("trying invalid operations:")
    for label, action in [
        ("open with empty owner", lambda: BankAccount("")),
        ("open with negative balance", lambda: BankAccount("Cleo", balance=-1)),
        ("open with bad currency", lambda: BankAccount("Cleo", currency="XYZ")),
        ("withdraw too much", lambda: alice.withdraw(10**6)),
        ("deposit zero", lambda: alice.deposit(0)),
    ]:
        try:
            action()
            print(f"  {label}: (no error — bug!)")
        except ValueError as e:
            print(f"  {label}: rejected -> {e}")


if __name__ == "__main__":
    main()
