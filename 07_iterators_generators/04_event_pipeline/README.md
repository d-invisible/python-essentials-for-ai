# 04 — Event Pipeline: generators in a real module

A small `.py` module that processes a stream of log-like events through a chain of
generator stages. Demonstrates that the same shape we used in the notebook scales to a
real module with types and tests.

## Files

- [`pipeline.py`](pipeline.py) — `Event` dataclass + every stage as a typed generator (`Iterator[Event] → Iterator[Event]`) plus an `aggregate()` terminal.
- [`demo.py`](demo.py) — runs the pipeline on a small in-memory stream and prints the aggregate.
- [`test_pipeline.py`](test_pipeline.py) — assert-based tests.

## Run it

```powershell
python 07_iterators_generators\04_event_pipeline\demo.py
python 07_iterators_generators\04_event_pipeline\test_pipeline.py
```

And mypy:

```powershell
.venv\Scripts\python.exe -m mypy 07_iterators_generators\04_event_pipeline
```

## What this demonstrates

| Concept | Where |
|---|---|
| Typed generator stage | every `def stage(...) -> Iterator[Event]` in `pipeline.py` |
| `yield from` for a sub-stream | `from_records(...)` |
| `try/finally` cleanup inside a generator | `from_records(...)` prints a "drained" line on completion |
| Composing many stages | `Pipeline.build()` chains them |
| Terminal step | `aggregate(events)` consumes the pipeline into a result |
| Early-exit consumer | `find_first(pipeline, predicate)` uses `next` |

## Pattern: stages are just functions

Each stage has the type `Iterator[Event] → Iterator[Event]`. That means:

- Stages compose by **function call**: `parse(filter(strip(read())))`.
- Stages are **trivial to test**: feed a small list in, assert the list out.
- Adding a stage requires **no changes to existing stages**. Same as the `Canvas`
  composition lesson from folder 04, applied to data flow.

## Try this

1. Add a `rate_limit(events, per_second)` stage that uses `time.monotonic()` to pace the
   stream. Why is this hard with eager processing?
2. Add a `tee(events) -> tuple[Iterator, Iterator]` that fans the stream into two
   independent iterators (use `itertools.tee`). Stream simultaneously to two consumers.
3. Convert the pipeline so the source is a generator that reads a file lazily
   (`open(path)` already returns an iterator over lines). The rest of the stages don't
   change. That's the win.
