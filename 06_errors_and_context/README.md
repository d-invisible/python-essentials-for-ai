# 06 — Errors and Context Managers

Two stdlib facilities that show up on every page of real Python code. Done well, they make
your code shorter, safer, and easier to debug. Done poorly, they hide bugs and leak resources.

## You'll be able to

- Read the **built-in exception hierarchy** and pick the right base for a custom exception.
- Use `try / except / else / finally` correctly — and explain what each clause is for.
- Wrap one exception in another with `raise NewError(...) from original` to preserve context.
- Design a **small exception hierarchy** for your own modules instead of leaking generic
  `Exception` everywhere.
- Use `with` statements for any resource that needs guaranteed cleanup.
- Build your own context managers two ways: the **`__enter__` / `__exit__`** protocol and
  the **`@contextmanager`** decorator.

## Prerequisites

- [04_oop_advanced](../04_oop_advanced/README.md) — inheritance (for the exception hierarchy).
- [02_functions_deep](../02_functions_deep/README.md) — decorators (`@contextmanager`).

## How to work through this folder

| # | File | Format | Why |
|---|------|--------|-----|
| 1 | [01_exceptions.ipynb](01_exceptions.ipynb) | notebook | small examples, see each trace |
| 2 | [02_custom_exceptions.ipynb](02_custom_exceptions.ipynb) | notebook | design choices are easier to compare in cells |
| 3 | [03_context_managers.ipynb](03_context_managers.ipynb) | notebook | both context-manager forms side-by-side |
| 4 | [04_file_pipeline/](04_file_pipeline/) | `.py` | a real little tool that ties both together |

## Cheat sheet — `try / except / else / finally`

```python
try:
    do_thing()                # the operation that might raise
except SpecificError as e:    # handle a specific exception
    handle(e)
except (TypeA, TypeB) as e:   # handle several at once
    handle(e)
else:
    # runs ONLY if the try block raised nothing
    after_success()
finally:
    # ALWAYS runs — success, exception, even early return inside try
    cleanup()
```

| Clause | Runs when | Use for |
|---|---|---|
| `try` | always (it's the protected block) | the one operation that might raise |
| `except` | the matching exception fires | recovery / logging / re-raising |
| `else` | the `try` finished without raising | post-success work that *shouldn't* be wrapped in `try` |
| `finally` | every path out of the `try` | cleanup that must happen no matter what |

## Cheat sheet — context managers

| You want | Reach for |
|---|---|
| Open and auto-close a file | `with open(path) as f:` |
| Acquire and release a lock | `with lock:` |
| Time a block of code | a custom `@contextmanager` |
| Suppress a specific exception | `with contextlib.suppress(FileNotFoundError):` |
| Redirect stdout temporarily | `with contextlib.redirect_stdout(buf):` |
| Manage several at once | `with open(a) as f1, open(b) as f2:` |
| Conditional context (sometimes none) | `contextlib.ExitStack` |

## Exercises

Add solutions in the matching notebook or in `04_file_pipeline/exercises.py`.

1. **`safe_int(s, default=None)`** — wraps `int(s)` and returns `default` on `ValueError`.
   Then write `safe_int_strict(s)` that raises a *custom* `ParseError` instead of
   returning a default. When would you prefer each?
2. **Custom exception hierarchy.** Design 3 exceptions for a hypothetical payment
   processor: `PaymentError` (base), `PaymentDeclined`, `PaymentNetworkError`. Show one
   try/except that catches both by catching only the base.
3. **`@contextmanager` `timed(label)`.** Builds on `@timed` from
   [02_functions_deep/04_decorator_module/decorators.py](../02_functions_deep/04_decorator_module/decorators.py)
   but as a *block* — `with timed("loop"): ...` — printing the elapsed time on exit.
4. **Class-based context manager `TempEnv(VAR="x")`.** Sets env vars on enter, restores
   them on exit. Verify it restores even if the block raises.
5. **Reach for `raise ... from`.** Take this code and rewrite it so the original cause is
   preserved:
   ```python
   try:
       data = json.loads(text)
   except json.JSONDecodeError:
       raise ValueError("bad config")    # original exception lost!
   ```
   Why does `from e` matter for debugging?

## Next topic

After "next learning": **07_iterators_generators** — `iter`/`next`, generator functions,
`yield`, `yield from`, lazy pipelines.
