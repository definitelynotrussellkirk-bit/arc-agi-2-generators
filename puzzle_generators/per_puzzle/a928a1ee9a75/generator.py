"""Generator for arc_puzzle_bank_21_set16_s:S16_M6 — fill band between parallel pairs.

Rule: two color-pairs (e.g. two 2s on row r1, two 3s on row r2 sharing
the SAME columns) define horizontal bars. Output fills the rectangular
band between them with 8s.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: misaligned_columns, single_pair, adjacent_rows.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a928a1ee9a75"
VERSION = "1.1.0"
TASK_ID = "a928a1ee9a75"
SUMMARY = "Two color-pairs on different rows sharing columns (parallel bars)."

INVARIANTS = [
    "background is 0",
    "exactly two distinct non-zero colors, each appearing exactly twice",
    "the two pairs share the same column pair (so the band is rectangular)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("misaligned_columns", "single_pair", "adjacent_rows")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "2", "valid": "2..2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "two_aligned_color_pairs",
                       "valid": "two_aligned_color_pairs"},
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
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 2)
    r1 = rng.randint(1, h - 5)
    r2 = rng.randint(r1 + 3, h - 2)
    c1 = rng.randint(1, w - 5)
    c2 = rng.randint(c1 + 3, w - 2)
    g[r1][c1] = palette[0]
    g[r1][c2] = palette[0]
    g[r2][c1] = palette[1]
    g[r2][c2] = palette[1]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "misaligned_columns":
        # two pairs on different columns → no rectangular band defined
        g[1][1] = 4; g[1][5] = 4
        g[5][2] = 6; g[5][7] = 6   # different cols
        return g
    if name == "single_pair":
        # only 1 pair → can't form a band (need 2 parallel bars)
        g[1][2] = 4; g[1][6] = 4
        return g
    if name == "adjacent_rows":
        # pairs on adjacent rows → no interior cells in the band
        g[3][2] = 4; g[3][6] = 4
        g[4][2] = 6; g[4][6] = 6
        return g
    return g
