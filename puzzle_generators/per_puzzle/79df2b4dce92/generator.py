"""Generator for arc_puzzle_bank_21_set23_s:S23_H4.

Rule: top-row prototype library labels rotated motifs in bottom row;
output strip names matching prototypes.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_library, no_query, all_same_label.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "79df2b4dce92"
VERSION = "1.1.0"
TASK_ID = "79df2b4dce92"
SUMMARY = "Look up rotated query motifs in a labeled top-row prototype library."

INVARIANTS = [
    "the grid is a 2x4 lattice of 3x3 tiles separated by color 9",
    "top tiles contain label colors at local (0,0) plus prototype motif cells",
    "bottom tiles are rotated copies of the prototypes",
    "the output strip contains the matching prototype labels in query order",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_library", "no_query", "all_same_label")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "order":          {"type": "int", "default": "rng 0..5", "valid": "0..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "2x4_tile_lattice",
                       "valid": "2x4_tile_lattice"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 1), (1, 1), (1, 2)],
    [(0, 2), (1, 2), (2, 2)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 1), (0, 2), (1, 0), (1, 1)],
]

_ORDERS = [
    [0, 1, 2, 3],
    [1, 3, 0, 2],
    [2, 0, 3, 1],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [1, 0, 3, 2],
]


def _rot90(cells):
    return [(c, 2 - r) for r, c in cells]


def _rot(cells, turns):
    out = list(cells)
    for _ in range(turns % 4):
        out = _rot90(out)
    return out


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def _tile_origin(row_idx, col_idx):
    return row_idx * 4, col_idx * 4


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    order = _ORDERS[ctx.draw_int("order", 0, len(_ORDERS) - 1)]
    labels = rng.sample([1, 3, 4, 5, 6, 7, 8], 4)
    g = full_grid(7, 15, 0)
    for r in range(7):
        for c in (3, 7, 11):
            g[r][c] = 9
    for c in range(15):
        g[3][c] = 9

    for col, (label, cells) in enumerate(zip(labels, _SHAPES)):
        top, left = _tile_origin(0, col)
        g[top][left] = label
        _paint(g, top, left, cells, 2)

    for col, proto_idx in enumerate(order):
        top, left = _tile_origin(1, col)
        _paint(g, top, left, _rot(_SHAPES[proto_idx], rng.randrange(4)), 2)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 15, 0)
    for r in range(7):
        for c in (3, 7, 11): g[r][c] = 9
    for c in range(15): g[3][c] = 9
    if name == "no_library":
        # Top tiles empty (no prototypes) — rule has no library
        # to look up bottom-row motifs against.
        for col in range(4):
            top, left = _tile_origin(1, col)
            _paint(g, top, left, _SHAPES[col], 2)
        return g
    if name == "no_query":
        # Library present but bottom tiles empty — rule has nothing
        # to classify; output strip undefined.
        labels = [1, 3, 4, 5]
        for col, (label, cells) in enumerate(zip(labels, _SHAPES)):
            top, left = _tile_origin(0, col)
            g[top][left] = label
            _paint(g, top, left, cells, 2)
        return g
    if name == "all_same_label":
        # All 4 prototypes share the same label color — rule's
        # output strip cannot discriminate prototypes.
        for col, cells in enumerate(_SHAPES):
            top, left = _tile_origin(0, col)
            g[top][left] = 4
            _paint(g, top, left, cells, 2)
        for col in range(4):
            top, left = _tile_origin(1, col)
            _paint(g, top, left, _SHAPES[col], 2)
        return g
    return g
