"""Entry point for the modules demo.

Run from the project root:

    python 00_foundations\\04_modules\\app.py
"""

from greetings import farewell, greet


def main() -> None:
    name = "Dinakar"
    print(greet(name))
    print(farewell(name))


if __name__ == "__main__":
    main()
