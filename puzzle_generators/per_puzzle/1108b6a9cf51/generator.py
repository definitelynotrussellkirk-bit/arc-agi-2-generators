"""Generator for arc_additional_puzzles_21_set16_bundle:E106 — three 3x3 panels: dihedral A→B applied to C.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_separators, identical_panels, no_query.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1108b6a9cf51"
VERSION = "1.1.0"
TASK_ID = "1108b6a9cf51"

SUMMARY = "Three 3x3 panels: infer the A-to-B dihedral transform and apply it to C."

INVARIANTS = [
    "background is 0",
    "panel separator columns are 9",
    "A and B are 3x3 panels related by one dihedral transform",
    "output is the same transform applied to the third 3x3 panel",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separators", "identical_panels", "no_query")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "transform":      {"type": "int", "default": "rng 1..7", "valid": "0..7"},
    "a_cells":        {"type": "int", "default": "rng 4..6", "valid": "1..9"},
    "c_cells":        {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "abc_panel_strip",
                       "valid": "abc_panel_strip"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _xform(grid, code):
    n = len(grid)
    if code == 0:
        return [row[:] for row in grid]
    if code == 1:
        return [[grid[n - 1 - r][c] for r in range(n)] for c in range(n)]
    if code == 2:
        return [row[::-1] for row in grid[::-1]]
    if code == 3:
        return [[grid[r][n - 1 - c] for r in range(n)] for c in range(n)]
    if code == 4:
        return [row[::-1] for row in grid]
    if code == 5:
        return grid[::-1]
    if code == 6:
        return [[grid[c][r] for c in range(n)] for r in range(n)]
    return [[grid[n - 1 - c][n - 1 - r] for c in range(n)] for r in range(n)]


def _panel(rng, colors, count):
    g = full_grid(3, 3, 0)
    for r, c in rng.sample([(r, c) for r in range(3) for c in range(3)], count):
        g[r][c] = rng.choice(colors)
    return g


def _paste(out, panel, left):
    for r in range(3):
        for c in range(3):
            out[r][left + c] = panel[r][c]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    colors = [1, 2, 3, 4, 5, 6, 7, 8]
    if difficulty == "easy":
        a_lo, a_hi = 3, 4
        c_lo, c_hi = 3, 4
    elif difficulty == "hard":
        a_lo, a_hi = 5, 7
        c_lo, c_hi = 5, 7
    else:
        a_lo, a_hi = 4, 6
        c_lo, c_hi = 3, 6
    for _ in range(100):
        code = ctx.draw_int("transform", 1, 7)
        a = _panel(rng, colors, ctx.draw_int("a_cells", a_lo, a_hi))
        b = _xform(a, code)
        if a == b:
            continue
        c = _panel(rng, colors, ctx.draw_int("c_cells", c_lo, c_hi))
        g = full_grid(3, 11, 0)
        for r in range(3):
            g[r][3] = 9
            g[r][7] = 9
        _paste(g, a, 0)
        _paste(g, b, 4)
        _paste(g, c, 8)
        return g
    raise ValueError("could not build asymmetric transform-transfer panels")


def _draw_from_degenerate(name, rng):
    g = full_grid(3, 11, 0)
    a = [[1, 1, 0], [0, 1, 0], [0, 0, 0]]
    b = [[0, 1, 1], [0, 1, 0], [0, 0, 0]]
    c = [[2, 2, 0], [0, 2, 0], [0, 0, 2]]
    if name == "no_separators":
        # No 9-cols — rule's panel decomposition fails;
        # A/B/C boundaries undefined.
        _paste(g, a, 0); _paste(g, b, 4); _paste(g, c, 8)
        return g
    for r in range(3):
        g[r][3] = 9; g[r][7] = 9
    if name == "identical_panels":
        # A and B identical — inferred transform is identity;
        # rule's transform branch invisible on C.
        _paste(g, a, 0); _paste(g, a, 4); _paste(g, c, 8)
        return g
    if name == "no_query":
        # A→B shows transform but C is empty — rule has no
        # query to apply transform to.
        _paste(g, a, 0); _paste(g, b, 4)
        return g
    return g
