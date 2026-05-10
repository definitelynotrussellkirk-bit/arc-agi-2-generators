"""Generator for arc_puzzle_bank_21_set9_s:S9_M5 — pick object matching top count.

Rule: count of 1s in row 0 = K. Find the (only) non-row-0 blob of
size K, paint it in 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, K,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_count_row, no_size_match, multiple_size_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "017f1406edaf"
VERSION = "1.1.0"
TASK_ID = "017f1406edaf"
SUMMARY = "Row 0 has K 1-cells (K=3..5) + 3 distinct-size blobs below, one of size K."

INVARIANTS = [
    "background is 0",
    "row 0 contains K 1-cells where K ∈ 3..5",
    "below row 0: 3 blobs at distinct sizes, exactly one of size K",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_count_row", "no_size_match", "multiple_size_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "K":              {"type": "int", "default": "rng 3..5", "valid": "3..5"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "count_plus_three_blobs",
                       "valid": "count_plus_three_blobs"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
    K = rng.randint(3, 5)
    cols = rng.sample(range(w), K)
    for c in cols:
        g[0][c] = 1
    used = {(0, c) for c in cols}
    for c in range(w):
        used.add((1, c))
    other_sizes = [s for s in [2, 3, 4, 5, 6] if s != K][:2]
    sizes = [K] + other_sizes
    palette = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 3)
    for size, color in zip(sizes, palette):
        cells = grow_blob(rng, h, w, used, size, max_attempts=80)
        if cells is None:
            continue
        for r, c in cells:
            g[r][c] = color
        used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_count_row":
        # blobs without row-0 count → no K to select with
        for r, c in [(2, 1), (2, 2)]: g[r][c] = 4
        for r, c in [(4, 5), (5, 5), (5, 6)]: g[r][c] = 6
        return g
    if name == "no_size_match":
        # K=4 in row 0, but no blob has size 4
        for c in [1, 3, 5, 7]: g[0][c] = 1  # K=4
        for r, c in [(2, 1), (2, 2)]: g[r][c] = 4  # size 2
        for r, c in [(4, 5), (5, 5), (5, 6)]: g[r][c] = 6  # size 3
        return g
    if name == "multiple_size_match":
        # 2 blobs share size K → ambiguous winner
        for c in [1, 3, 5]: g[0][c] = 1  # K=3
        for r, c in [(2, 1), (2, 2), (3, 1)]: g[r][c] = 4  # size 3
        for r, c in [(4, 5), (4, 6), (5, 5)]: g[r][c] = 6  # size 3
        return g
    return g
