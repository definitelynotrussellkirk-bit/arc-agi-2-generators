"""Generator for arc_puzzle_bank_21_more:easy_b07 — Fill 0 between matching pair.

Rule: 0-cell with same non-zero value horizontally adjacent on both
sides (or vertically) → fill with that value. Horizontal precedence.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_triplets,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_triplets, gap_too_wide, no_distractor.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bf1bc9d143b8"
VERSION = "1.1.0"
TASK_ID = "bf1bc9d143b8"
SUMMARY = "2-3 horizontal/vertical (a,0,a) triplets in distinct rows/cols."

INVARIANTS = [
    "≥1 horizontal (a,0,a) triplet for some non-bg a",
    "1-2 distractor isolated cells (no matching neighbor)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_triplets", "gap_too_wide", "no_distractor")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_triplets":     {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "row_triplets_plus_distractor",
                       "valid": "row_triplets_plus_distractor"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..6"},
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
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 7, 9)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used_rows = set()
    palette = [2, 3, 4, 5, 6, 7, 8, 9]
    for _ in range(rng.randint(2, 3)):
        for _ in range(20):
            r = rng.randint(0, h - 1)
            if r in used_rows: continue
            c = rng.randint(0, w - 3)
            color = rng.choice(palette)
            g[r][c] = color; g[r][c + 2] = color
            used_rows.add(r)
            break
    for _ in range(20):
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] == 0:
            g[r][c] = rng.choice(palette)
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_triplets":
        # only distractor singletons → no (a,0,a) patterns to fill
        g[1][2] = 4
        g[3][5] = 6
        return g
    if name == "gap_too_wide":
        # pair separated by 2+ zeros → not adjacent triplets, rule doesn't fire
        g[2][1] = 4
        g[2][5] = 4  # gap of 3 zeros, not 1
        return g
    if name == "no_distractor":
        # only triplets without distractor → no contrast for "isolated" cells
        g[1][1] = 4; g[1][3] = 4
        g[3][2] = 6; g[3][4] = 6
        return g
    return g
