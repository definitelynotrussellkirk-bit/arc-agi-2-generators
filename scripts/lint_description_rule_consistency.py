#!/usr/bin/env python3
"""Cross-artifact lint: colors named in description must appear in rule.

Lexical-form lint catches `blue(6)` (name/number mismatch). This catches
the next class of authoring error:

    DESC: "Ignore all distractors and look only at the magenta(6)
           object. Output ... all blue(1) cells ..."
    RULE: only references colors {0, 6}  (no 1)

The author confused two colors mid-description. The lexical form is
fine; the cross-reference is wrong. Without checking the rule we can't
catch it.

Three checks:
  1. desc-extra-color   color named in desc that doesn't appear in rule
  2. desc-missing-color color in rule that's never named in desc (only
                        flagged if the rule actively uses the color in
                        a recolor / paint / set-cell, not just iteration)
  3. desc-bare-number   bare digit 1-9 in description prose where a
                        color name was intended (e.g., "fill with 7" —
                        should be `orange(7)`)

Auto-fix is conservative: only the desc-extra-color findings can
sometimes be fixed by removing the offending phrase or replacing the
wrong color name with the correct one — but disambiguation requires
LLM-style judgment, so we flag and let humans decide.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.lint_descriptions import COLOR_NAMES, COLOR_NAME_TO_NUM


# Regex for canonical name(N) refs in description
_DESC_COLOR_RE = re.compile(
    rf"\b({'|'.join(COLOR_NAMES.values())})\((\d)\)",
    re.IGNORECASE,
)
# Bare digit that's almost certainly a COLOR reference (not a count or
# control value). Limited to color-action contexts.
# Trigger contexts (each → bare-digit-as-color):
#   color-verb prefix:     with N, to N, becomes N, stays N, color N, fill N,
#                          paint N, recolor N, color it N, color them N
#   arrow:                 → N, -> N (no-space variant)
#   quantifier prefix:     Each N, every N, all N, the N, that N, these N, this N,
#                          a N, an N
#   preposition prefix:    into N, from N, as N, via N, using N
#
# Skips when followed by a count-noun/dimension:
#   N hole, N marker, N cell, N component, N object, N row, N column,
#   N quadrant, N panel, N edge, N corner, N side, N step, N time, N copy,
#   N copies, N rotation, N degree, N line, N pixel, N block, N adjacent,
#   N consecutive, N neighbor, N seed, N axis, N direction, N point, N piece,
#   N quarter, N third, N position, N frame, N layer, N dihedral, N nonzero,
#   N distinct, N unique, N×, N x, N by, N D (1D), N st/nd/rd/th
_DESC_BARE_NUM_RE = re.compile(
    r"(?:"
    r"\b(?:with|to|becomes?|stays?|color|fill|paint|recolor)(?:\s+(?:it|them|the|each))?\s+"
    r"|→\s*|->\s*"
    r"|\b(?:Each|each|The|the|That|that|These|these|This|this|All|all|Every|every|Any|any|a|an)\s+"
    r"|\b(?:into|from|as|via|using)\s+"
    r")"
    r"([1-9])"
    # Negative lookahead: skip when digit is followed by a count noun, dimension marker,
    # connectivity term, scale marker (Nx, NxN), fraction (N/N), or D-suffix (1D/2D/3D).
    r"(?!\s*(?:hole|marker|cell|component|object|row|column|quadrant|panel|edge|"
    r"corner|side|step|time|copy|copies|rotation|degree|line|pixel|block|adjacent|"
    r"consecutive|neighbor|seed|axis|direction|point|piece|quarter|third|position|"
    r"frame|layer|dihedral|nonzero|non-zero|distinct|unique|orientation|color|"
    r"st|nd|rd|th))"
    # Hyphenated compounds that are NOT colors:
    #   4-connected, 4-neighbor, 4-conn, 8-connectivity (graph-theory)
    #   1-row, 2-row, N-row (dimension)
    #   1-hole, 2-hole (count of holes inside an object)
    #   1-based, 0-based (indexing)
    #   1-wide, 2-wide (line/segment width)
    #   3-cell, 3-grid, 4-sided (count compounds)
    r"(?![-‐-—](?:conn(?:ected|ectivity)?|neighbor[a-z]*|cell|grid|sided?|"
    r"row|col|column|hole|based|wide|tall|long|deep|bordered|colored|valued))"
    r"(?![Dd]\b)"                                                          # 1D, 2D, 3D
    r"(?![×x]\d)"                                                          # 3×3, 5x5
    r"(?![×x]\b)"                                                          # 3x scaling
    r"(?![-]?by[-\s]\d)"                                                   # 3-by-3, 3 by 3
    r"(?![/]\d)"                                                           # 1/4 fraction
    r"\b",
    re.IGNORECASE,
)


def colors_in_rule(rule_src: str) -> Counter:
    """Color literals in a Racket rule, weighted by how 'used' they are.

    Heuristic: count integer literals that look like color values. We
    weight them more if they appear in painting / recoloring contexts
    (paint-cells, set-cell, recolor, swap-colors) — those are where the
    rule actively cares about the color.
    """
    counts = Counter()
    # Pass 1: every digit token
    for m in re.finditer(r"\b([0-9])\b", rule_src):
        counts[int(m.group(1))] += 1
    return counts


def lint_one(desc: str, rule: str, puzzle_colors: set[int] | None = None) -> list[dict]:
    """Lint one (description, rule) pair.

    `puzzle_colors` is the set of colors that actually appear in the
    puzzle's train/test image data. When supplied, desc-extra-color
    only fires if the named color is ALSO absent from the puzzle —
    avoiding false positives where the rule treats walls/seeds via a
    generic predicate (`(or (= v 0) (= v 2))`) but the description
    correctly names the wall color from the puzzle ("gray(5) walls"
    when 5 IS in every train pair)."""
    findings = []
    rule_colors = colors_in_rule(rule)
    rule_color_set = {c for c, n in rule_colors.items() if n > 0}
    # The grounded set of "colors valid for this puzzle" is rule
    # literals OR colors actually present in the puzzle's image data.
    grounded = rule_color_set | (puzzle_colors or set())
    strongly_used = {c for c, n in rule_colors.items() if n >= 4 and c != 0}

    # 1. Colors named in desc that don't appear in rule literally
    desc_color_set = set()
    for m in _DESC_COLOR_RE.finditer(desc):
        try:
            num = int(m.group(2))
        except Exception:
            continue
        desc_color_set.add(num)

    # If we have no puzzle_colors (canonical data didn't include train/test
    # for this task), we can't reliably ground the description's color
    # references — skip desc-extra-color to avoid false positives. The
    # rule-literal-only fallback overflags rules that use generic
    # predicates (e.g., `(or (= v 0) (= v 2))` accepts any non-{0,2}
    # color as a wall, but description correctly names the puzzle's
    # actual wall color which we can't verify here).
    if puzzle_colors is None or not puzzle_colors:
        extras = set()
    else:
        extras = desc_color_set - grounded
    for n in extras:
        # Downgraded to warn: many descriptions are more concrete than
        # their rule (puzzle has gray walls, rule treats non-bg/non-seed
        # generically). Real authoring errors (M86 contradictions,
        # fc5d964d color confusion) still surface here for review.
        findings.append({
            "kind": "desc-extra-color",
            "severity": "warn",
            "color_num": n,
            "color_name": COLOR_NAMES.get(n),
            "match": f"{COLOR_NAMES.get(n)}({n})",
            "suggest": f"description names `{COLOR_NAMES.get(n)}({n})` "
                       f"but rule has no literal {n}; check whether "
                       f"the rule is generic (false positive) or the "
                       f"description has the wrong color (real bug)",
        })

    # 2. desc-missing-color disabled — fundamentally noisy because rule
    # literals include framework/iteration code, not just the rule's
    # "subject" colors. Without parsing rule semantics we can't tell
    # which color is central.
    _ = strongly_used  # silence unused

    # 3. Bare digit color references — `fill with 7` instead of `orange(7)`
    sanitized = _DESC_COLOR_RE.sub("", desc)  # strip name(N) to avoid double-count
    for m in _DESC_BARE_NUM_RE.finditer(sanitized):
        n = int(m.group(1))
        findings.append({
            "kind": "desc-bare-number",
            "severity": "warn",
            "color_num": n,
            "color_name": COLOR_NAMES.get(n),
            "match": str(n),
            "offset": m.start(),
            "suggest": f"`{n}` in prose probably means `{COLOR_NAMES.get(n)}({n})`",
        })

    return findings


def auto_fix(desc: str) -> str:
    """Replace bare-digit color refs with `name(N)`. Only applies the
    desc-bare-number fix (the easy mechanical one). Other findings need
    human/LLM review."""
    def _replace(m):
        # Recover the prefix span (everything up to the digit) — this
        # is the part of the match before the trailing digit.
        digit = m.group(1)
        full = m.group(0)
        prefix = full[: full.rfind(digit)]
        n = int(digit)
        name = COLOR_NAMES.get(n)
        if name is None:
            return full
        return f"{prefix}{name}({n})"
    return _DESC_BARE_NUM_RE.sub(_replace, desc)


def collect():
    rows = []
    with (ROOT / "data/canonical/puzzles.jsonl").open() as f:
        for line in f:
            try:
                r = json.loads(line)
            except Exception:
                continue
            tid = r.get("task_id")
            desc = r.get("written_solution") or ""
            rule = r.get("program_solution") or ""
            if not (tid and desc and rule):
                continue
            # Collect colors from train + test pairs
            puzzle_colors: set[int] = set()
            for split in ("train", "test"):
                for pair in r.get(split) or []:
                    if not isinstance(pair, dict):
                        continue
                    for grid_key in ("input", "output"):
                        grid = pair.get(grid_key) or []
                        if not isinstance(grid, list):
                            continue
                        for row in grid:
                            # Cells may be ints (canonical) or single-char
                            # strings (some legacy bank formats).
                            for v in row:
                                if isinstance(v, int) and 0 <= v <= 9:
                                    puzzle_colors.add(v)
                                elif isinstance(v, str) and len(v) == 1 and v.isdigit():
                                    puzzle_colors.add(int(v))
            rows.append({"tid": tid, "desc": desc.strip(),
                         "rule": rule.strip(),
                         "puzzle_colors": puzzle_colors})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--show-each", action="store_true",
                    help="print every finding (default: just summary)")
    args = ap.parse_args()

    rows = collect()
    print(f"linting {len(rows)} (description, rule) pairs", file=sys.stderr)

    by_kind = Counter()
    by_severity = Counter()
    n_clean = 0
    flagged = []
    for r in rows[: args.limit or None]:
        f = lint_one(r["desc"], r["rule"], r.get("puzzle_colors"))
        if not f:
            n_clean += 1
            continue
        flagged.append({"tid": r["tid"], "desc": r["desc"], "findings": f})
        for finding in f:
            by_kind[finding["kind"]] += 1
            by_severity[finding["severity"]] += 1

    print(f"\n=== summary ===")
    print(f"  pairs scanned: {len(rows[: args.limit or None])}")
    print(f"  clean:         {n_clean} ({n_clean / max(len(rows), 1):.1%})")
    print(f"  flagged:       {len(flagged)}")
    print(f"  by kind:       {dict(by_kind)}")
    print(f"  by severity:   {dict(by_severity)}")

    if args.show_each:
        for r in flagged[:50]:
            print(f"\n[{r['tid']}]")
            print(f"  DESC: {r['desc'][:200]}")
            for f in r["findings"]:
                print(f"  {f['kind']}: {f.get('suggest')}")
    else:
        print(f"\nfirst 10 flagged:")
        for r in flagged[:10]:
            kinds = Counter(f["kind"] for f in r["findings"])
            print(f"  {r['tid']:55s}  {dict(kinds)}")

    out = Path("/tmp/desc_rule_consistency.jsonl")
    with out.open("w") as f:
        for r in flagged:
            f.write(json.dumps(r) + "\n")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
