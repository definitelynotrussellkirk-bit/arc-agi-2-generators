"""Generator for arc_additional_puzzles_21_set2:E10 — Fill 0 in 2x2 with 3 4-cells using 9.

Rule: for each 2×2 sub-block with exactly 3 cells = 4 and 1 cell = 0,
set that 0 to 9.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_Ls,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_Ls, all_solid_squares, mixed_4_colors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "53ffc8bc9584"
VERSION = "1.1.0"
TASK_ID = "53ffc8bc9584"
SUMMARY = "2-3 L-trominoes of color 4 (3 cells in 2×2 with 4th = 0)."

INVARIANTS = [
    "≥2 L-shaped 4-trominoes (3 cells in 2×2, 4th is 0)",
    "no two patterns within distance 2",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_Ls", "all_solid_squares", "mixed_4_colors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_Ls":           {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "spaced_L_4_trominoes",
                       "valid": "spaced_L_4_trominoes"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
            for dr, dc in rng.choice(L_variants):
                g[r + dr][c + dc] = 4
            placed.append((r, c))
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 7
    g = full_grid(h, w, 0)
    if name == "no_Ls":
        # only solo 4-cells, no 2x2 with 3 cells → rule never fires
        g[1][1] = 4
        g[3][3] = 4
        g[4][5] = 4
        return g
    if name == "all_solid_squares":
        # 2x2 with all 4 cells = 4 → no 0-cell to fill
        for r in range(2):
            for c in range(2): g[1 + r][1 + c] = 4
        for r in range(2):
            for c in range(2): g[3 + r][4 + c] = 4
        return g
    if name == "mixed_4_colors":
        # 2x2 with 3 cells but mixed colors → "all 3 cells = 4" precondition fails
        g[1][1] = 4; g[1][2] = 6; g[2][1] = 4   # mixed
        g[3][3] = 4; g[3][4] = 4; g[4][4] = 3   # mixed
        return g
    return g
