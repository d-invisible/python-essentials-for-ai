# 04 — File Pipeline: exceptions + context managers in one place

A small `.py` tool that **processes a directory of CSV-ish files**, summing one column.
Every concept from this folder shows up:

- A custom exception **hierarchy** (`PipelineError` → `FileReadError`, `LineParseError`).
- **`raise ... from e`** at module boundaries (wrap `OSError`, `ValueError`).
- A **class-based context manager** (`Pipeline`) — state + multiple methods.
- A **`@contextmanager`** helper (`timed`) — quick setup/yield/teardown.
- `try / except / else / finally` used in anger.

## Files

- [`exceptions.py`](exceptions.py) — the exception hierarchy.
- [`pipeline.py`](pipeline.py) — `Pipeline` class (context manager) + `timed` helper.
- [`demo.py`](demo.py) — creates a temp folder of sample data, runs the pipeline.
- [`test_pipeline.py`](test_pipeline.py) — assert-based tests.

## Run it

```powershell
python 06_errors_and_context\04_file_pipeline\demo.py
python 06_errors_and_context\04_file_pipeline\test_pipeline.py
```

`demo.py` writes its sample data to a temp directory and cleans up after itself — nothing
lands in your project tree.

## What this teaches in code

| Concept | Where to look |
|---|---|
| Hierarchy with one base | `exceptions.py` |
| `raise FileReadError(...) from e` | `pipeline.py` → `Pipeline._read_file` |
| `__enter__` / `__exit__` | `pipeline.py` → `Pipeline` |
| `@contextmanager` | `pipeline.py` → `timed` |
| `try / except / else` | `pipeline.py` → `Pipeline.run` |
| Cleanup that ALWAYS runs | `Pipeline.__exit__` closes the report file even on errors |

## Try this

1. Add a `--strict` mode: any `LineParseError` aborts the whole pipeline instead of being
   logged and skipped. Where do you add the option, and does the existing test catch the
   change?
2. Replace `Pipeline`'s class-based context manager with a `@contextmanager` version.
   Which is clearer for this case? Why?
3. Add an `ExceptionGroup` path that collects every per-line failure and re-raises them
   together after the whole file is processed. Compare with the current "log and skip"
   behavior — when would each be appropriate?
