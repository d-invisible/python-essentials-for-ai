"""Tiny self-test for `BankAccount`.

Uses plain `assert` for now so this folder has zero dependencies. We'll convert
these tests to `pytest` in folder 09_testing_with_pytest.

Run:
    python 03_oop_basics\\03_bank_account\\test_account.py
"""

from account import BankAccount


def test_construction_validates() -> None:
    # Happy path
    a = BankAccount("Alice", balance=100, currency="USD")
    assert a.owner == "Alice"
    assert a.balance == 100.0
    assert a.currency == "USD"

    # Owner cannot be blank
    for bad_owner in ["", "   ", None]:  # type: ignore[list-item]
        try:
            BankAccount(bad_owner)  # type: ignore[arg-type]
        except (ValueError, AttributeError):
            pass
        else:
            raise AssertionError(f"expected error for owner={bad_owner!r}")

    # Negative balance rejected
    try:
        BankAccount("Bob", balance=-1)
    except ValueError:
        pass
    else:
        raise AssertionError("negative balance should have been rejected")

    # Unsupported currency rejected
    try:
        BankAccount("Bob", currency="XYZ")
    except ValueError:
        pass
    else:
        raise AssertionError("unsupported currency should have been rejected")


def test_deposit_withdraw() -> None:
    a = BankAccount("Alice", balance=100)
    a.deposit(50)
    assert a.balance == 150
    a.withdraw(30)
    assert a.balance == 120

    # Withdraw more than balance
    try:
        a.withdraw(10_000)
    except ValueError:
        pass
    else:
        raise AssertionError("over-withdraw should have been rejected")

    # Non-positive amounts
    for bad in [0, -5]:
        try:
            a.deposit(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"deposit({bad}) should have been rejected")


def test_classmethod_open_bumps_counter() -> None:
    # Snapshot the counter so this test is independent of order.
    before = BankAccount.total_accounts_opened
    BankAccount.open("Cleo")
    BankAccount.open("Dan", currency="INR")
    after = BankAccount.total_accounts_opened
    assert after - before == 2, f"counter should increase by 2, got {after - before}"


def test_staticmethod_currency_check() -> None:
    # No instance needed.
    assert BankAccount.is_valid_currency("USD") is True
    assert BankAccount.is_valid_currency("XYZ") is False


def test_repr_and_str() -> None:
    a = BankAccount("Alice", balance=42.5, currency="EUR")
    # __repr__ should mention class name and key fields
    r = repr(a)
    assert "BankAccount" in r and "Alice" in r and "EUR" in r
    # __str__ should be user-friendly (and different)
    s = str(a)
    assert s == "Alice: 42.50 EUR"


def main() -> None:
    tests = [
        test_construction_validates,
        test_deposit_withdraw,
        test_classmethod_open_bumps_counter,
        test_staticmethod_currency_check,
        test_repr_and_str,
    ]
    for t in tests:
        t()
        print(f"  ok  {t.__name__}")
    print(f"\n{len(tests)} tests passed.")


if __name__ == "__main__":
    main()
