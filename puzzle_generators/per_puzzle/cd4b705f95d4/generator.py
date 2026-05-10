"""Generator for arc_puzzle_bank_21_set10_s:S10_H7 — Move 3-blob (size = count of 1s) to 2-anchor.

Rule: target_size = count of 1s in row 0. Find 3-blob with that size in
body. Anchor = first 2-cell. Translate blob's bbox top-left to anchor.
Paint moved cells with 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, k,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_count_row, no_anchor, no_size_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "cd4b705f95d4"
VERSION = "1.1.0"
TASK_ID = "cd4b705f95d4"
SUMMARY = "Row 0 has k 1-cells + 2 3-blobs (one of size k) + 2-anchor."

INVARIANTS = [
    "row 0 has 2-4 1-cells",
    "exactly 2 3-blobs of distinct sizes (one matches k)",
    "exactly one 2-anchor with room for translated blob",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_count_row", "no_anchor", "no_size_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "k":              {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "count_row_plus_two_blobs_plus_anchor",
                       "valid": "count_row_plus_two_blobs_plus_anchor"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 9, 10)
        k = ctx.draw_int("k", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
        k = ctx.draw_int("k", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
        k = ctx.draw_int("k", 2, 3)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    cols = list(range(w)); rng.shuffle(cols)
    for c in cols[:k]:
        g[0][c] = 1
    if k == 2:
        paint_at(g, 2, 1, [(0, 0), (1, 0)], 3)
        paint_at(g, 2, 6, [(0, 0), (1, 0), (1, 1)], 3)
    else:
        paint_at(g, 2, 1, [(0, 0), (1, 0), (1, 1)], 3)
        paint_at(g, 2, 6, [(0, 0), (1, 0)], 3)
    g[5][5] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_count_row":
        # blobs and anchor present but no 1-cells → no target size signal
        paint_at(g, 2, 1, [(0, 0), (1, 0)], 3)
        paint_at(g, 2, 6, [(0, 0), (1, 0), (1, 1)], 3)
        g[5][5] = 2
        return g
    if name == "no_anchor":
        # count + blobs but no 2-anchor → nowhere to translate the matching blob
        for c in [1, 3]: g[0][c] = 1
        paint_at(g, 2, 1, [(0, 0), (1, 0)], 3)
        paint_at(g, 2, 6, [(0, 0), (1, 0), (1, 1)], 3)
        return g
    if name == "no_size_match":
        # neither 3-blob has size k → rule's selection step has no candidate
        for c in [1, 3, 5, 7]: g[0][c] = 1  # k = 4
        paint_at(g, 2, 1, [(0, 0), (1, 0)], 3)
        paint_at(g, 2, 6, [(0, 0), (1, 0), (1, 1)], 3)
        g[5][5] = 2
        return g
    return g
