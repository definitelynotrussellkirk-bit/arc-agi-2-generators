"""Generator for arc_additional_puzzle_bank_volume21:E145 — blue→cyan reflect across maroon divider.

Rule: blue cells are reflected across a maroon divider as cyan.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_blue, blue_on_right.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a6b5a6d9b5ef"
VERSION = "1.1.0"
TASK_ID = "a6b5a6d9b5ef"
SUMMARY = "Blue cells are reflected across a maroon divider as cyan."

INVARIANTS = [
    "background is 0",
    "there is a full-height maroon divider column",
    "blue source cells lie to the left of the divider",
    "reflected destinations are in bounds and off the divider",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_blue", "blue_on_right")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "grid_w":         {"type": "int", "default": "rng 9..15", "valid": "7..25"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 5..9", "valid": "1..20"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "blue_left_with_9_div",
                       "valid": "blue_left_with_9_div"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        n_cells = ctx.draw_int("n_cells", 4, 5)
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
    cells: set[tuple[int, int]] = set()
    for _ in range(200):
        if len(cells) >= n_cells:
            break
        cells.add((rng.randint(0, h - 1), rng.choice(left_cols)))
    for r, c in cells:
        g[r][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    axis = w // 2
    if name == "no_divider":
        # no maroon divider → axis undefined
        g[2][1] = 1; g[3][2] = 1
        return g
    if name == "no_blue":
        # divider but no blue source cells → no source cells, no mirror
        for r in range(h): g[r][axis] = 9
        return g
    if name == "blue_on_right":
        # blue on right side → reverses source/destination roles
        for r in range(h): g[r][axis] = 9
        g[2][axis + 1] = 1
        g[3][axis + 2] = 1
        return g
    return g
