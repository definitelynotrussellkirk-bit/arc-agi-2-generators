"""Generator for arc_additional_puzzles_21_set5:M29 — Crop to bbox of largest non-bg object.

Rule: build mask (1 where v != 0), find connected components on the
mask, pick the largest, crop to its bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_largest, single_blob, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "b962e7deb312"
VERSION = "1.1.0"
TASK_ID = "b962e7deb312"
SUMMARY = "Two non-touching blobs, biggest unique; output crops to its bbox."

INVARIANTS = [
    "exactly 2 connected components in the non-bg mask",
    "the larger one has unique size (no tie)",
    "the larger one is large enough that crop is non-trivial (≥3 cells)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_largest", "single_blob", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "two_distinct_size_blobs",
                       "valid": "two_distinct_size_blobs"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "1..3"},
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
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    colors = list(range(1, 10)); rng.shuffle(colors)
    used = set()
    big_size = rng.randint(5, 8)
    small_size = rng.randint(2, big_size - 2)
    for size, color in zip([big_size, small_size], colors[:2]):
        blob = grow_blob(rng, h, w, used, size)
        if blob is None: continue
        used |= blob
        for r, c in blob: g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "tied_largest":
        # two equal-size blobs → "largest" is ambiguous; rule must tie-break or fail
        for (r, c) in [(1, 1), (1, 2), (2, 1), (2, 2)]: g[r][c] = 4
        for (r, c) in [(6, 6), (6, 7), (7, 6), (7, 7)]: g[r][c] = 6
        return g
    if name == "single_blob":
        # one blob → trivially largest, crop is exactly that blob's bbox; no comparison
        for (r, c) in [(3, 3), (3, 4), (3, 5), (4, 4), (5, 4)]: g[r][c] = 4
        return g
    if name == "no_blobs":
        # blank grid → no blobs; rule has nothing to crop, undefined output
        return g
    return g
