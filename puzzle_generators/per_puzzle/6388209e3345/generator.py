"""Generator for arc_puzzle_bank_twentyfirst21:H143.

Combinatorial axes (8): match_index, transform, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_query, no_protos, ambiguous_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6388209e3345"
VERSION = "1.1.0"
TASK_ID = "6388209e3345"
SUMMARY = "Match a query support to one of two canonical prototype panels."

INVARIANTS = [
    "the input has two 3x3 prototype panels and one query panel",
    "the query support is a symmetry of exactly one prototype",
    "the canonical output is the matched prototype in its original color",
    "prototype supports have different cell counts to avoid ambiguity",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_query", "no_protos", "ambiguous_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "match_index":    {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "transform":      {"type": "enum", "default": "rng", "valid": "id|r1|r2|r3|fh|fv|tr|atr"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "4", "valid": "3..5"},
    "position_bias":  {"type": "str", "default": "two_protos_one_query",
                       "valid": "two_protos_one_query"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "3..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PROTOS = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 2)],
]
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


def _paint_panel(g, panel, cells, color):
    left = panel * 4
    for r, c in cells:
        g[r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    match_index = ctx.draw_int("match_index", 0, 1)
    if difficulty == "easy":
        code = ctx.draw_choice("transform", ["id", "fh"])
    elif difficulty == "hard":
        code = ctx.draw_choice("transform", ["r1", "r3", "tr", "atr"])
    else:
        code = ctx.draw_choice("transform", _CODES)
    proto_colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], 2)
    query_color = rng.choice([4, 6, 7, 9])

    g = full_grid(3, 11, 0)
    for sep in (3, 7):
        for r in range(3):
            g[r][sep] = 8
    for idx, cells in enumerate(_PROTOS):
        _paint_panel(g, idx, cells, proto_colors[idx])
    _paint_panel(g, 2, _xform(_PROTOS[match_index], code), query_color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(3, 11, 0)
    for sep in (3, 7):
        for r in range(3):
            g[r][sep] = 8
    if name == "no_query":
        # Query panel empty — rule has nothing to match.
        _paint_panel(g, 0, _PROTOS[0], 4)
        _paint_panel(g, 1, _PROTOS[1], 5)
        return g
    if name == "no_protos":
        # Both proto panels empty — rule has no candidate to match against.
        _paint_panel(g, 2, _PROTOS[0], 6)
        return g
    if name == "ambiguous_match":
        # Both protos have same shape — query matches both.
        _paint_panel(g, 0, _PROTOS[0], 4)
        _paint_panel(g, 1, _PROTOS[0], 5)
        _paint_panel(g, 2, _PROTOS[0], 6)
        return g
    return g
