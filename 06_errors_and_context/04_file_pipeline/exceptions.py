"""Exception hierarchy for the file-pipeline module.

One base for the whole module; specific subclasses for the cases callers might want to
handle differently. Adding fields only when a caller would react to them programmatically.
"""

from __future__ import annotations


class PipelineError(Exception):
    """Base for every error this module raises."""


class FileReadError(PipelineError):
    """Couldn't read a file from disk. Wraps the underlying OSError."""

    def __init__(self, path: str, message: str) -> None:
        super().__init__(f"{path}: {message}")
        self.path = path


class LineParseError(PipelineError):
    """A specific line of a file could not be parsed."""

    def __init__(self, path: str, line_no: int, message: str) -> None:
        super().__init__(f"{path}:{line_no}: {message}")
        self.path = path
        self.line_no = line_no
