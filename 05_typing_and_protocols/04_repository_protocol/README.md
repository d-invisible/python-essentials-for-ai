# 04 — Protocol-based Repository (DI preview)

A small `.py` example showing **Protocol + generics + dependency injection** working
together. This is a preview of folder 12 (`services and DI`) — the cleanest, smallest
DI pattern in Python uses exactly these tools.

## Files

- [`repository.py`](repository.py) — defines `Repository[T]` as a `Protocol`. No concrete code, just the contract.
- [`in_memory.py`](in_memory.py) — `InMemoryRepository[T]` implementing the protocol structurally (does *not* inherit from it).
- [`service.py`](service.py) — `UserService` depends on `Repository[User]`. **It doesn't know or care which implementation it gets.** That's the win.
- [`demo.py`](demo.py) — wires real classes together (DI by passing the repository in).
- [`test_repo.py`](test_repo.py) — tests for the in-memory implementation and for the service (using the in-memory repo as a *test double*).

## Run it

```powershell
python 05_typing_and_protocols\04_repository_protocol\demo.py
python 05_typing_and_protocols\04_repository_protocol\test_repo.py
```

## Type-check it

The whole folder is typed and should pass mypy:

```powershell
.venv\Scripts\python.exe -m mypy 05_typing_and_protocols\04_repository_protocol
```

Try breaking something in `service.py` (`return None` where a `User` is expected, pass an
`int` to `repo.save(...)`) and re-run mypy to see it catch the bug.

### A real-world typing gap

You'll notice `Repository[T]` does **not** bound `T` to a `HasId` Protocol — yet
`InMemoryRepository.save` clearly needs `item.id`. Read the docstrings at the top of
`repository.py` and `in_memory.py` for why. Short version: not every type-checker accepts
*structural* matches on Protocol bounds, so we document the contract instead of expressing
it in the type system. This is a real pattern you'll see in production Python.

## Why this is a big deal

Look at `UserService.find_or_create_user` in `service.py`. It uses `self.repo` to find and
save users — but `self.repo` could be:

- the `InMemoryRepository` from `in_memory.py` (production, before you have a DB),
- a future `SqlAlchemyRepository` (production, with a real DB),
- a mock in a unit test.

The service code doesn't change. *The dependency is injected.*

That's the whole game. Folders 12 → 14 build on exactly this pattern: FastAPI's `Depends`
is just an automated way to wire these together.

## Try this

1. Add a `delete(id: int) -> bool` method to the `Repository` protocol. Make
   `InMemoryRepository` implement it. Does mypy now complain anywhere else? (It should —
   it'll flag any code path that uses the protocol but doesn't account for the new method.)
2. Add a `MockRepository` that records every call it gets and returns canned responses.
   Use it in a test that asserts `UserService.find_or_create_user` *did not call save*
   when the user already existed.
3. Make `Repository[T]` extend a smaller `ReadRepository[T]` (just `find_by_id` and `all`)
   plus the writes. Why might callers prefer to receive a `ReadRepository[T]` when they
   only read? (Hint: principle of least privilege.)
