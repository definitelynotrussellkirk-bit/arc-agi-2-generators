"""Generator for arc_additional_puzzles_21_set16_bundle:H106 — apply TL→TR transform to BL.

Rule: a 9 cross separates quadrants; the TL→TR transform is applied
to BL.

Combinatorial axes (8): grid_h, grid_w, palette_kind, command,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cross, identical_tl_tr, missing_tr.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "673e85a3c1cb"
VERSION = "1.1.0"
TASK_ID = "673e85a3c1cb"
SUMMARY = "A 9 cross separates quadrants; the TL->TR transform is applied to BL."

INVARIANTS = [
    "one full color-9 row and one full color-9 column split the grid",
    "the top-right quadrant is a transform of the top-left quadrant",
    "the inferred transform is applied to the bottom-left quadrant",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cross", "identical_tl_tr", "missing_tr")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9..9"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "command":        {"type": "choice", "default": "rot", "valid": "rot|flip"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "9cross_with_quadrant_transform",
                       "valid": "9cross_with_quadrant_transform"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _place(g, r, c, cells, color):
    for dr, dc in cells:
        g[r + dr][c + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    command = ctx.draw_choice("command", ["rot", "flip"])
    if "command" not in overrides:
        command = "rot" if sample_index % 2 == 0 else "flip"
    color = ctx.draw_color("color", exclude={0, 9})
    g = full_grid(9, 9, 0)
    for c in range(9):
        g[4][c] = 9
    for r in range(9):
        g[r][4] = 9
    tl = [(0, 0), (1, 0), (1, 1)]
    tr = [(0, 0), (0, 1), (1, 0)] if command == "rot" else [(0, 1), (1, 0), (1, 1)]
    bl = [(0, 0), (0, 1), (1, 1)]
    _place(g, 1, 1, tl, color)
    _place(g, 1, 6, tr, color)
    _place(g, 6, 1, bl, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 0)
    tl = [(0, 0), (1, 0), (1, 1)]
    tr = [(0, 0), (0, 1), (1, 0)]   # rot of tl
    bl = [(0, 0), (0, 1), (1, 1)]
    if name == "no_cross":
        # no 9 cross → quadrants undefined
        _place(g, 1, 1, tl, 4)
        _place(g, 1, 6, tr, 4)
        _place(g, 6, 1, bl, 4)
        return g
    for c in range(9): g[4][c] = 9
    for r in range(9): g[r][4] = 9
    if name == "identical_tl_tr":
        # TL == TR → no transform inferred (identity), output BL identical to BL
        _place(g, 1, 1, tl, 4)
        _place(g, 1, 6, tl, 4)   # identical
        _place(g, 6, 1, bl, 4)
        return g
    if name == "missing_tr":
        # TR quadrant empty → no transform to infer
        _place(g, 1, 1, tl, 4)
        _place(g, 6, 1, bl, 4)
        return g
    return g
