"""A small file-processing pipeline.

It reads `.csv` files from a directory, sums one column, writes a report.

Demonstrates:
  - custom exception hierarchy (see `exceptions.py`)
  - `raise NewError(...) from e` at the I/O boundary
  - class-based context manager (`Pipeline.__enter__` / `__exit__`)
  - `@contextmanager`-decorated timing helper
  - `try / except / else` to keep post-success code outside the protected block
"""

from __future__ import annotations

import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import IO, Iterator

from exceptions import FileReadError, LineParseError, PipelineError


@contextmanager
def timed(label: str) -> Iterator[None]:
    """Print how long the wrapped block took. Runs even if the block raises."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"[timed] {label}: {elapsed_ms:.2f} ms")


@dataclass
class PipelineResult:
    files_processed: int = 0
    rows_summed: int = 0
    total: float = 0.0
    parse_errors: list[LineParseError] = field(default_factory=list)
    read_errors: list[FileReadError] = field(default_factory=list)


class Pipeline:
    """Reads CSV-ish files and accumulates a column's total.

    Use it as a context manager so the report file is guaranteed to be closed::

        with Pipeline(in_dir="data", report_path="out.txt", column=0) as p:
            result = p.run()
    """

    def __init__(self, in_dir: str | Path, report_path: str | Path, column: int = 0) -> None:
        if column < 0:
            raise PipelineError(f"column must be >= 0, got {column}")
        self.in_dir = Path(in_dir)
        self.report_path = Path(report_path)
        self.column = column
        self._report_file: IO[str] | None = None
        self.result = PipelineResult()

    # ---- context-manager protocol ----
    def __enter__(self) -> Pipeline:
        # Open the report file here so it's released on __exit__ no matter what.
        try:
            self._report_file = self.report_path.open("w", encoding="utf-8")
        except OSError as e:
            # Translate the third-party (here, stdlib) exception into our domain.
            raise FileReadError(str(self.report_path), f"cannot open report: {e}") from e
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        # Always close — even if the body raised. Returning None propagates the exception.
        if self._report_file is not None:
            self._report_file.close()
            self._report_file = None

    # ---- main work ----
    def run(self) -> PipelineResult:
        assert self._report_file is not None, "use Pipeline as a context manager"

        if not self.in_dir.is_dir():
            raise FileReadError(str(self.in_dir), "directory not found")

        for path in sorted(self.in_dir.glob("*.csv")):
            try:
                file_total, rows = self._read_file(path)
            except FileReadError as e:
                # Log it, remember it, and keep going — single bad file shouldn't abort.
                self.result.read_errors.append(e)
                self._write_line(f"SKIP {path.name}: {e}")
            else:
                # Post-success: write the per-file line OUTSIDE the try, so a write
                # bug here surfaces as itself, not as a misleading FileReadError.
                self.result.files_processed += 1
                self.result.rows_summed += rows
                self.result.total += file_total
                self._write_line(f"OK   {path.name}: rows={rows}, sum={file_total}")

        self._write_line(f"---")
        self._write_line(
            f"TOTAL  files={self.result.files_processed} "
            f"rows={self.result.rows_summed} sum={self.result.total}"
        )
        return self.result

    # ---- helpers ----
    def _read_file(self, path: Path) -> tuple[float, int]:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as e:
            # Boundary: wrap OSError, KEEP the cause for debuggers.
            raise FileReadError(str(path), f"cannot read: {e}") from e

        total = 0.0
        rows = 0
        for i, line in enumerate(text.splitlines(), start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            cols = [c.strip() for c in line.split(",")]
            if self.column >= len(cols):
                # Record but don't abort the file.
                self.result.parse_errors.append(
                    LineParseError(str(path), i, f"only {len(cols)} columns, wanted {self.column}")
                )
                continue
            try:
                value = float(cols[self.column])
            except ValueError as e:
                # `raise ... from e` is the syntax for re-raising; when we're just
                # *recording* the exception, we set __cause__ explicitly so the chain
                # is preserved if a caller later re-raises it.
                err = LineParseError(str(path), i, f"not a number: {cols[self.column]!r}")
                err.__cause__ = e
                self.result.parse_errors.append(err)
                continue
            total += value
            rows += 1
        return total, rows

    def _write_line(self, text: str) -> None:
        assert self._report_file is not None
        self._report_file.write(text + "\n")


if __name__ == "__main__":
    print("Run demo.py to see the pipeline in action.")
