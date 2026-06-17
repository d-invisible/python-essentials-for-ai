"""An in-memory `Repository[T]` implementation.

Notice: this class does NOT inherit from `Repository`. It only needs to *match the shape*
of the protocol — that's structural typing. mypy verifies the call sites.

Why `getattr(item, "id")` instead of `item.id`?
Because `T` is unbounded here (see the note in `repository.py`), mypy doesn't know `T`
has an `id` attribute. `getattr` returns `Any`, which mypy lets through. It's a small
documented escape hatch — the cleanest workaround when the bound can't be expressed.
"""

from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class InMemoryRepository(Generic[T]):
    """Stores items keyed by their `.id`. Useful for dev and tests."""

    def __init__(self) -> None:
        self._items: dict[int, T] = {}

    def find_by_id(self, id: int) -> T | None:
        return self._items.get(id)

    def save(self, item: T) -> None:
        # Duck-typed: `item` is expected to have an `id: int`. See module docstring.
        self._items[getattr(item, "id")] = item

    def all(self) -> list[T]:
        # Return a fresh list so callers can't mutate our storage.
        return list(self._items.values())

    def delete(self, id: int) -> bool:
        # `del` raises if the key is missing; pop with default lets us return a bool.
        return self._items.pop(id, None) is not None
