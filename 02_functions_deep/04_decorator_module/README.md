# 04 — A Real Decorator Module

Until now decorators have lived inside notebook cells. Real decorators belong in a `.py`
module that other code can `import`. This folder is the smallest realistic version of
that — three decorators you'll keep reaching for.

## Files

- [`decorators.py`](decorators.py) — `@timed`, `@memoize`, `@retry(times=...)`.
- [`demo.py`](demo.py) — imports and demonstrates each.

## Run it

```powershell
python 02_functions_deep\04_decorator_module\demo.py
```

You should see output from all three decorators in turn.

## Why these three

- **`@timed`** — the simplest *plain* decorator. Demonstrates the shape and `functools.wraps`.
- **`@memoize`** — shows a decorator that *stores state* (a cache dict) per wrapped function.
  This is what `functools.lru_cache` does, hand-rolled.
- **`@retry(times=...)`** — shows the **decorator with arguments** pattern: an extra
  function layer because you call the decorator *before* applying it.

## Try this

1. Add a `@deprecated(reason: str)` decorator that prints a warning the first time the
   wrapped function is called (use a closure or `functools.lru_cache(maxsize=1)` for the
   "first time" flag).
2. The current `@memoize` won't work on a function with `dict` arguments — why? Add a test
   that demonstrates the failure. (Hint: hashability.)
3. Make `@retry` re-raise the *original* exception type, not a generic one — verify by
   asserting `pytest.raises(SpecificError)` on a failure case (we'll properly use `pytest`
   in folder 09).
