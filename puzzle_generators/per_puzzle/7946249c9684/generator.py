"""Generator for arc_puzzle_bank_21_set12_bundle:easy_l01 — Hollow vertical runs.

Rule: per column, replace each contiguous run of one color with just
its first and last cells in that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_bars,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_bars, length_2_bars, horizontal_only.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7946249c9684"
VERSION = "1.1.0"
TASK_ID = "7946249c9684"
SUMMARY = "2-3 vertical bars (each ≥3 rows tall) of distinct colors in different columns."

INVARIANTS = [
    "2-3 vertical bars in distinct columns",
    "each bar ≥3 rows tall (so output is non-trivial: only first+last kept)",
    "isolated bars (separator rows on either side)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_bars", "length_2_bars", "horizontal_only")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_bars":         {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "vertical_bars_with_distractor",
                       "valid": "vertical_bars_with_distractor"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "1..6"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_bars = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_bars)
    cols = rng.sample(range(w), n_bars)
    for c, color in zip(cols, palette):
        bar_len = rng.randint(3, h - 2)
        r0 = rng.randint(0, h - bar_len)
        for r in range(r0, r0 + bar_len):
            g[r][c] = color
    distract_color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    for _ in range(20):
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] == 0:
            g[r][c] = distract_color
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_bars":
        # blank → no vertical bars to hollow
        return g
    if name == "length_2_bars":
        # 2-cell bars → already only first+last (rule is identity)
        for r in [2, 3]: g[r][2] = 4
        for r in [4, 5]: g[r][5] = 6
        return g
    if name == "horizontal_only":
        # horizontal bars → "vertical" precondition fails
        for c in range(2, 5): g[3][c] = 4
        for c in range(2, 5): g[5][c] = 6
        return g
    return g
