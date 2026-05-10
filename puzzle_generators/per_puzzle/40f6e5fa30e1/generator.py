"""Generator for arc_additional_puzzle_bank_volume16:M112.

Rule: blank cells with cardinal contact to both colors 1 and 2 become 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_anchors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_color_1, no_color_2, no_targets.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "40f6e5fa30e1"
VERSION = "1.1.0"
TASK_ID = "40f6e5fa30e1"
SUMMARY = "Blank cells with cardinal contact to both colors 1 and 2 become 8."

INVARIANTS = [
    "target cells are zero before transformation",
    "each target has at least one cardinal neighbor of color 1 and one of color 2",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_color_1", "no_color_2", "no_adjacency")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_anchors":      {"type": "int", "default": "3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "anchor_pairs",
                       "valid": "anchor_pairs"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    anchors = [(2, 2), (h - 3, w - 3), (2, w - 3)]
    for i, (r, c) in enumerate(anchors):
        if 0 < r < h - 1 and 0 < c < w - 1:
            if i % 2 == 0:
                g[r][c - 1] = 1
                g[r][c + 1] = 2
            else:
                g[r - 1][c] = 1
                g[r + 1][c] = 2
    for _ in range(3):
        r = rng.randint(0, h - 1)
        c = rng.randint(0, w - 1)
        if g[r][c] == 0:
            g[r][c] = rng.choice([1, 2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_color_1":
        # only color 2 cells → no cell can have a 1-neighbor, rule paints nothing
        g[2][1] = 2; g[2][3] = 2
        g[5][4] = 2
        return g
    if name == "no_color_2":
        # only color 1 cells → no cell can have a 2-neighbor
        g[2][1] = 1; g[2][3] = 1
        g[5][4] = 1
        return g
    if name == "no_adjacency":
        # 1s and 2s present but never share a cardinal neighbor → no targets
        g[1][1] = 1
        g[6][6] = 2
        return g
    return g
