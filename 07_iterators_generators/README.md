# 07 — Iterators and Generators

How Python's `for` loop actually works, and the cheapest way to process huge or infinite
streams of data without filling memory.

## You'll be able to

- Explain the **iterator protocol** (`__iter__`, `__next__`, `StopIteration`) and write
  a custom iterator class.
- Write **generator functions** with `yield` — and explain how they're "paused functions."
- Use **generator expressions** for lazy sequences (`(x*x for x in xs)`).
- Compose generators into **lazy pipelines** — read, parse, filter, transform without
  ever building a full list.
- Use `yield from` to delegate to a sub-generator.

## Prerequisites

- [01_data_structures](../01_data_structures/README.md) — comprehensions (the eager
  cousins of generator expressions).
- [06_errors_and_context](../06_errors_and_context/README.md) — `StopIteration` is an
  exception; understanding exceptions makes the protocol obvious.

## How to work through this folder

| # | File | Format | Why |
|---|------|--------|-----|
| 1 | [01_iter_next.ipynb](01_iter_next.ipynb) | notebook | small live experiments with `next()` |
| 2 | [02_generators.ipynb](02_generators.ipynb) | notebook | watching `yield` pause/resume is the point |
| 3 | [03_lazy_pipelines.ipynb](03_lazy_pipelines.ipynb) | notebook | many tiny stages, see them compose |
| 4 | [04_event_pipeline/](04_event_pipeline/) | `.py` | a real pipeline (read → parse → filter → aggregate) wired up in code |

## Cheat sheet — list vs generator

| | List comprehension `[...]` | Generator expression `(...)` |
|---|---|---|
| Builds all values up front | yes | no — produces them one at a time |
| Memory | O(n) | O(1) per yield |
| Re-iterable | yes | **no** — once consumed, it's exhausted |
| Indexable | yes (`xs[0]`) | no (you'd have to convert) |
| Good for | results you'll use multiple times | feed into `sum`, `any`, `all`, `max`, file streaming |

## Cheat sheet — when to write a generator

- The data **doesn't fit in memory** (log files, DB cursors, large API pages).
- You want a **lazy pipeline** that quits early (`any`, `next`, `break`).
- You're modeling a **stream** of events, not a finite collection.
- You want a function that's *naturally paused* between calls (think coroutines).

Otherwise, a list is fine — clarity beats cleverness.

## Exercises

Add solutions in the matching notebook or in `04_event_pipeline/exercises.py`.

1. **`countdown(n)`** — generator that yields `n, n-1, ..., 1, "GO!"`. (Mix int and str
   yields — what's the natural return type? `int | str` works.)
2. **`take(n, it)`** — yield the first `n` items of any iterable. Use it to slice an
   infinite generator without converting to a list first.
3. **`flatten(nested)`** — yield every leaf from an arbitrarily-nested list. Use
   `yield from` recursively.
4. **Real lazy pipeline.** Given any text source (a hard-coded multiline string is fine),
   build a pipeline: `read_lines → strip_blanks_and_comments → parse_int → filter > 0 →
   sum`. Each step is a separate generator function. Confirm intermediate lists are never
   built.
5. **The gotcha.** Predict what happens, then run:
   ```python
   xs = (i for i in range(3))
   print(list(xs))     # ?
   print(list(xs))     # ?
   ```
   What's the lesson?

## Next topic

After "next learning": **08_modules_and_packages** — package layout, relative vs absolute
imports, `__init__.py`, `src/` layout, running with `python -m`.
