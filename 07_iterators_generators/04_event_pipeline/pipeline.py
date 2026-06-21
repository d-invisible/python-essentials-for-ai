"""A small event pipeline built out of typed generator stages.

Each stage has the type `Iterator[Event] -> Iterator[Event]`. That means stages compose
by function call, are trivial to test in isolation, and adding a new stage requires no
changes to the existing ones.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Event:
    level: str               # "INFO", "WARN", "ERROR", ...
    source: str              # which subsystem emitted it
    message: str
    ts: float = 0.0          # seconds since some epoch (kept simple)


# ---------------- sources ----------------

def from_records(records: Iterable[tuple[str, str, str, float]]) -> Iterator[Event]:
    """Source stage: turn raw tuples into Events.

    The `try/finally` here demonstrates generator cleanup: the "drained" line prints
    whether the stream is fully consumed OR the consumer stops early.
    """
    try:
        for level, source, message, ts in records:
            yield Event(level=level, source=source, message=message, ts=ts)
    finally:
        # Real code would close a file handle / DB cursor here.
        print("[from_records] drained")


# ---------------- transforming stages ----------------

def normalize_level(events: Iterator[Event]) -> Iterator[Event]:
    """Upper-case the level so downstream stages can compare consistently."""
    for e in events:
        yield Event(level=e.level.upper(), source=e.source, message=e.message, ts=e.ts)


def only_levels(events: Iterator[Event], levels: set[str]) -> Iterator[Event]:
    """Filter to events whose level is in `levels`. Keeps the stream lazy."""
    for e in events:
        if e.level in levels:
            yield e


def add_prefix(events: Iterator[Event], prefix: str) -> Iterator[Event]:
    """Demonstrates a transforming stage that builds new Events (immutability friendly)."""
    for e in events:
        yield Event(level=e.level, source=e.source, message=f"{prefix}{e.message}", ts=e.ts)


# ---------------- terminal stages (consumers) ----------------

@dataclass
class Aggregate:
    total: int = 0
    by_level: dict[str, int] = field(default_factory=dict)
    by_source: dict[str, int] = field(default_factory=dict)
    last_message: str | None = None


def aggregate(events: Iterator[Event]) -> Aggregate:
    """Drain the pipeline into an aggregate. This is what runs the whole chain."""
    a = Aggregate()
    for e in events:
        a.total += 1
        a.by_level[e.level] = a.by_level.get(e.level, 0) + 1
        a.by_source[e.source] = a.by_source.get(e.source, 0) + 1
        a.last_message = e.message
    return a


def find_first(events: Iterator[Event], predicate) -> Event | None:
    """Early-exit consumer: pull until the first match, then stop.

    Because the pipeline is lazy, every upstream stage stops too.
    """
    return next((e for e in events if predicate(e)), None)


# ---------------- a small convenience to wire stages together ----------------

class Pipeline:
    """Bundles common stage choices behind one builder.

    A class isn't strictly needed (each stage is already a function), but it keeps
    the wiring readable when you have many parameters.
    """

    def __init__(self, levels: set[str], prefix: str = "") -> None:
        self.levels = levels
        self.prefix = prefix

    def build(self, source: Iterable[tuple[str, str, str, float]]) -> Iterator[Event]:
        stream = from_records(source)
        stream = normalize_level(stream)
        stream = only_levels(stream, self.levels)
        if self.prefix:
            stream = add_prefix(stream, self.prefix)
        return stream


if __name__ == "__main__":
    sample = [
        ("info",  "auth",  "user logged in",   1.0),
        ("warn",  "auth",  "stale token",      2.0),
        ("error", "db",    "connection lost",  3.0),
        ("debug", "db",    "noise",            3.5),
        ("error", "api",   "5xx upstream",     4.0),
    ]
    p = Pipeline(levels={"ERROR", "WARN"}, prefix=">> ")
    print("Aggregate:", aggregate(p.build(sample)))
