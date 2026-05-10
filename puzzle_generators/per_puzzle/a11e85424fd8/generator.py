"""Generator for arc_puzzle_bank_twentysecond21:H151.

Rule: find the candidate object whose support matches the query under a
dihedral transform; output cropped + recolored to the query color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_query, no_candidates, identical_candidates.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a11e85424fd8"
VERSION = "1.1.0"
TASK_ID = "a11e85424fd8"
SUMMARY = "Find the candidate object whose support matches the query symmetry."

INVARIANTS = [
    "the input has a 3x3 query panel and a wider candidate-object panel",
    "candidate objects are 4-connected and separated by background",
    "exactly one candidate support matches the query under a dihedral transform",
    "the output is that candidate cropped and recolored to the query color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_query", "no_candidates", "identical_candidates")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "transform":      {"type": "enum", "default": "rng",
                       "valid": "id|r1|r2|r3|fh|fv|tr|atr"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "query_with_two_candidates",
                       "valid": "query_with_two_candidates"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_QUERY = [(0, 0), (1, 0), (1, 1)]
_DISTRACTOR = [(0, 0), (0, 1), (1, 1), (2, 1)]
_CODES = ["id", "r1", "r2", "r3", "fh", "fv", "tr", "atr"]


def _normalize(cells):
    min_r = min(r for r, _ in cells)
    min_c = min(c for _, c in cells)
    return sorted((r - min_r, c - min_c) for r, c in cells)


def _dims(cells):
    return max(r for r, _ in cells) + 1, max(c for _, c in cells) + 1


def _xform(cells, code):
    h, w = _dims(cells)
    if code == "id":
        raw = cells
    elif code == "r1":
        raw = [(c, h - 1 - r) for r, c in cells]
    elif code == "r2":
        raw = [(h - 1 - r, w - 1 - c) for r, c in cells]
    elif code == "r3":
        raw = [(w - 1 - c, r) for r, c in cells]
    elif code == "fh":
        raw = [(r, w - 1 - c) for r, c in cells]
    elif code == "fv":
        raw = [(h - 1 - r, c) for r, c in cells]
    elif code == "tr":
        raw = [(c, r) for r, c in cells]
    else:
        raw = [(w - 1 - c, h - 1 - r) for r, c in cells]
    return _normalize(raw)


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    code = ctx.draw_choice("transform", _CODES)
    q_color = rng.choice([1, 2, 3, 6, 7, 9])
    hit_color = rng.choice([4, 5, 6, 7])
    other_color = rng.choice([2, 3, 4, 9])

    g = full_grid(3, 11, 0)
    for r in range(3):
        g[r][3] = 8
    _paint(g, 0, 0, _xform(_QUERY, code), q_color)
    _paint(g, 0, 4, _QUERY, hit_color)
    _paint(g, 0, 8, _DISTRACTOR, other_color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(3, 11, 0)
    for r in range(3):
        g[r][3] = 8
    if name == "no_query":
        # Query panel empty — rule has no shape to match against.
        _paint(g, 0, 4, _QUERY, 4)
        _paint(g, 0, 8, _DISTRACTOR, 6)
        return g
    if name == "no_candidates":
        # Query but no candidate objects — rule's selector finds
        # nothing.
        _paint(g, 0, 0, _QUERY, 2)
        return g
    if name == "identical_candidates":
        # Both candidates identical to the query — rule's
        # "exactly one matches" tie-break ambiguous.
        _paint(g, 0, 0, _QUERY, 2)
        _paint(g, 0, 4, _QUERY, 4)
        _paint(g, 0, 8, _QUERY, 6)
        return g
    return g
