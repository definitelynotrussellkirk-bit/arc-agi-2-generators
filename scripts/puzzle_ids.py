"""Stable identifiers for every puzzle.

Every puzzle row gets TWO derived fields alongside its `task_id`:

  content_hash : 12-char hex of SHA256 over the canonical-JSON of the
                 puzzle's (train + test) grid pairs. Content-addressed —
                 two puzzles with identical grids get the same hash,
                 regardless of which bank they live in. Useful for
                 dedup / cross-bank matching.

  slug         : lowercase, underscore-separated, max 20 words,
                 [a-z0-9_] only. Derived from `name` if present,
                 otherwise the first sentence of `description`/
                 `written_rule`, otherwise a `puzzle_<content_hash>`
                 fallback. Human-readable canonical id.

Both are deterministic: given the same puzzle, the same hash/slug
come out.

Used by build_canonical_puzzles.py (adds them to puzzles.jsonl) and
build_puzzle_db.py (adds them to puzzle_db.jsonl). The linter checks
agreement between the two.
"""
from __future__ import annotations
import hashlib
import json
import re


MAX_SLUG_WORDS = 20


def _canonical_pair_list(pairs) -> list:
    """Normalize a pair-list container into a deterministic shape:
    list[{"input": grid, "output": grid}]. Sorts nothing (order matters
    in ARC data). Handles:
      - None
      - list[dict]
      - a single dict (v2_meta_puzzles test-field quirk)
    """
    if pairs is None:
        return []
    if isinstance(pairs, dict):
        return [pairs]
    out = []
    for p in pairs:
        if not isinstance(p, dict):
            continue
        out.append({
            "input": _normalize_grid(p.get("input")),
            "output": _normalize_grid(p.get("output")),
        })
    return out


def _normalize_grid(g):
    """Convert list[str] ('0303000' compact ARC notation) to
    list[list[int]]. Returns g unchanged if already in list-of-lists
    form. Returns None on anything unrecognizable.
    """
    if g is None:
        return None
    if isinstance(g, list) and g and isinstance(g[0], list):
        return g
    if isinstance(g, list) and g and isinstance(g[0], str):
        try:
            return [[int(ch) for ch in row] for row in g]
        except ValueError:
            return None
    return None


def content_hash(entry: dict) -> str:
    """12-char hex hash over the canonical (train, test, solution_text)
    representation.

    Two puzzles with identical grids hash to the same string regardless
    of bank / name / difficulty — that's intentional, for dedup.

    Edge case: a rule-only template has empty train AND empty test.
    Without any grid data, every rule-only puzzle would collide on the
    same "empty" hash. To keep rule-only entries distinct, we mix the
    solution text into the hash ONLY when both grid slots are empty.
    Non-empty grid cases ignore the solution text so two banks that
    describe the same puzzle in different words still collide.
    """
    train = _canonical_pair_list(entry.get("train"))
    test = _canonical_pair_list(
        entry.get("test")
        or ([{"input": entry.get("test_input"),
              "output": entry.get("test_output")}]
            if entry.get("test_input") is not None else [])
    )
    payload = {"train": train, "test": test}
    if not train and not test:
        # Rule-only — fall back to solution text so templates stay
        # distinguishable. Prefer the machine-readable code over the
        # written description.
        payload["_ruleonly_solution"] = (
            entry.get("program_solution")
            or entry.get("written_solution")
            # Backwards-compat reads — bank source files still use these:
            or entry.get("reference_program")
            or entry.get("program_solution_python")
            or entry.get("written_rule")
            or entry.get("task_id", "")
        )
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:12]


def slugify(text: str, max_words: int = MAX_SLUG_WORDS) -> str:
    """Convert free-form text into a lowercase_underscore_slug with at
    most `max_words` words. Strips anything outside [a-z0-9_]; collapses
    whitespace and punctuation to a single underscore.
    """
    if not text:
        return ""
    # Lowercase; keep alnum + whitespace
    t = re.sub(r"[^a-z0-9\s]+", " ", text.lower())
    words = [w for w in t.split() if w]
    if not words:
        return ""
    words = words[:max_words]
    return "_".join(words)


