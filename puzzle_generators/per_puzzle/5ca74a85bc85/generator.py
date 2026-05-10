"""Generator for arc_additional_puzzle_bank_volume7:E49 — mirror left cells across maroon divider.

Rule: colored cells are mirrored across a full-height maroon divider,
preserving color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_left_cells, right_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5ca74a85bc85"
VERSION = "1.1.0"
TASK_ID = "5ca74a85bc85"
SUMMARY = "Colored cells are mirrored across a full-height maroon divider, preserving color."

INVARIANTS = [
    "background is 0",
    "there is a full-height maroon divider column",
    "source colored cells lie to the left of the divider",
    "reflected destinations are in bounds and initially empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_left_cells", "right_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "grid_w":         {"type": "int", "default": "rng 9..15", "valid": "7..25"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 5..9", "valid": "1..20"},
    "palette_size":   {"type": "int", "default": "rng 2..6", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "left_cells_with_divider",
                       "valid": "left_cells_with_divider"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..7", "valid": "2..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        n_cells = ctx.draw_int("n_cells", 5, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 13, 15)
        n_cells = ctx.draw_int("n_cells", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 9, 15)
        n_cells = ctx.draw_int("n_cells", 5, 9)
    rng = ctx.draw_rng("placement")
    axis = rng.randint(3, w - 4)
    left_cols = list(range(max(0, 2 * axis - (w - 1)), axis))
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][axis] = 9
    colors = [1, 2, 3, 4, 5, 6, 7, 8]
    cells: set[tuple[int, int]] = set()
    for _ in range(200):
        if len(cells) >= n_cells:
            break
        cells.add((rng.randint(0, h - 1), rng.choice(left_cols)))
    for i, (r, c) in enumerate(sorted(cells)):
        g[r][c] = colors[i % len(colors)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # left cells but no maroon divider → no axis to mirror across
        g[2][1] = 4
        g[5][3] = 6
        return g
    if name == "no_left_cells":
        # divider but left side blank → nothing to mirror
        for r in range(h): g[r][5] = 9
        return g
    if name == "right_already_filled":
        # right side already has cells → mirror destination collides
        for r in range(h): g[r][5] = 9
        g[2][2] = 4; g[2][8] = 6
        g[5][3] = 7; g[5][7] = 8
        return g
    return g
