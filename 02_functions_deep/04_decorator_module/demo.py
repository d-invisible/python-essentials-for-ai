"""Demo of the three decorators in `decorators.py`.

Run:

    python 02_functions_deep\\04_decorator_module\\demo.py
"""

import random

from decorators import memoize, retry, timed


@timed
def warm_up(n: int) -> int:
    """Sum 0..n-1 to give @timed something to measure."""
    return sum(range(n))


@memoize
def fib(n: int) -> int:
    """Fibonacci with naive recursion — fast only because of @memoize."""
    return n if n < 2 else fib(n - 1) + fib(n - 2)


@retry(times=4, delay=0.05)
def flaky(success_rate: float) -> str:
    """Succeeds with probability `success_rate`, otherwise raises."""
    if random.random() < success_rate:
        return "ok"
    raise RuntimeError("transient failure")


def main() -> None:
    print("--- @timed ---")
    warm_up(1_000_000)
    warm_up(5_000_000)

    print("\n--- @memoize ---")
    # fib(200) would never finish without memoization.
    print("fib(200) =", fib(200))
    print("cache entries:", len(fib.cache))  # type: ignore[attr-defined]
    # Names are preserved thanks to functools.wraps:
    print("fib.__name__ =", fib.__name__)
    print("fib.__doc__  =", fib.__doc__)

    print("\n--- @retry ---")
    random.seed(42)
    print("eventually succeeds:", flaky(0.4))

    random.seed(0)
    try:
        flaky(0.0)        # always fails
    except RuntimeError as e:
        print("gave up after retries with:", e)


if __name__ == "__main__":
    main()
