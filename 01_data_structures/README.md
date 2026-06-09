# 01 — Data Structures

The four built-in containers — **list, tuple, dict, set** — plus the patterns we use to
build and iterate them. This is where you start *thinking* in Python instead of translating
from another language.

## You'll be able to

- Pick the right container for the job (mutable vs immutable, ordered vs not, unique vs not).
- Slice and index sequences confidently — including negative indices and `[a:b:step]`.
- Reach for the idiomatic loop: `enumerate`, `zip`, `dict.items()`, etc.
- Write **comprehensions** for list/dict/set, and know when *not* to.
- Explain Python's reference model — why `b = a` is *not* a copy, and what `copy` / `deepcopy` do.

## Prerequisites

- [00_foundations](../00_foundations/README.md) — especially functions and `for` loops.

## How to work through this folder

Open each notebook in VS Code → kernel **Python (basics_01)**. Run every cell. Predict the
output before you run.

| # | File | What it covers |
|---|------|----------------|
| 1 | [01_lists_and_tuples.ipynb](01_lists_and_tuples.ipynb) | list ops, slicing, tuple, mutability, copy vs reference |
| 2 | [02_dicts_and_sets.ipynb](02_dicts_and_sets.ipynb) | dict ops, set ops, common patterns (counting, grouping, dedup) |
| 3 | [03_comprehensions.ipynb](03_comprehensions.ipynb) | list/dict/set comprehensions, generator expressions, `enumerate`/`zip` patterns |

## Cheat sheet — when to use which

| Need | Use | Why |
|------|-----|-----|
| Ordered, will grow/shrink | `list` | mutable sequence |
| Fixed-size record / heterogeneous fields | `tuple` | immutable, hashable |
| Lookup by key | `dict` | O(1) average get/set |
| Unique items, fast membership test | `set` | O(1) `in`, no duplicates |
| Don't know yet | `list` | safe default; switch later |

## Exercises

Add your solutions as new cells in the matching notebook, or as a new `exercises.py`.

1. **Top-N words.** Given a string, return the N most common words as a list of `(word, count)`
   pairs sorted by count descending. (Hint: `dict` to count, then `sorted(..., key=...)`.)
2. **Invert a dict.** Given `{"a": 1, "b": 2, "c": 1}` produce `{1: ["a", "c"], 2: ["b"]}`.
3. **Set algebra.** Given two lists of user IDs `old` and `new`, return three sets:
   `added`, `removed`, `kept`.
4. **Matrix transpose with `zip`.** `transpose([[1,2,3],[4,5,6]])` should return `[(1,4),(2,5),(3,6)]`
   in one line. (Hint: `zip(*matrix)`.)
5. **Reference trap.** Predict the output, then run it. Explain in one sentence why:
   ```python
   grid = [[0] * 3] * 3
   grid[0][0] = 9
   print(grid)
   ```

## Next topic

After "next learning": **02_functions_deep** — `*args`/`**kwargs`, closures, decorators.
