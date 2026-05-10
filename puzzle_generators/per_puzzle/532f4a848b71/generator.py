"""Generator for arc_puzzle_bank_21_next:hard_c07 — Pick n-th object by reverse-reading-order.

Rule: n = count of 9s in row 0. Sort body objects by (size desc, r1 desc,
c1 desc); pick (n-1)-th; output bbox crop.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_nines,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_nines, no_blobs, equal_sized_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "532f4a848b71"
VERSION = "1.1.0"
TASK_ID = "532f4a848b71"
SUMMARY = "Row 0 has 1-3 9-cells (selecting which body object) + 3 distinct-size body blobs."

INVARIANTS = [
    "row 0 has between 1 and 3 cells of color 9",
    "exactly 3 non-touching body blobs of distinct sizes (so reverse-reading-order pick is unambiguous)",
    "blobs use distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_nines", "no_blobs", "equal_sized_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_nines":        {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "row0_9count_with_3_distinct_blobs",
                       "valid": "row0_9count_with_3_distinct_blobs"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        n_nines = ctx.draw_int("n_nines", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        n_nines = ctx.draw_int("n_nines", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
        n_nines = ctx.draw_int("n_nines", 1, 3)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    cols = list(range(w)); rng.shuffle(cols)
    for c in cols[:n_nines]:
        g[0][c] = 9
    palette = list(range(2, 10)); rng.shuffle(palette)
    if 9 in palette: palette.remove(9)
    motifs = [
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (0, 1)],
    ]
    rng.shuffle(motifs)
    positions = [(2, 1), (2, w - 4), (h - 3, w // 2 - 1)]
    rng.shuffle(positions)
    for (top, left), m, c in zip(positions, motifs, palette[:3]):
        paint_at(g, top, left, m, c)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_nines":
        # body blobs but no 9-count in row 0 → no n to pick by
        for r, c in [(2, 1), (2, 2), (3, 1), (3, 2)]: g[r][c] = 4
        for r, c in [(2, 6), (2, 7), (3, 6)]: g[r][c] = 6
        for r, c in [(6, 4), (6, 5)]: g[r][c] = 7
        return g
    if name == "no_blobs":
        # 9-count but no body blobs → nothing to pick
        g[0][2] = 9; g[0][5] = 9
        return g
    if name == "equal_sized_blobs":
        # all blobs same size → "distinct sizes" precondition fails
        g[0][2] = 9
        for r, c in [(2, 1), (2, 2)]: g[r][c] = 4
        for r, c in [(2, 6), (2, 7)]: g[r][c] = 6
        for r, c in [(6, 4), (6, 5)]: g[r][c] = 7
        return g
    return g
