"""Generator for arc_puzzle_bank_seventh21:E48.

Rule: each row has a 1-marker immediately followed by a color cell;
the color extends as a ray rightward until it hits a 9 stopper or
the edge.

Combinatorial axes (8): grid_h, grid_w, palette_kind, launchers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_launcher, missing_color_cell, launcher_at_right_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ae370359ef71"
VERSION = "1.1.0"
TASK_ID = "ae370359ef71"
SUMMARY = "Rows contain a 1/color launcher whose color ray travels right."

INVARIANTS = [
    "background is 0",
    "each active row has a 1 immediately followed by a nonzero non-9 color",
    "ray path to the right is initially empty until a stopper or edge",
    "optional stopper color is 9",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_launcher", "missing_color_cell", "launcher_at_right_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "3..14"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "launchers":      {"type": "int", "default": "rng 2..4", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 2..7", "valid": "1..7"},
    "position_bias":  {"type": "str", "default": "row_left", "valid": "row_left"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..7", "valid": "1..7"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 9, 10)
        target = min(ctx.draw_int("launchers", 2, 3), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 12, 13)
        target = min(ctx.draw_int("launchers", 3, 4), h)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 9, 13)
        target = min(ctx.draw_int("launchers", 2, 4), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), target)
    for r in rows:
        c = rng.randint(0, w - 5)
        color = rng.choice([2, 3, 4, 5, 6, 7, 8])
        g[r][c] = 1
        g[r][c + 1] = color
        if rng.randrange(2) == 0:
            g[r][rng.randint(c + 3, w - 1)] = 9
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 11
    g = full_grid(h, w, 0)
    if name == "no_launcher":
        # color cell with no preceding 1 → no ray to fire
        g[1][3] = 4
        g[3][2] = 7
        return g
    if name == "missing_color_cell":
        # 1 marker without a color cell after it → ray color undefined
        g[1][2] = 1
        g[3][1] = 1
        return g
    if name == "launcher_at_right_edge":
        # 1 at last column → no room for color cell or ray
        g[1][w - 1] = 1
        g[3][w - 2] = 1; g[3][w - 1] = 4
        return g
    return g
