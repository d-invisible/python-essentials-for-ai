# 00 — Foundations

The bare-minimum Python you need before we touch OOP. Aim for fluency, not depth — we'll
revisit everything later in a more structured way.

## You'll be able to

- Read and write basic Python syntax confidently (variables, types, f-strings, I/O).
- Drive control flow with `if`/`elif`/`else`, `for`, `while`, `match`.
- Define and call functions with parameters, defaults, and return values.
- Split code across files (modules) and understand `import` + `if __name__ == "__main__"`.
- Decide when to use `.ipynb` (exploration) vs `.py` (real programs).

## Prerequisites

- Python 3.12 installed in `.venv` (already done).
- VS Code with the Python + Jupyter extensions, or any Jupyter UI.

## How to work through this folder

Open each file in order. Run every cell / script yourself — don't just read.

| # | File | Format | Why this format |
|---|------|--------|-----------------|
| 1 | [01_syntax_types_io.ipynb](01_syntax_types_io.ipynb) | notebook | exploratory; seeing each value matters |
| 2 | [02_control_flow.ipynb](02_control_flow.ipynb) | notebook | same — short snippets, immediate output |
| 3 | [03_functions_intro.ipynb](03_functions_intro.ipynb) | notebook | learn by calling and observing |
| 4 | [04_modules/](04_modules/) | `.py` scripts | this is the first thing that *must* be a real program |

### Selecting the kernel in VS Code

When you open a `.ipynb`, click "Select Kernel" → "Python Environments" → choose
`.venv (Python 3.12.13)`. If it doesn't appear, run once in a terminal:

```powershell
.\.venv\Scripts\python.exe -m ipykernel install --user --name basics01-py312 --display-name "Python (basics_01)"
```

### Running `.py` files

From the project root, with `.venv` activated:

```powershell
python 00_foundations\04_modules\app.py
# or, the "proper" way once we get to packages:
python -m 00_foundations.04_modules.app  # (won't work yet — folder names start with digits)
```

## Exercises

Do these after you've worked through all four files. Add your solutions inside the
relevant notebook as new cells, or as a new `exercises.py`.

1. **FizzBuzz** — print numbers 1..30. Replace multiples of 3 with `Fizz`, multiples of 5
   with `Buzz`, multiples of both with `FizzBuzz`. Solve it twice: once with `if/elif`,
   once with `match`.
2. **Temperature converter** — write a function `c_to_f(c: float) -> float` and a function
   `f_to_c(f: float) -> float`. Verify `f_to_c(c_to_f(100)) == 100.0` (mind floating-point!).
3. **Word counter** — given a string `s`, return a dict mapping each word to how many times
   it appears. Lower-case everything; split on whitespace.
4. **Module split** — take your word counter, move it into `04_modules/text_utils.py`, and
   call it from `app.py`. Make `text_utils.py` *also* runnable on its own with a small demo
   guarded by `if __name__ == "__main__"`.
5. **Pick `.py` or `.ipynb`** — for each below, decide and write one sentence why:
   (a) experimenting with regex patterns, (b) a CLI that renames files in a folder,
   (c) plotting the distribution of word lengths in a book, (d) the production code for a
   FastAPI endpoint.

## Next topic

After "next learning": **01_data_structures** — list/tuple/dict/set, slicing,
comprehensions, mutability.
