"""Demo: drive the pipeline a few different ways from one input stream.

Run:
    python 07_iterators_generators\\04_event_pipeline\\demo.py
"""

from __future__ import annotations

from pipeline import (
    Pipeline,
    aggregate,
    find_first,
    from_records,
    normalize_level,
    only_levels,
)


SAMPLE = [
    ("info",  "auth",  "user logged in",      1.0),
    ("debug", "auth",  "session cache miss",  1.1),
    ("warn",  "auth",  "stale token",         2.0),
    ("error", "db",    "connection lost",     3.0),
    ("debug", "db",    "retry handshake",     3.2),
    ("error", "db",    "retry failed",        3.5),
    ("info",  "api",   "request",             3.6),
    ("error", "api",   "5xx upstream",        4.0),
]


def main() -> None:
    # ---- 1. The "aggregate everything" use case ----
    p = Pipeline(levels={"ERROR", "WARN"}, prefix=">> ")
    result = aggregate(p.build(SAMPLE))
    print("\n[aggregate ERROR+WARN]")
    print(f"  total      : {result.total}")
    print(f"  by_level   : {result.by_level}")
    print(f"  by_source  : {result.by_source}")
    print(f"  last_msg   : {result.last_message!r}")

    # ---- 2. The "early-exit" use case ----
    # Pipeline only walks far enough to find one match — note the "drained" line
    # still fires because of the generator's `finally`.
    p2 = Pipeline(levels={"ERROR", "WARN"})
    print("\n[first error from db]")
    hit = find_first(p2.build(SAMPLE), lambda e: e.level == "ERROR" and e.source == "db")
    print(f"  found: {hit}")

    # ---- 3. Compose stages manually if you don't want the Pipeline helper ----
    print("\n[manual composition: just INFO]")
    stream = only_levels(normalize_level(from_records(SAMPLE)), {"INFO"})
    for e in stream:
        print("  -", e)


if __name__ == "__main__":
    main()
