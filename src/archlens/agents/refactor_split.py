"""Oversized-module splitter: split a >150-line module into <=150-line parts (task 11.019).

Top-level definitions are binned greedily so each emitted part stays within the line cap; the
original module is rewritten as a façade re-importing every part (imports updated).
"""

import ast
from pathlib import Path

from ..shared.constants import LINE_CAP
from ..shared.lines import effective_lines

_IMPORTS = (ast.Import, ast.ImportFrom)
_DEFS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Assign, ast.AnnAssign)


def _segments(text: str) -> tuple[str, list[str]]:
    header, chunks = [], []
    for node in ast.parse(text).body:
        seg = ast.get_source_segment(text, node)
        if seg is None:
            continue
        if isinstance(node, _IMPORTS):
            header.append(seg)
        elif isinstance(node, _DEFS):
            chunks.append(seg)
    return "\n".join(header), chunks


def _bin(header: str, chunks: list[str]) -> list[list[str]]:
    parts: list[list[str]] = []
    current: list[str] = []
    for chunk in chunks:
        trial = header + "\n" + "\n\n".join([*current, chunk])
        if current and effective_lines(trial) > LINE_CAP:
            parts.append(current)
            current = [chunk]
        else:
            current.append(chunk)
    if current:
        parts.append(current)
    return parts


def split_module(path) -> list[Path]:
    """Split an oversized module into parts <=150 lines; return the new part paths."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    header, chunks = _segments(text)
    written, facade = [], []
    for index, group in enumerate(_bin(header, chunks), 1):
        part = path.with_name(f"{path.stem}_part{index}.py")
        prefix = f"{header}\n\n" if header else ""
        part.write_text(prefix + "\n\n".join(group) + "\n", encoding="utf-8")
        written.append(part)
        facade.append(f"from {part.stem} import *")
    path.write_text("\n".join(facade) + "\n", encoding="utf-8")
    return written
