"""Generator for arc_additional_puzzles_21_set18_bundle:E126 — Iterative 2x2 fill.

Rule: scan 2x2 windows; whenever 3 of 4 cells are same non-zero, fill
the 4th. Iterate.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shapes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_l_pattern, all_complete_squares, mixed_color_l.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8b7d1307ff93"
VERSION = "1.1.0"
TASK_ID = "8b7d1307ff93"
SUMMARY = "2-3 L-shaped 3-cell groups of distinct colors, well separated."

INVARIANTS = [
    "2-3 L-shapes (3 cells of one color forming an L)",
    "each L's missing 4th cell is 0",
    "shapes well-separated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_l_pattern", "all_complete_squares", "mixed_color_l")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shapes":       {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "separated_l_shapes",
                       "valid": "separated_l_shapes"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

LSHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 1), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (1, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_shapes = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n_shapes)
    placed = []
    for color in palette:
        for _ in range(40):
            shape = rng.choice(LSHAPES)
            r0 = rng.randint(0, h - 2); c0 = rng.randint(0, w - 2)
            if any(abs(r0 - pr) < 4 and abs(c0 - pc) < 4 for pr, pc in placed):
                continue
            for dr, dc in shape:
                g[r0 + dr][c0 + dc] = color
            placed.append((r0, c0))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_l_pattern":
        # blank → no 2x2 windows with 3 same cells
        return g
    if name == "all_complete_squares":
        # 2x2 already filled → no empty corner to fill
        for dr in range(2):
            for dc in range(2):
                g[1 + dr][1 + dc] = 4
        for dr in range(2):
            for dc in range(2):
                g[4 + dr][5 + dc] = 6
        return g
    if name == "mixed_color_l":
        # 2x2 has 3 cells of 3 different colors → no shared color
        g[1][1] = 4; g[1][2] = 6; g[2][1] = 7
        return g
    return g
