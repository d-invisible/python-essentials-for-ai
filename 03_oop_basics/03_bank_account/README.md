# 03 — A Real Class: `BankAccount`

A small but **production-shaped** OOP example. Demonstrates:

- Validation in `__init__` (rejecting bad state at construction).
- An **alternative constructor** (`@classmethod`).
- A **static utility** (`@staticmethod`) related to the class.
- A **class attribute counter** that tracks how many accounts have been opened.
- A clean `__repr__` and a different `__str__`.

## Files

- [`account.py`](account.py) — the `BankAccount` class.
- [`demo.py`](demo.py) — uses the class.
- [`test_account.py`](test_account.py) — tiny self-test using plain `assert`. We'll convert
  this to **`pytest`** properly in folder `09_testing_with_pytest`.

## Run it

```powershell
python 03_oop_basics\03_bank_account\demo.py
python 03_oop_basics\03_bank_account\test_account.py
```

## Why a "bank account" specifically

It hits every concept naturally:

| Concept | Shows up as |
|---|---|
| `__init__` + validation | reject `balance < 0`, reject empty owner |
| instance method | `deposit`, `withdraw` mutate `self.balance` |
| `@classmethod` | `BankAccount.open(owner)` — alternative constructor |
| `@staticmethod` | `BankAccount.is_valid_currency(code)` |
| class attribute | `total_accounts_opened` counter shared across instances |
| `__repr__` / `__str__` | dev-friendly vs user-friendly views |

## Try this

1. Add a `transfer(self, other: "BankAccount", amount: float)` method. Validate both sides.
2. Add an `@classmethod` `from_dict(cls, data: dict)` so an account can be rehydrated
   from a JSON-like dict. Verify `BankAccount.from_dict(acc.to_dict())` round-trips.
3. Why does `total_accounts_opened` work as an `int` class attribute even though we
   said "no mutable class attributes"? (Hint: `+=` on an `int` is reassignment, not
   mutation. Where does the new value land — on the class or the instance?)
