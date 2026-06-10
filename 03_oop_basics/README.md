# 03 — OOP Basics

Your first real Python classes. We stop short of inheritance and abstract base classes —
those are folder 04. The focus here is on building the **mental model** for what `self`
actually means and the difference between data that lives on an *instance* vs the *class*.

## You'll be able to

- Define a class with `__init__`, attributes, and methods.
- Explain what `self` is and why it's the first parameter.
- Distinguish **instance attributes** (per-object) from **class attributes** (shared).
- Choose between `@classmethod`, `@staticmethod`, and a plain instance method.
- Write `__repr__` and `__str__` so your objects print sanely in logs and notebooks.
- Use **alternative constructors** (the `@classmethod` `from_*` pattern) — the same pattern
  Pydantic, FastAPI dependencies, and most agent frameworks use.

## Prerequisites

- [02_functions_deep](../02_functions_deep/README.md) — decorators (we use `@classmethod` /
  `@staticmethod` here) and `*args`/`**kwargs` (constructor patterns).

## How to work through this folder

| # | File | Format | Why |
|---|------|--------|-----|
| 1 | [01_classes_intro.ipynb](01_classes_intro.ipynb) | notebook | seeing instances + attribute lookup helps |
| 2 | [02_methods.ipynb](02_methods.ipynb) | notebook | class/static/instance differences are easier with print output |
| 3 | [03_bank_account/](03_bank_account/) | `.py` | a real class lives in a `.py` module, not a notebook |

## Cheat sheet — the three method kinds

| | First arg | Knows about | Typical use |
|---|---|---|---|
| **instance method** | `self` | the *instance* | normal behavior using `self.x` |
| **`@classmethod`** | `cls` | the *class* | alternative constructors (`from_dict`, `from_str`) |
| **`@staticmethod`** | — | neither | utility logically grouped with the class but not needing `self`/`cls` |

## Exercises

Add solutions to the matching notebook or to `03_bank_account/exercises.py`.

1. **`Point` class.** With `x`, `y`. Add `__repr__`, a `distance_to(other)` method, and a
   `@classmethod` `origin()` that returns `Point(0, 0)`.
2. **`Rectangle` class.** Constructor takes `width` and `height`. Add `area()`,
   `perimeter()`, and a `@classmethod` `square(side)` that returns a square Rectangle.
3. **Counter as a class.** Re-do the `make_counter` closure from
   [02_functions_deep/02_closures_lambdas.ipynb](../02_functions_deep/02_closures_lambdas.ipynb)
   as a class with a `step()` method. Which is clearer for you? Why?
4. **The class-attribute trap.** Explain what goes wrong:
   ```python
   class Player:
       inventory = []          # class attribute (shared!)
       def add(self, item):
           self.inventory.append(item)
   a = Player(); b = Player()
   a.add("sword")
   print(b.inventory)          # ?
   ```
   Fix it.
5. **`__repr__` discipline.** Add a `__repr__` to your `Point` so that
   `eval(repr(p)) == p` (with `Point` in scope). Why is that a good rule of thumb?

## Next topic

After "next learning": **04_oop_advanced** — inheritance, `super()`, polymorphism,
`@dataclass`, `@property`, composition over inheritance.
