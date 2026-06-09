"""A tiny module with reusable greeting helpers.

Importable from `app.py`. Also runnable on its own — see the bottom of this file.
"""


def greet(name: str, greeting: str = "Hello") -> str:
    """Return a friendly greeting for `name`."""
    return f"{greeting}, {name}!"


def farewell(name: str) -> str:
    """Return a goodbye message for `name`."""
    return f"Goodbye, {name}."


# This block runs ONLY when you do `python greetings.py` directly.
# When `app.py` imports this file, this block is skipped.
if __name__ == "__main__":
    print("Running greetings.py directly — quick self-test:")
    print(greet("World"))
    print(farewell("World"))
