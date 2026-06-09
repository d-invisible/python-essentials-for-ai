"""Small reusable decorators.

Three patterns:

- `timed`          — plain decorator.
- `memoize`        — plain decorator that holds per-function cache state.
- `retry(times=N)` — decorator factory (decorator with arguments).
"""

from __future__ import annotations

import functools
import time
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def timed(func: Callable[P, R]) -> Callable[P, R]:
    """Print how long `func` takes to execute. Returns the original result."""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            print(f"[timed] {func.__name__} took {elapsed_ms:.2f} ms")

    return wrapper


def memoize(func: Callable[P, R]) -> Callable[P, R]:
    """Cache results by (args, sorted-kwargs). Arguments must be hashable.

    For production code, prefer `functools.lru_cache` — this is the hand-rolled version
    for teaching purposes.
    """
    cache: dict[tuple, R] = {}

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        # Build a hashable key from args and kwargs. Sorting kwargs makes
        # `f(a=1, b=2)` and `f(b=2, a=1)` hit the same cache entry.
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    # Expose the cache for inspection — useful in tests and demos.
    wrapper.cache = cache  # type: ignore[attr-defined]
    return wrapper


def retry(
    times: int = 3,
    delay: float = 0.1,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Retry `func` up to `times` times if it raises any of `exceptions`.

    Re-raises the last exception unchanged after exhausting attempts.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exc: BaseException | None = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    print(f"[retry] {func.__name__} attempt {attempt}/{times} failed: {e}")
                    if attempt < times:
                        time.sleep(delay)
            # We can only reach here if every attempt raised — last_exc is set.
            assert last_exc is not None
            raise last_exc

        return wrapper

    return decorator


# Quick self-test when run directly.
if __name__ == "__main__":
    @timed
    def big_sum(n: int) -> int:
        return sum(range(n))

    @memoize
    def fib(n: int) -> int:
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    @retry(times=3, delay=0.01)
    def always_fails() -> Any:
        raise RuntimeError("nope")

    big_sum(1_000_000)
    print("fib(50) =", fib(50))
    print("memoize cache size:", len(fib.cache))  # type: ignore[attr-defined]
    try:
        always_fails()
    except RuntimeError as e:
        print("retry gave up with:", e)
