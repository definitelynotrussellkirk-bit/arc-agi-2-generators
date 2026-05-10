#!/usr/bin/env python3
"""Extract per-task descriptions from solvers/grounded_rules.py inline
comments and write them to data/standalone_descriptions.json.

Each rule in GROUNDED_RULES is preceded by `#` comments authored as
solving notes; these are real descriptions of what the rule does. The
canonical builder previously hardcoded `written_solution=""` for
training-set tasks because there was no source file. With this
mapping in place, the builder can populate `written_solution` from the
extracted text — closing the 1,000-task description gap.

Run after editing comments in grounded_rules.py:
    python3 scripts/extract_standalone_descriptions.py
    python3 scripts/build_canonical_puzzles.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GR_PATH = ROOT / "solvers" / "grounded_rules.py"
OUT_PATH = ROOT / "data" / "standalone_descriptions.json"

_BANNER_RE = re.compile(r"^\s*(?:---+|===+|\+\++|\*\*\*+)")
# Match the entry line — the value may be `r"""..."""`, `'...'`, `"..."`,
# or a helper call like `_local_rewrite_rule(...)` / other Python expr.
_TID_LINE_RE = re.compile(r'^\s*"([0-9a-f]{8})"\s*:\s*\S')


def extract_comments(src: str) -> dict[str, str]:
    """Walk grounded_rules.py and pull the comment block immediately
    above each entry. Skip section banners. Comments separated from
    the entry by blank lines are still associated, up to the previous
    entry's closing triple-quote.

    Stops scanning once the NOT_GROUNDED dict opens — entries below
    that line are placeholders that mirror tids from GROUNDED_RULES,
    and their leading dict-level comment ("Tasks that need Python…")
    leaks onto each tid otherwise."""
    out: dict[str, str] = {}
    lines = src.splitlines()
    # Truncate at the NOT_GROUNDED boundary so its placeholder entries
    # can't shadow the real GROUNDED_RULES descriptions above.
    not_grounded_idx = None
    for i, line in enumerate(lines):
        if line.startswith("NOT_GROUNDED = {") or line.startswith("NOT_GROUNDED ="):
            not_grounded_idx = i
            break
    if not_grounded_idx is not None:
        lines = lines[:not_grounded_idx]

    tid_lines: list[tuple[int, str]] = [
        (i, m.group(1)) for i, line in enumerate(lines)
        if (m := _TID_LINE_RE.match(line))
    ]

    def find_prev_close(start: int) -> int:
        # Closing form for the PREVIOUS entry. Match string-quoted ends
        # (`""",` / `',`) and helper-call ends (`]),` / `),`).  Plain
        # `)` (no comma) is mid-expression; skip.
        j = start - 1
        while j >= 0:
            s = lines[j].rstrip()
            if (s.endswith('""",') or s.endswith("',")
                or s.endswith('"),') or s.endswith("']),")
                or s.endswith(']),') or s.endswith('),')):
                return j + 1
            j -= 1
        return 0

    for i, tid in tid_lines:
        scan_start = find_prev_close(i)
        # Walk backwards from i-1 collecting the LAST contiguous block of
        # # comments (closest to the entry). Skip blanks; banners end a
        # block.
        last_block: list[str] = []
        for j in range(i - 1, max(scan_start - 1, -1), -1):
            stripped = lines[j].rstrip()
            if not stripped:
                if last_block:
                    break
                continue
            if not stripped.lstrip().startswith("#"):
                if last_block:
                    break
                continue
            text = stripped.lstrip("# ").rstrip()
            if not text:
                continue
            if _BANNER_RE.match(text):
                if last_block:
                    break
                continue
            last_block.append(text)
        if last_block:
            last_block.reverse()
            joined = " ".join(last_block).strip()
            if joined:
                out[tid] = joined
    return out


def main():
    src = GR_PATH.read_text()
    comments = extract_comments(src)
    OUT_PATH.write_text(json.dumps(comments, indent=2, sort_keys=True) + "\n")
    print(f"extracted {len(comments)} descriptions → {OUT_PATH.relative_to(ROOT)}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
