"""Demo of the file pipeline.

Creates a temporary directory of three CSV-ish files (one valid, one with bad rows,
one missing), runs the pipeline, prints the report, then cleans up.

Run:
    python 06_errors_and_context\\04_file_pipeline\\demo.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from pipeline import Pipeline, timed


def write_samples(root: Path) -> None:
    (root / "good.csv").write_text(
        "# header line, ignored\n"
        "10\n"
        "20\n"
        "30\n",
        encoding="utf-8",
    )
    (root / "mixed.csv").write_text(
        "1\n"
        "not-a-number\n"
        "3\n"
        "\n"
        "# blank above\n"
        "5\n",
        encoding="utf-8",
    )
    # Don't write `missing.csv` — but we'll point the pipeline at it via a different glob.


def main() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        in_dir = Path(tmpdir) / "data"
        in_dir.mkdir()
        write_samples(in_dir)
        report_path = Path(tmpdir) / "report.txt"

        with timed("pipeline.run"):
            with Pipeline(in_dir=in_dir, report_path=report_path, column=0) as p:
                result = p.run()

        print("\n--- result summary ---")
        print(f"files processed : {result.files_processed}")
        print(f"rows summed     : {result.rows_summed}")
        print(f"total           : {result.total}")
        print(f"parse errors    : {len(result.parse_errors)}")
        for e in result.parse_errors:
            print(f"  - {e}  (caused by {type(e.__cause__).__name__})")
        print(f"read errors     : {len(result.read_errors)}")

        print("\n--- report.txt ---")
        print(report_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
