"""Generator for arc_puzzle_bank_21_set11_s:S11_M3 — Crop blob with N boundary cells.

Rule: n = count of 1s in row 0. Find body blob with exactly n boundary
cells; output bbox-cropped boundary mask in blob's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_ones, texture.
Degenerates: no_ones, no_blobs, all_same_boundary.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "33eb6312ab78"
VERSION = "1.1.0"
TASK_ID = "33eb6312ab78"
SUMMARY = "Row 0 has 4-8 1-cells + 3 distinct-color body blobs with distinct boundary-cell counts."

INVARIANTS = [
    "row 0 has between 4 and 8 1-cells",
    "exactly 3 non-touching body blobs",
    "one body blob has boundary-cell count equal to the number of row-0 1-cells",
    "boundary-cell counts are distinct",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_ones", "no_blobs", "all_same_boundary")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_ones":         {"type": "int", "default": "rng 4..8", "valid": "4..8"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "row0_ones_3_blobs_below",
                       "valid": "row0_ones_3_blobs_below"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


BOUNDARY_SHAPES = {
    4: [(0, 0), (0, 1), (0, 2), (0, 3)],
    5: [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0)],
    6: [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1)],
    7: [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2)],
    8: [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3)],
}



def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 12, 12)
        n_ones = ctx.draw_int("n_ones", 4, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 14, 17)
        n_ones = ctx.draw_int("n_ones", 6, 8)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 12, 14)
        n_ones = ctx.draw_int("n_ones", 4, 8)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    cols = list(range(w)); rng.shuffle(cols)
    for c in cols[:n_ones]:
        g[0][c] = 1
    palette = [c for c in [2, 3, 4, 6, 7, 8, 9]]; rng.shuffle(palette)
    counts = [n_ones] + rng.sample([n for n in BOUNDARY_SHAPES if n != n_ones], 2)
    rng.shuffle(counts)
    slots = [(1, 1), (1, 7), (h - 3, w - 5)]
    for (r, c), boundary_count, color in zip(slots, counts, palette):
        paint_at(g, r, c, BOUNDARY_SHAPES[boundary_count], color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    g = full_grid(h, w, 0)
    if name == "no_ones":
        # Body blobs but row 0 has zero 1-cells — rule's count-of-1s
        # n=0 doesn't match any blob's boundary-cell count.
        paint_at(g, 1, 1, BOUNDARY_SHAPES[4], 3)
        paint_at(g, 4, 6, BOUNDARY_SHAPES[6], 7)
        return g
    if name == "no_blobs":
        # Row 0 has 1-cells but no body blobs below — rule has nothing
        # to crop and emit.
        for c in [1, 3, 5, 7]: g[0][c] = 1
        return g
    if name == "all_same_boundary":
        # Row 0 + body blobs but every blob has the same boundary count
        # — rule's "find blob whose boundary count == n" picks
        # multiple ambiguously.
        for c in [1, 3, 5, 7, 9]: g[0][c] = 1
        paint_at(g, 1, 1, BOUNDARY_SHAPES[5], 3)
        paint_at(g, 4, 6, BOUNDARY_SHAPES[5], 7)
        return g
    return g
