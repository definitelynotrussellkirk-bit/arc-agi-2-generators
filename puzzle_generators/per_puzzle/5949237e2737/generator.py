"""Generator for arc_puzzle_bank_21_set8_s:S8_H5.

A vertical color-8 fold bar divides the grid. Only left-side cells whose
mirrored right-side cell has the same color survive in the output.

Combinatorial axes (8): grid_h, half_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_bar, no_pairs, all_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5949237e2737"
VERSION = "1.1.0"
TASK_ID = "5949237e2737"
SUMMARY = "Mirror the left side across a vertical 8-bar and keep color agreements."

INVARIANTS = [
    "there is one full vertical separator bar of color 8",
    "nonzero evidence appears on both sides of the bar",
    "at least one mirrored left/right pair has matching color",
    "at least one mirrored pair is a mismatch or missing on the right",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_bar", "no_pairs", "all_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "half_w":         {"type": "int", "default": "rng 3..5", "valid": "2..7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 5..9", "valid": "2..20"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "fold_about_8bar",
                       "valid": "fold_about_8bar"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "2..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        half = ctx.draw_int("half_w", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        half = ctx.draw_int("half_w", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        half = ctx.draw_int("half_w", 3, 5)
    n_pairs = ctx.draw_int("n_pairs", 5, min(9, h * half))
    colors = [1, 2, 3, 4, 5, 6, 7, 9]

    g = full_grid(h, 2 * half + 1, 0)
    for r in range(h):
        g[r][half] = 8

    left_positions = [(r, c) for r in range(h) for c in range(half)]
    rng.shuffle(left_positions)
    match_count = max(1, n_pairs // 2)
    for idx, (r, c) in enumerate(left_positions[:n_pairs]):
        color = rng.choice(colors)
        mirror_c = half + (half - c)
        g[r][c] = color
        if idx < match_count:
            g[r][mirror_c] = color
        elif idx % 2 == 0:
            alternatives = [v for v in colors if v != color]
            g[r][mirror_c] = rng.choice(alternatives)
    return g


def _draw_from_degenerate(name, rng):
    h, half = 8, 4
    w = 2 * half + 1
    g = full_grid(h, w, 0)
    if name == "no_bar":
        # No 8-bar — fold axis is undefined.
        g[1][1] = 4; g[1][7] = 4
        g[3][2] = 5; g[3][6] = 5
        return g
    if name == "no_pairs":
        # 8-bar but cells only on one side — no pairs to compare.
        for r in range(h):
            g[r][half] = 8
        g[1][1] = 4; g[2][2] = 5; g[3][1] = 6
        return g
    if name == "all_match":
        # 8-bar with every pair matching — rule keeps everything (no contrast).
        for r in range(h):
            g[r][half] = 8
        for (r, c, color) in [(1, 1, 4), (2, 2, 5), (3, 1, 6), (4, 3, 7)]:
            g[r][c] = color
            g[r][half + (half - c)] = color
        return g
    return g
