"""Wire concrete classes together — the DI moment.

Run:
    python 05_typing_and_protocols\\04_repository_protocol\\demo.py
"""

from in_memory import InMemoryRepository
from service import User, UserService


def main() -> None:
    # 1. Pick a repository implementation.
    repo: InMemoryRepository[User] = InMemoryRepository()

    # 2. Inject it into the service. The service has no idea which kind of repo this is.
    service = UserService(repo)

    # 3. Use the service.
    alice = service.find_or_create_user(1, "Alice", "a@b.c")
    bob = service.find_or_create_user(2, "Bob", "b@b.c")
    print("created:", alice)
    print("created:", bob)

    # idempotent: same id returns the same user, no second save
    alice_again = service.find_or_create_user(1, "Alice", "a@b.c")
    print("same user?", alice is alice_again)

    print("\nall users:")
    for u in service.list_users():
        print(" -", u)

    # deactivate
    print("\ndeactivate id=2 ->", service.deactivate(2))
    print("deactivate id=99 ->", service.deactivate(99))
    print("\nafter deactivation:")
    for u in service.list_users():
        print(" -", u)


if __name__ == "__main__":
    main()
