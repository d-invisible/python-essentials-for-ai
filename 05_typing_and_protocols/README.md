# 05 — Typing and Protocols

Where type hints stop being decoration and start catching real bugs. We add **mypy** here
so you can run a real type-checker against your code — without it, hints are vibes.

## You'll be able to

- Annotate variables, functions, and class attributes with everything from `list[int]`
  through `dict[str, list[User]]`, `Optional[X]`, and `X | None`.
- Write **generic** functions and classes with `TypeVar` and `Generic` (e.g. a typed cache).
- Choose between **`abc.ABC`** (nominal subtyping — declared inheritance) and
  **`Protocol`** (structural subtyping — duck-typed but checked).
- Add metadata to a type with `typing.Annotated` — the foundation under FastAPI's
  `Depends(...)` and Pydantic's `Field(...)`.
- Run `mypy` against a module and read its output.

## Prerequisites

- [03_oop_basics](../03_oop_basics/README.md) + [04_oop_advanced](../04_oop_advanced/README.md) — classes, ABCs, dataclasses.

## How to work through this folder

| # | File | Format | Why |
|---|------|--------|-----|
| 1 | [01_typing_basics.ipynb](01_typing_basics.ipynb) | notebook | many small examples, see each one |
| 2 | [02_generics.ipynb](02_generics.ipynb) | notebook | TypeVar / Generic in tiny pieces |
| 3 | [03_protocol_vs_abc.ipynb](03_protocol_vs_abc.ipynb) | notebook | structural vs nominal — easier with cells |
| 4 | [04_repository_protocol/](04_repository_protocol/) | `.py` | a Protocol-based repository pattern — preview of DI (folder 12) |

## Run the type checker

mypy is now installed in `.venv`. From the project root:

```powershell
.venv\Scripts\python.exe -m mypy 05_typing_and_protocols\04_repository_protocol
```

The `04_repository_protocol/` folder should type-check cleanly. The `.py` files include
a few intentionally-broken examples (clearly labelled) so you can *see* mypy fail.

## Cheat sheet — modern Python type hints (3.10+)

| Concept | Modern form | Older form (still seen) |
|---|---|---|
| list of ints | `list[int]` | `List[int]` (from typing) |
| dict | `dict[str, User]` | `Dict[str, User]` |
| optional | `User \| None` | `Optional[User]` |
| union | `int \| str` | `Union[int, str]` |
| callable | `Callable[[int, str], bool]` | same |
| any | `Any` | `Any` |
| no return | `-> None` | `-> None` |
| never returns | `-> Never` | `-> NoReturn` |

Use the modern forms in new code. We allow the old forms when reading older codebases.

## Exercises

Add solutions in the matching notebook or in `04_repository_protocol/exercises.py`.

1. **Typed `pick`.** Write `pick(d: dict[K, V], *keys: K) -> dict[K, V]` with proper generic
   parameters. Make sure `mypy --strict` is happy.
2. **`Cache[K, V]` class.** A `@dataclass` generic cache. Methods: `get(k) -> V | None`,
   `set(k, v) -> None`, `clear() -> None`. Verify a `Cache[str, int]` rejects passing a
   `Cache[str, int].set("k", "v")` via mypy.
3. **`SupportsArea` protocol.** Replace the `Shape` ABC from
   [04_oop_advanced/04_shapes_app/shapes.py](../04_oop_advanced/04_shapes_app/shapes.py)
   with a `Protocol`. Does the existing `Canvas` still work without `isinstance` checks
   on Shape? Why?
4. **`Annotated` metadata.** Write `validate_positive(x: Annotated[int, "must be > 0"])`.
   How does FastAPI use the same pattern via `Depends`? (Foreshadowing folder 13.)
5. **Break it, watch mypy bark.** Take one type-correct function from this folder and
   introduce a bug (`return None` where `int` is expected, mix a `str` into a `list[int]`).
   Run mypy and read the error. This is the muscle you want.

## Next topic

After "next learning": **06_errors_and_context** — exceptions, custom exceptions, context
managers, `with`.
