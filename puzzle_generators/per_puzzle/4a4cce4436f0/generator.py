"""Generator for arc_puzzle_bank_twelfth_21_bundle:hard_81_fill_partitioned_chambers_by_internal_keys.

Combinatorial axes (8): grid_h, grid_w, palette_kind, wall_style,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_keys, multiple_keys_per_chamber.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4a4cce4436f0"
VERSION = "1.1.0"
TASK_ID = "4a4cce4436f0"
SUMMARY = "Fill each wall-partitioned chamber with its single internal key color."

INVARIANTS = [
    "color 5 cells form full divider walls that partition the grid into chambers",
    "each fillable chamber contains exactly one non-wall nonzero key color",
    "only zero cells inside those single-key chambers are filled",
    "walls and original key cells are preserved",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_keys", "multiple_keys_per_chamber")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9..9"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "wall_style":     {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "5walls_with_internal_keys",
                       "valid": "5walls_with_internal_keys"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PALETTES = [
    [2, 3, 4, 6],
    [1, 7, 8, 9],
    [2, 6, 7, 8],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        wall_style = ctx.draw_int("wall_style", 0, 0)
    elif difficulty == "hard":
        wall_style = ctx.draw_int("wall_style", 0, 3)
    else:
        wall_style = ctx.draw_int("wall_style", 0, 3)
    palette = ctx.draw_int("palette", 0, len(_PALETTES) - 1)
    colors = _PALETTES[palette]
    g = full_grid(9, 9, 0)

    wall_row = 4 if wall_style in (0, 2) else 3
    wall_col = 4 if wall_style in (0, 1) else 5
    for c in range(9):
        g[wall_row][c] = 5
    for r in range(9):
        g[r][wall_col] = 5

    chambers = [
        (1, 1),
        (1, wall_col + 2),
        (wall_row + 2, 1),
        (wall_row + 2, wall_col + 2),
    ]
    for (r, c), color in zip(chambers, colors):
        if 0 <= r < 9 and 0 <= c < 9 and g[r][c] == 0:
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 0)
    if name == "no_walls":
        # keys without 5-walls → no chambers, nothing to fill
        g[2][2] = 4; g[2][6] = 6
        g[6][2] = 7; g[6][6] = 8
        return g
    if name == "no_keys":
        # walls without keys → chambers exist but no fill color
        for c in range(9): g[4][c] = 5
        for r in range(9): g[r][4] = 5
        return g
    if name == "multiple_keys_per_chamber":
        # one chamber has 2 different keys → ambiguous, "exactly one" fails
        for c in range(9): g[4][c] = 5
        for r in range(9): g[r][4] = 5
        g[1][1] = 4; g[2][2] = 6  # both in TL chamber
        g[1][7] = 7
        g[7][1] = 8
        return g
    return g
