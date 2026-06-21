"""Tests for the event pipeline.

Plain `assert` for now; pytest in folder 09.

Run:
    python 07_iterators_generators\\04_event_pipeline\\test_pipeline.py
"""

from __future__ import annotations

from pipeline import (
    Event,
    Pipeline,
    aggregate,
    find_first,
    from_records,
    normalize_level,
    only_levels,
)


SAMPLE = [
    ("info",  "auth", "ok", 1.0),
    ("warn",  "auth", "stale", 2.0),
    ("error", "db",   "lost",  3.0),
    ("info",  "api",  "ok",    4.0),
    ("error", "api",  "5xx",   5.0),
]


def test_from_records_yields_events() -> None:
    events = list(from_records(SAMPLE))
    assert len(events) == 5
    assert all(isinstance(e, Event) for e in events)
    assert events[0] == Event("info", "auth", "ok", 1.0)


def test_stage_normalize_level() -> None:
    events = list(normalize_level(from_records(SAMPLE)))
    levels = [e.level for e in events]
    assert levels == ["INFO", "WARN", "ERROR", "INFO", "ERROR"]


def test_stage_only_levels_is_lazy() -> None:
    # We can iterate without exhausting if we only need a few items.
    p = Pipeline(levels={"ERROR"})
    stream = p.build(SAMPLE)
    # Take only the first one.
    first = next(stream)
    assert first.level == "ERROR" and first.source == "db"
    # The stream is still alive; we can keep going.
    second = next(stream)
    assert second.level == "ERROR" and second.source == "api"


def test_aggregate_drains_and_counts() -> None:
    p = Pipeline(levels={"ERROR", "WARN"})
    result = aggregate(p.build(SAMPLE))
    assert result.total == 3
    assert result.by_level == {"WARN": 1, "ERROR": 2}
    assert result.by_source == {"auth": 1, "db": 1, "api": 1}


def test_prefix_stage() -> None:
    p = Pipeline(levels={"ERROR"}, prefix=">> ")
    events = list(p.build(SAMPLE))
    assert events[0].message.startswith(">> ")
    assert events[1].message.startswith(">> ")


def test_find_first_early_exit() -> None:
    p = Pipeline(levels={"ERROR", "WARN", "INFO"})
    hit = find_first(p.build(SAMPLE), lambda e: e.source == "api")
    assert hit is not None
    assert hit.source == "api"
    assert hit.level == "INFO"      # the first api event is the INFO ok, not the ERROR


def test_find_first_returns_none_when_no_match() -> None:
    p = Pipeline(levels={"ERROR"})
    hit = find_first(p.build(SAMPLE), lambda e: e.source == "missing")
    assert hit is None


def test_pipeline_is_one_shot() -> None:
    # Same lesson as plain generator expressions: once consumed, the iterator is done.
    p = Pipeline(levels={"ERROR"})
    stream = p.build(SAMPLE)
    first = list(stream)
    second = list(stream)
    assert len(first) == 2 and len(second) == 0


def main() -> None:
    tests = [
        test_from_records_yields_events,
        test_stage_normalize_level,
        test_stage_only_levels_is_lazy,
        test_aggregate_drains_and_counts,
        test_prefix_stage,
        test_find_first_early_exit,
        test_find_first_returns_none_when_no_match,
        test_pipeline_is_one_shot,
    ]
    for t in tests:
        t()
        print(f"  ok  {t.__name__}")
    print(f"\n{len(tests)} tests passed.")


if __name__ == "__main__":
    main()
