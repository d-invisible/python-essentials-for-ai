"""Tests for the repository and service.

Two things to notice:

  1. We test `InMemoryRepository` directly — basic CRUD.
  2. We test `UserService` by injecting the in-memory repo as a **test double** — exactly
     what we'd do with a mock in a larger project. The service has no idea it's in a test.

Plain `assert` for now — pytest in folder 09.

Run:
    python 05_typing_and_protocols\\04_repository_protocol\\test_repo.py
"""

from in_memory import InMemoryRepository
from service import User, UserService


def test_in_memory_crud() -> None:
    repo: InMemoryRepository[User] = InMemoryRepository()
    assert repo.find_by_id(1) is None
    assert repo.all() == []

    u = User(1, "Alice", "a@b.c")
    repo.save(u)
    assert repo.find_by_id(1) == u
    assert repo.all() == [u]

    # save is upsert by id
    u2 = User(1, "Alice2", "a2@b.c")
    repo.save(u2)
    assert repo.find_by_id(1) == u2
    assert len(repo.all()) == 1

    # delete returns True the first time, False afterwards
    assert repo.delete(1) is True
    assert repo.delete(1) is False
    assert repo.find_by_id(1) is None


def test_in_memory_all_returns_a_copy() -> None:
    # Encapsulation — the list returned by all() should be a copy, not the storage.
    repo: InMemoryRepository[User] = InMemoryRepository()
    repo.save(User(1, "A", "a@b.c"))
    snapshot = repo.all()
    snapshot.clear()
    assert len(repo.all()) == 1, "caller mutating the snapshot should not affect storage"


def test_user_service_uses_injected_repository() -> None:
    # This test injects the in-memory repo. The service can't tell the difference between
    # this and a "real" repository.
    repo: InMemoryRepository[User] = InMemoryRepository()
    service = UserService(repo)

    # find_or_create_user creates on first call, returns existing on second
    a1 = service.find_or_create_user(1, "Alice", "a@b.c")
    a2 = service.find_or_create_user(1, "Alice", "a@b.c")
    assert a1 == a2
    assert len(service.list_users()) == 1

    # deactivation removes
    assert service.deactivate(1) is True
    assert service.deactivate(1) is False
    assert service.list_users() == []


def test_user_service_doesnt_overwrite_on_duplicate_find_or_create() -> None:
    # If a user with this id already exists, find_or_create_user returns it WITHOUT saving
    # the new (different) name/email. This is intentional — and the kind of behavior a
    # mock would let us assert call counts on (exercise #2 in the README).
    repo: InMemoryRepository[User] = InMemoryRepository()
    service = UserService(repo)
    service.find_or_create_user(1, "Alice", "a@b.c")
    returned = service.find_or_create_user(1, "DIFFERENT", "x@y.z")
    assert returned.name == "Alice"
    assert returned.email == "a@b.c"


def main() -> None:
    tests = [
        test_in_memory_crud,
        test_in_memory_all_returns_a_copy,
        test_user_service_uses_injected_repository,
        test_user_service_doesnt_overwrite_on_duplicate_find_or_create,
    ]
    for t in tests:
        t()
        print(f"  ok  {t.__name__}")
    print(f"\n{len(tests)} tests passed.")


if __name__ == "__main__":
    main()
