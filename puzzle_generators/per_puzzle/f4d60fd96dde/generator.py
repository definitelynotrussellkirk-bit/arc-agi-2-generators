"""Generator for arc_puzzle_bank_21_next:easy_c04 — Fill 0 in 2x2 with 3 same-color cells.

Rule: for each 2×2 sub-block where exactly 3 cells share a single
non-zero color and 1 cell is 0, set that 0 to the color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_l,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_l_pattern, all_complete_squares, mixed_color_l.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f4d60fd96dde"
VERSION = "1.1.0"
TASK_ID = "f4d60fd96dde"
SUMMARY = "2-3 L-trominoes (3 cells in 2×2) of distinct colors."

INVARIANTS = [
    "≥2 L-tromino patterns: 3 cells of 1 color in a 2×2 with 4th = 0",
    "no two patterns within distance 2",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_l_pattern", "all_complete_squares", "mixed_color_l")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_l":            {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "separated_l_trominoes",
                       "valid": "separated_l_trominoes"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
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
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 6, 8)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = [2, 3, 4, 5, 6, 7, 8, 9]
    placed = []
    L_variants = [
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (1, 1)],
        [(0, 1), (1, 0), (1, 1)],
    ]
    for _ in range(40):
        if len(placed) >= rng.randint(2, 3): break
        r = rng.randint(0, h - 2); c = rng.randint(0, w - 2)
        if all(abs(r - pr) > 2 or abs(c - pc) > 2 for pr, pc in placed):
            color = rng.choice(palette)
            for dr, dc in rng.choice(L_variants):
                g[r + dr][c + dc] = color
            placed.append((r, c))
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 7
    g = full_grid(h, w, 0)
    if name == "no_l_pattern":
        # blank → no 2×2 windows with 3 same-color cells
        return g
    if name == "all_complete_squares":
        # 2×2 windows fully filled with 1 color → "exactly 3 + 1 zero" precondition fails
        for r, c in [(1, 1), (1, 2), (2, 1), (2, 2)]:
            g[r][c] = 4
        for r, c in [(1, 4), (1, 5), (2, 4), (2, 5)]:
            g[r][c] = 6
        return g
    if name == "mixed_color_l":
        # 2×2 has 3 non-zero cells but they're 3 different colors → no shared color
        g[1][1] = 4; g[1][2] = 6; g[2][1] = 7
        return g
    return g
