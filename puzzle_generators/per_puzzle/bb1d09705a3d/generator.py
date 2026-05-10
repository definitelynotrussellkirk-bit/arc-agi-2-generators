"""Generator for arc_additional_puzzle_bank_volume9:M61 — Bar chart of N-objects-per-color.

Rule: build a 3x6 grid where row r has color (r+1) painted in the
first n cells, where n = number of (r+1)-colored connected components
in the input.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n1,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_counts_equal, missing_color, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "bb1d09705a3d"
VERSION = "1.1.0"
TASK_ID = "bb1d09705a3d"
SUMMARY = "Several non-touching blobs of colors 1,2,3; output is 3x6 bar chart of counts."

INVARIANTS = [
    "between 1 and 5 components of color 1, 2, and 3 each",
    "counts are not all equal (so output isn't trivially uniform)",
    "blobs are non-touching",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_counts_equal", "missing_color", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n1":             {"type": "int", "default": "rng 1..5", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "n2":             {"type": "int", "default": "rng 1..5", "valid": "1..6"},
    "n3":             {"type": "int", "default": "rng 1..5", "valid": "1..6"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        n1 = ctx.draw_int("n1", 1, 3)
        n2 = ctx.draw_int("n2", 1, 3)
        n3 = ctx.draw_int("n3", 1, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n1 = ctx.draw_int("n1", 3, 5)
        n2 = ctx.draw_int("n2", 3, 5)
        n3 = ctx.draw_int("n3", 3, 5)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 12)
        n1 = ctx.draw_int("n1", 1, 5)
        n2 = ctx.draw_int("n2", 1, 5)
        n3 = ctx.draw_int("n3", 1, 5)
    if n1 == n2 == n3:
        n3 = (n3 % 5) + 1

    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used = set()
    for color, n in ((1, n1), (2, n2), (3, n3)):
        for _ in range(n):
            size = rng.randint(1, 3)
            blob = grow_blob(rng, h, w, used, size)
            if blob is None: continue
            used |= blob
            for r, c in blob: g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    import random
    rng = random.Random(0)
    h, w = 11, 11
    g = full_grid(h, w, 0)
    used = set()
    if name == "all_counts_equal":
        # all colors have equal counts → output rows have equal length, no contrast in heights
        for color in (1, 2, 3):
            for _ in range(2):
                blob = grow_blob(rng, h, w, used, 2)
                if blob is None: continue
                used |= blob
                for r, c in blob: g[r][c] = color
        return g
    if name == "missing_color":
        # one of the 3 colors is absent → that row's count is 0, ambiguous bar shape
        for color in (1, 3):
            for _ in range(3):
                blob = grow_blob(rng, h, w, used, 2)
                if blob is None: continue
                used |= blob
                for r, c in blob: g[r][c] = color
        return g
    if name == "no_blobs":
        # empty grid → counts are all zero, output is empty/all-zero bar chart
        return g
    return g
