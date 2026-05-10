"""Generator for arc_puzzle_bank_21_set11_s:S11_H3 — Find blob with k holes; output its bbox-cropped boundary mask.

Rule: k = count of 1s in row 0. Find first body blob with k holes; output
its boundary cells' bbox crop in color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_ones,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_ones, all_solid, all_same_holes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import RING_3X3

GENERATOR_ID = "4dd0b3ed33ee"
VERSION = "1.1.0"
TASK_ID = "4dd0b3ed33ee"
SUMMARY = "Row 0 has 1-3 1-cells + body has shapes with varied hole counts."

INVARIANTS = [
    "row 0 has between 1 and 3 cells of color 1",
    "body has 3 blobs of distinct hole counts (0, 1, 2)",
    "blobs use distinct non-1 colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_ones", "all_solid", "all_same_holes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..7", "valid": "5..10"},
    "grid_w":         {"type": "int", "default": "rng 14..16", "valid": "12..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_ones":         {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "row0_count_then_blobs",
                       "valid": "row0_count_then_blobs"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "3..5"},
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
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 14, 15)
        n_ones = ctx.draw_int("n_ones", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 15, 17)
        n_ones = ctx.draw_int("n_ones", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 14, 16)
        n_ones = ctx.draw_int("n_ones", 1, 3)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    cols = list(range(w)); rng.shuffle(cols)
    for c in cols[:n_ones]:
        g[0][c] = 1
    palette = [c for c in [2, 3, 4, 6, 7, 8, 9] if c != 1]; rng.shuffle(palette)
    # Solid 2x2 (0 holes)
    paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0), (1, 1)], palette[0])
    # Hollow 3x3 (1 hole)
    paint_at(g, 1, 5, RING_3X3, palette[1])
    # Figure-8 (2 holes)
    paint_at(g, 1, 10, [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                    (1, 0), (1, 4),
                    (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
                    (3, 0), (3, 4),
                    (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)] if h > 5 else
                    RING_3X3, palette[2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 15
    g = full_grid(h, w, 0)
    if name == "no_ones":
        # Row 0 has no 1s — k = 0 ambiguous (no count to interpret).
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0), (1, 1)], 2)
        paint_at(g, 1, 5, RING_3X3, 3)
        return g
    if name == "all_solid":
        # All blobs are solid (0 holes) — rule cannot pick by hole count k>0.
        g[0][3] = 1; g[0][7] = 1
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0), (1, 1)], 2)
        paint_at(g, 1, 5, [(0, 0), (0, 1), (1, 0), (1, 1)], 3)
        paint_at(g, 1, 10, [(0, 0), (0, 1), (1, 0), (1, 1)], 4)
        return g
    if name == "all_same_holes":
        # All blobs have exactly 1 hole — multiple ambiguous matches for k=1.
        g[0][3] = 1
        paint_at(g, 1, 1, RING_3X3, 2)
        paint_at(g, 1, 5, RING_3X3, 3)
        paint_at(g, 1, 10, RING_3X3, 4)
        return g
    return g
