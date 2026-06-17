"""The `Repository[T]` contract — pure shape, no implementation.

Any class with `find_by_id`, `save`, `all`, and `delete` of the right shapes structurally
satisfies this protocol — no inheritance required.

About the missing `bound=HasId`
-------------------------------
The natural design would parameterize this on `T: HasId` where `HasId` is a Protocol with
an `id: int` attribute. That works in many type-checkers, but some versions reject
*structural* matches on Protocol bounds and demand explicit inheritance — which defeats
the purpose. So we leave `T` unbounded here and document the contract: implementations
are expected to handle entities exposing an `id: int`. Real-world Python typing: 95% of
the time it's airtight, occasionally you accept a documented gap.
"""

from __future__ import annotations

from typing import Protocol, TypeVar

T = TypeVar("T")


class Repository(Protocol[T]):
    """A generic CRUD-ish repository contract.

    Implementations work with entities that expose an `id: int` attribute (duck-typed).
    """

    def find_by_id(self, id: int) -> T | None: ...

    def save(self, item: T) -> None: ...

    def all(self) -> list[T]: ...

    def delete(self, id: int) -> bool: ...
