"""Generator for arc_additional_puzzle_bank_volume18:E125.

Each color's aligned marker pair is filled into a same-color segment.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, single_cell, adjacent_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ffb7c0bc9376"
VERSION = "1.1.0"
TASK_ID = "ffb7c0bc9376"
SUMMARY = "Each color's aligned marker pair is filled into a same-color segment."

INVARIANTS = [
    "background is 0",
    "each active nonzero color appears exactly twice",
    "paired markers share a row with empty cells between",
    "pairs use distinct rows and columns to avoid accidental extra pairs",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_cell", "adjacent_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "row_aligned_pairs",
                       "valid": "row_aligned_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..5", "valid": "1..8"},
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
        w = ctx.draw_int("grid_w", 8, 9)
        n_pairs = ctx.draw_int("n_pairs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
        n_pairs = ctx.draw_int("n_pairs", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
        n_pairs = ctx.draw_int("n_pairs", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    colors = list(range(1, 10))
    rng.shuffle(colors)
    rows = rng.sample(range(h), min(n_pairs, h, len(colors)))
    used_cols: set[int] = set()
    placed = 0
    for color, r in zip(colors, rows):
        candidates = [c for c in range(w) if c not in used_cols]
        if len(candidates) < 2:
            break
        c1, c2 = sorted(rng.sample(candidates, 2))
        if c2 - c1 < 2:
            continue
        g[r][c1] = color
        g[r][c2] = color
        used_cols.update((c1, c2))
        placed += 1
    if placed == 0:
        g[1][1] = 2
        g[1][4] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # blank → no pairs to fill
        return g
    if name == "single_cell":
        # only one cell of each color → "exactly twice" precondition fails
        g[2][3] = 4
        g[5][6] = 6
        return g
    if name == "adjacent_pair":
        # pair adjacent (distance 1) → no empty cells between, segment is degenerate
        g[3][4] = 4; g[3][5] = 4
        return g
    return g
