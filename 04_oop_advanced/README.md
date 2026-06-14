# 04 — OOP Advanced

The rest of the OOP toolkit. After this folder, the shapes Pydantic models, FastAPI
dependency classes, and agent-tool registries take feel obvious.

## You'll be able to

- Build a class **hierarchy** with inheritance, override methods, and call the parent's
  version with `super()`.
- Reach for **polymorphism** instead of `isinstance(...) / elif`-chains.
- Use **abstract base classes** (`abc.ABC`, `@abstractmethod`) to force subclasses to
  implement a contract.
- Use **`@dataclass`** to skip writing `__init__`, `__repr__`, and `__eq__` for
  data-holding classes.
- Use **`@property`** to expose a *derived* value as if it were an attribute.
- Decide between **inheritance** and **composition** — and default to composition.

## Prerequisites

- [03_oop_basics](../03_oop_basics/README.md) — `__init__`, methods, class vs instance attributes.
- [02_functions_deep](../02_functions_deep/README.md) — decorators (`@dataclass`, `@property`).

## How to work through this folder

| # | File | Format | Why |
|---|------|--------|-----|
| 1 | [01_inheritance.ipynb](01_inheritance.ipynb) | notebook | watching attribute/method lookup walk the MRO is the point |
| 2 | [02_abc_and_polymorphism.ipynb](02_abc_and_polymorphism.ipynb) | notebook | small typed examples are easier to read in cells |
| 3 | [03_dataclasses_and_property.ipynb](03_dataclasses_and_property.ipynb) | notebook | many tiny variants of `@dataclass` |
| 4 | [04_shapes_app/](04_shapes_app/) | `.py` | a small app showing inheritance + ABC + dataclass + composition together |

## Decision flow — inheritance vs composition

```
Does B *behave like* an A (and could be substituted wherever an A is expected)?
├── Yes → inheritance might be right  (Square is a Rectangle? — careful, this often fails)
└── No, B just *uses* an A's services → composition (B has-a A)
```

**Default to composition.** Inheritance is rigid; composition swaps. We'll lean on this
hard once we get to services and FastAPI dependencies (folders 12–14).

## Cheat sheet — `@dataclass` flags you'll use

| Flag | What it does | When |
|------|--------------|------|
| `@dataclass` | generates `__init__`, `__repr__`, `__eq__` | most data-holding classes |
| `frozen=True` | makes instances immutable (and hashable) | value objects, dict keys |
| `slots=True` | uses `__slots__` — less memory, no attribute creation | very-many-of objects |
| `kw_only=True` | all fields must be passed by keyword | classes with many fields |
| `field(default_factory=list)` | per-instance mutable defaults | lists/dicts as defaults |

## Exercises

Add solutions in the matching notebook or in `04_shapes_app/exercises.py`.

1. **`Animal` hierarchy.** Base class `Animal` with abstract `speak()`. Subclasses `Dog`,
   `Cat`, `Cow`. Loop over a list of mixed animals and call `speak()` — polymorphism with
   no `isinstance` in sight.
2. **`Vector` dataclass.** `@dataclass(frozen=True)` with `x: float`, `y: float`. Add
   `__add__`, `__sub__`, and a `@property` `magnitude`. Confirm `frozen=True` makes it
   hashable (try `{Vector(1, 2)}`).
3. **`super()` order.** Construct a 3-level hierarchy (`A → B → C`) where each `__init__`
   calls `super().__init__(...)`. Print something inside each. What order do they run? Why?
4. **Composition refactor.** Take the `BankAccount` class from
   [03_oop_basics/03_bank_account/account.py](../03_oop_basics/03_bank_account/account.py)
   and pull the validation logic out into a separate `AccountValidator` class that
   `BankAccount` *uses* (composition). Does the result feel cleaner? When would it be
   overkill?
5. **`@property` setter.** Add a `@temperature.setter` to a `Sensor` class that rejects
   values below absolute zero. Why is this preferable to a plain attribute + a setter
   method?

## Next topic

After "next learning": **05_typing_and_protocols** — `list[int]`, generics, `Protocol` vs
`ABC`, `typing.Annotated`.
