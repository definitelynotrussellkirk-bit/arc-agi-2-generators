"""Generator for arc_puzzle_bank_twentieth21:H136 — match query to prototype family.

Choose which canonical prototype family matches a transformed query.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: identical_protos (the two prototypes are identical →
query matches both, rule's "exactly one" fails), no_query (query
panel empty → rule's matcher has nothing to compare), query_matches_neither
(query is a third unrelated shape → rule's selector finds no match).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a51a8e285ce9"
VERSION = "1.1.0"
TASK_ID = "a51a8e285ce9"
SUMMARY = "Choose which canonical prototype family matches a transformed query."

INVARIANTS = [
    "the input has two 4x4 prototype panels and one 4x4 query panel",
    "the query support is a symmetry of exactly one prototype support",
    "prototype families have different cell counts to avoid ambiguity",
    "the output is the matched prototype support recolored by the query color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("identical_protos", "no_query", "query_matches_neither")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "match_index":    {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "transform":      {"type": "enum", "default": "rng", "valid": "id|r1|r2|r3|fh|fv|tr|atr"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "two_protos_one_query",
                       "valid": "two_protos_one_query"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "fixed_layout", "valid": "fixed_layout"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PROTOS = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
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
    left = panel * 5
    for r, c in cells:
        g[r][left + c] = color


def _make_separators(g):
    for sep in (4, 9):
        for r in range(4):
            g[r][sep] = 8


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    match_index = ctx.draw_int("match_index", 0, 1)
    code = ctx.draw_choice("transform", _CODES)
    proto_colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], 2)
    query_color = rng.choice([4, 6, 7, 9])

    g = full_grid(4, 14, 0)
    _make_separators(g)
    for idx, cells in enumerate(_PROTOS):
        _paint_panel(g, idx, cells, proto_colors[idx])
    _paint_panel(g, 2, _xform(_PROTOS[match_index], code), query_color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(4, 14, 0)
    _make_separators(g)
    if name == "identical_protos":
        # Both prototypes are identical → query matches both;
        # rule's "exactly one match" precondition fails.
        proto = _PROTOS[0]
        _paint_panel(g, 0, proto, 1)
        _paint_panel(g, 1, proto, 3)
        _paint_panel(g, 2, proto, 4)
        return g
    if name == "no_query":
        # Query panel empty → rule's matcher has nothing to compare;
        # output undefined.
        _paint_panel(g, 0, _PROTOS[0], 1)
        _paint_panel(g, 1, _PROTOS[1], 3)
        return g
    if name == "query_matches_neither":
        # Query is unrelated → rule's selector finds no match.
        _paint_panel(g, 0, _PROTOS[0], 1)
        _paint_panel(g, 1, _PROTOS[1], 3)
        _paint_panel(g, 2, [(0, 0), (1, 1), (2, 2), (3, 3)], 4)
        return g
    return g