# ---------------------------------------------------------------
# Primitives extraction — what grid-ops does a solution rely on?
# Useful for tagging, retrieval, and capability coverage reports.
# ---------------------------------------------------------------

# Racket keywords / variable sugar we don't want in the primitives list
_RACKET_STOPWORDS = frozenset({
    "rule!", "lambda", "let", "let*", "letrec", "if", "cond", "else",
    "begin", "define", "when", "unless", "and", "or", "not",
    "for", "for/list", "for/sum", "for/fold", "for/or", "for/and",
    "for/first", "for*", "in-list", "in-range", "in-naturals",
    "first", "second", "third", "fourth", "rest", "list",
    "quote", "map", "filter", "reduce", "apply",
    "+", "-", "*", "/", "=", "<", ">", "<=", ">=", "!=",
    "#t", "#f",
    # common variable names
    "g", "grid", "r", "c", "v", "i", "j", "k", "h", "w",
    "x", "y", "acc", "ob", "obj", "cell", "cells", "objs",
})


def extract_racket_primitives(rule_text: str, max_n: int = 40) -> list[str]:
    """Return the set of primitive-like symbols used in a Racket rule,
    excluding keywords / bound variables. Output is sorted and deduped.
    Rough but useful for tagging / retrieval.
    """
    if not rule_text:
        return []
    # Match Racket-legal identifiers (letters, digits, -, !, ?, *)
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9\-!?*/><=+]*", rule_text)
    seen: set[str] = set()
    for t in tokens:
        if t in _RACKET_STOPWORDS:
            continue
        # Skip single-letter tokens (usually variables)
        if len(t) < 2:
            continue
        # Skip pure numbers (regex already rejects) and dotted names
        seen.add(t)
        if len(seen) >= max_n:
            break
    return sorted(seen)


def extract_python_primitives(src: str, max_n: int = 40) -> list[str]:
    """Parse `src` as Python, walk the AST, collect the names of every
    function call target. Stops at max_n for pathologically large
    solutions. Falls back to [] on parse failure.
    """
    if not src:
        return []
    try:
        import ast as _ast
        tree = _ast.parse(src)
    except Exception:
        return []
    seen: set[str] = set()
    for node in _ast.walk(tree):
        if isinstance(node, _ast.Call):
            fn = node.func
            if isinstance(fn, _ast.Name):
                seen.add(fn.id)
            elif isinstance(fn, _ast.Attribute):
                seen.add(fn.attr)
            if len(seen) >= max_n:
                break
    # Drop trivial-builtin noise
    seen -= {"len", "range", "print", "enumerate", "zip", "sorted",
             "list", "set", "dict", "tuple", "str", "int", "float",
             "bool", "map", "filter", "abs", "min", "max", "sum",
             "all", "any"}
    return sorted(seen)


def compute_puzzle_ids(entry: dict) -> tuple[str, str]:
    """Compute (content_hash, slug) for an already-canonical-shaped
    entry (same dict the canonical JSONL line carries).

    Falls back through title → written_solution → task_id when
    choosing the slug source. Legacy bank source field names
    (`name`, `written_rule`, `description`, `pattern`) still work as
    last-resort reads since bank source files haven't been rewritten.
    """
    ch = content_hash(entry)
    slug_source = (entry.get("title")
                   or entry.get("written_solution")
                   # Backwards-compat reads:
                   or entry.get("name")
                   or entry.get("written_rule")
                   or entry.get("description")
                   or entry.get("pattern")
                   or entry.get("task_id", ""))
    slug = slugify(slug_source)
    if not slug:
        slug = f"puzzle_{ch}"
    return ch, slug
