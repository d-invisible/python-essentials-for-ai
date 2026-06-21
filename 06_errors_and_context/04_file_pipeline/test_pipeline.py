"""Tests for the file pipeline.

Plain `assert` for now; we move to `pytest` in folder 09.

Run:
    python 06_errors_and_context\\04_file_pipeline\\test_pipeline.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from exceptions import FileReadError, LineParseError, PipelineError
from pipeline import Pipeline


def _write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def test_happy_path_sums_column() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        in_dir = Path(tmp) / "in"
        in_dir.mkdir()
        _write(in_dir / "a.csv", "1\n2\n3\n")
        _write(in_dir / "b.csv", "4\n5\n")
        report = Path(tmp) / "report.txt"
        with Pipeline(in_dir=in_dir, report_path=report, column=0) as p:
            r = p.run()
        assert r.files_processed == 2
        assert r.rows_summed == 5
        assert r.total == 15.0
        assert r.parse_errors == []
        # Report file got something
        assert "TOTAL" in report.read_text(encoding="utf-8")


def test_parse_errors_dont_abort_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        in_dir = Path(tmp) / "in"
        in_dir.mkdir()
        _write(in_dir / "mixed.csv", "1\nbad\n3\n# comment\n5\n")
        report = Path(tmp) / "report.txt"
        with Pipeline(in_dir=in_dir, report_path=report) as p:
            r = p.run()
        assert r.files_processed == 1
        assert r.rows_summed == 3              # 1, 3, 5 — bad and comment skipped
        assert r.total == 9.0
        assert len(r.parse_errors) == 1
        err = r.parse_errors[0]
        assert isinstance(err, LineParseError)
        assert err.line_no == 2
        # raise-from semantics preserved
        assert err.__cause__ is not None
        assert isinstance(err.__cause__, ValueError)


def test_missing_directory_raises_file_read_error() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        report = Path(tmp) / "report.txt"
        with Pipeline(in_dir=Path(tmp) / "nope", report_path=report) as p:
            try:
                p.run()
            except FileReadError as e:
                assert "directory not found" in str(e)
                return
        raise AssertionError("expected FileReadError")


def test_exit_closes_report_even_on_error() -> None:
    # Verify the cleanup contract: __exit__ closes the report file even if run() raised.
    with tempfile.TemporaryDirectory() as tmp:
        report = Path(tmp) / "report.txt"
        with Pipeline(in_dir=Path(tmp) / "nope", report_path=report) as p:
            try:
                p.run()
            except FileReadError:
                pass
        # After __exit__: file handle is gone
        assert p._report_file is None


def test_negative_column_rejected() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        try:
            Pipeline(in_dir=tmp, report_path=Path(tmp) / "r.txt", column=-1)
        except PipelineError:
            return
        raise AssertionError("expected PipelineError for negative column")


def main() -> None:
    tests = [
        test_happy_path_sums_column,
        test_parse_errors_dont_abort_file,
        test_missing_directory_raises_file_read_error,
        test_exit_closes_report_even_on_error,
        test_negative_column_rejected,
    ]
    for t in tests:
        t()
        print(f"  ok  {t.__name__}")
    print(f"\n{len(tests)} tests passed.")


if __name__ == "__main__":
    main()
