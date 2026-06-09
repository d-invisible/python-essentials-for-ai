# 02 — Functions Deep

Everything `def` can do beyond the basics. After this folder, function signatures and
decorators in FastAPI / Pydantic / agent frameworks should look obvious.

## You'll be able to

- Write flexible function signatures with `*args`, `**kwargs`, positional-only (`/`), and keyword-only (`*`).
- Unpack iterables and mappings into calls (`f(*xs, **kw)`).
- Explain *first-class functions* and write **closures** that capture variables correctly (including the `nonlocal` keyword).
- Write a decorator from scratch — both the plain form and the *decorator-with-arguments* form.
- Use `functools.wraps` so your decorators don't break introspection.

## Prerequisites

- [00_foundations](../00_foundations/README.md) — `def`, return values, scope.
- [01_data_structures](../01_data_structures/README.md) — tuples and dicts (since `*args` is a tuple and `**kwargs` is a dict).

## How to work through this folder

| # | File | Format | Why |
|---|------|--------|-----|
| 1 | [01_args_kwargs.ipynb](01_args_kwargs.ipynb) | notebook | many tiny call examples to observe |
| 2 | [02_closures_lambdas.ipynb](02_closures_lambdas.ipynb) | notebook | seeing variable capture is the point |
| 3 | [03_decorators.ipynb](03_decorators.ipynb) | notebook | build them up step by step |
| 4 | [04_decorator_module/](04_decorator_module/) | `.py` | a real reusable decorator library |

## Why this matters for what's next

- **OOP / dataclasses** (folders 03–04) lean on `__init__(self, *args, **kwargs)` patterns.
- **FastAPI** routes are decorated functions (`@app.get(...)`) with rich keyword-only params.
- **Pydantic** validators are decorated methods.
- **Agent frameworks** wrap tools/functions with decorators to register them.

If decorators feel mysterious now, they will be *everywhere* by folder 13.

## Exercises

Add solutions in the matching notebook, or in `exercises.py`.

1. **Flexible logger.** Write `log(*args, sep=" | ", level="INFO", **fields)` that prints
   `[LEVEL] arg1 | arg2 | key=value | key=value`. Call it three different ways.
2. **Counter closure.** Write `make_counter(start=0)` that returns a function `next_val()`
   which, each time it's called, returns the next integer. (Hint: `nonlocal`.)
3. **`@timed` decorator.** Write a decorator that prints how long the wrapped function took
   to run. Don't lose the wrapped function's name or docstring — use `functools.wraps`.
4. **`@retry(times=N)` decorator.** Write a decorator that takes an argument and retries
   the wrapped function up to `N` times on any exception. Sleep 0.1s between attempts.
5. **What's printed?** Predict, then run:
   ```python
   funcs = [lambda: i for i in range(3)]
   print([f() for f in funcs])
   ```
   Then fix it so the output is `[0, 1, 2]`.

## Next topic

After "next learning": **03_oop_basics** — classes, `__init__`, `self`, methods, `@classmethod`/`@staticmethod`.
