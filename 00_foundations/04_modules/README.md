# 04 — Modules and `if __name__ == "__main__"`

Once a piece of code is bigger than a single notebook cell, it belongs in a `.py` file. This
folder is the simplest possible **multi-file program**.

## Files

- [`greetings.py`](greetings.py) — a *module*. Defines reusable functions. No side effects on import.
- [`app.py`](app.py) — the *entry point*. Imports from `greetings` and runs the program.

## Concepts

### Importing

```python
from greetings import greet, farewell   # named imports — the usual choice
import greetings                         # whole-module import — use the dotted form: greetings.greet(...)
```

Python finds modules by searching `sys.path`. When you run `python app.py`, the folder
containing `app.py` is added to `sys.path` automatically — that's why `from greetings
import ...` works here without any setup.

### `if __name__ == "__main__"`

When Python imports a file, it runs every top-level statement in it. That means a `print(...)`
at the top of `greetings.py` would execute every time someone imports it. We don't want that.

Each file has a built-in variable `__name__`:

- If the file is being **run directly** (`python greetings.py`), `__name__ == "__main__"`.
- If the file is being **imported** by another file, `__name__ == "greetings"`.

The idiom `if __name__ == "__main__":` lets you put demo/CLI code inside a file that's
*also* importable as a library.

### Running it

From the project root, with `.venv` activated:

```powershell
python 00_foundations\04_modules\app.py
# expected: "Hello, Dinakar!"  then  "Goodbye, Dinakar."

python 00_foundations\04_modules\greetings.py
# expected: the small demo guarded by `if __name__ == "__main__"`
```

## Try this

1. Add a `shout(name)` function to `greetings.py` that returns the greeting in uppercase.
   Import and use it from `app.py`.
2. Move the `if __name__ == "__main__"` block in `app.py` into a `def main():` function and
   call `main()` from the guard. This is the standard shape for any real script.
3. Add a `print("greetings loaded")` at the *top* of `greetings.py` (outside any function).
   Run `app.py`. Now move that line *inside* the `if __name__ == "__main__"` block in
   `greetings.py`. Re-run `app.py`. Explain the difference.
