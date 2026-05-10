"""Generator for arc_puzzle_bank_twentieth21:M134.

A full wall of 8s receives straight shadows from every colored cell on one
side of the wall.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, orientation, texture.
Degenerates: no_wall, no_objects, both_sides.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6a8c2662e37c"
VERSION = "1.1.0"
TASK_ID = "6a8c2662e37c"
SUMMARY = "Non-wall colored cells cast horizontal or vertical shadows to an 8 wall."

INVARIANTS = [
    "there is exactly one full row or column of color 8",
    "all nonzero non-8 cells lie on one side of the wall",
    "the wall and original object cells are preserved",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_wall", "no_objects", "both_sides")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "orientation":    {"type": "int", "default": "rng 0..1",
                       "valid": "0 vertical, 1 horizontal"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "wall_with_one_side_blob",
                       "valid": "wall_with_one_side_blob"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_BLOB = [(0, 0), (1, 0), (1, 1), (2, 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 11, 13)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 11)
    orientation = ctx.draw_int("orientation", 0, 1)
    g = full_grid(h, w, 0)
    colors = [2, 3, 4, 5]
    if orientation == 0:
        wall = rng.randint(3, w - 4)
        for r in range(h):
            g[r][wall] = 8
        side_left = rng.choice([True, False])
        top = rng.randint(1, h - 4)
        left = rng.randint(0, wall - 3) if side_left else rng.randint(wall + 1, w - 3)
        for i, (dr, dc) in enumerate(_BLOB):
            g[top + dr][left + dc] = colors[i % len(colors)]
    else:
        wall = rng.randint(3, h - 4)
        for c in range(w):
            g[wall][c] = 8
        side_top = rng.choice([True, False])
        top = rng.randint(0, wall - 3) if side_top else rng.randint(wall + 1, h - 3)
        left = rng.randint(1, w - 4)
        for i, (dr, dc) in enumerate(_BLOB):
            g[top + dr][left + dc] = colors[i % len(colors)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_wall":
        # Object but no 8-wall — rule has no shadow target row/column.
        for dr, dc in _BLOB:
            g[2 + dr][2 + dc] = 4
        return g
    if name == "no_objects":
        # Wall but no colored cells — rule has nothing to project shadows
        # from.
        for r in range(h): g[r][4] = 8
        return g
    if name == "both_sides":
        # 8-wall with colored cells on BOTH sides — rule's "all on one
        # side" precondition fails; shadow direction is ambiguous.
        for r in range(h): g[r][4] = 8
        g[2][1] = 4; g[2][2] = 5
        g[5][6] = 6; g[5][7] = 7
        return g
    return g
