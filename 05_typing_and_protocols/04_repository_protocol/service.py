"""`UserService` — depends on the `Repository[User]` shape, not a concrete class.

Swap in any class that satisfies `Repository[User]` (in-memory now, SQL later, mock in
tests) and this code keeps working. That's dependency injection.
"""

from __future__ import annotations

from dataclasses import dataclass

from repository import Repository


@dataclass(frozen=True)
class User:
    """Frozen value object. Has an `id: int`, so it satisfies the `HasId` Protocol."""

    id: int
    name: str
    email: str


class UserService:
    """Application-level operations on users.

    `repo` is injected — the service doesn't construct its own repository, doesn't pick a
    backend, doesn't know about persistence. It only knows the `Repository[User]` contract.
    """

    def __init__(self, repo: Repository[User]) -> None:
        self.repo = repo

    def find_or_create_user(self, id: int, name: str, email: str) -> User:
        """Return the existing user with `id`, or create + save a new one."""
        existing = self.repo.find_by_id(id)
        if existing is not None:
            return existing
        user = User(id=id, name=name, email=email)
        self.repo.save(user)
        return user

    def list_users(self) -> list[User]:
        return self.repo.all()

    def deactivate(self, id: int) -> bool:
        """Pretend-deactivate by deleting. Returns True if a user was removed."""
        return self.repo.delete(id)
