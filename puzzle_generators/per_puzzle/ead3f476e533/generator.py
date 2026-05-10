"""Generator for arc_puzzle_bank_21_next:medium_c04 — Keep only even-sized objects.

Rule: for each object, keep its cells (in their color) only if obj-size is
even, else drop them.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_even, all_odd, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "ead3f476e533"
VERSION = "1.1.0"
TASK_ID = "ead3f476e533"
SUMMARY = "Several non-touching colored blobs of mixed-parity sizes; output keeps only even-sized."

INVARIANTS = [
    "between 3 and 5 non-touching blobs",
    "at least one odd-sized AND one even-sized (so output != input)",
    "blobs use distinct non-bg colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_even", "all_odd", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..6"},
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
        n_blobs = ctx.draw_int("n_blobs", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        n_blobs = ctx.draw_int("n_blobs", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        n_blobs = ctx.draw_int("n_blobs", 3, 5)

    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    sizes = [1, 2, 3, 4, 5]
    rng.shuffle(sizes)
    sizes = sizes[:n_blobs]
    if all(s % 2 == 0 for s in sizes): sizes[0] = 3
    if all(s % 2 == 1 for s in sizes): sizes[0] = 4
    colors = list(range(1, 10)); rng.shuffle(colors)
    used = set()
    for i, size in enumerate(sizes):
        blob = grow_blob(rng, h, w, used, size)
        if blob is None: continue
        used |= blob
        for r, c in blob: g[r][c] = colors[i % len(colors)]
    return g


def _draw_from_degenerate(name, rng):
    import random
    rng = random.Random(0)
    h, w = 9, 9
    g = full_grid(h, w, 0)
    used = set()
    if name == "all_even":
        # all blobs even → rule keeps everything, identity output (no contrast)
        for size, color in [(2, 4), (4, 5), (2, 6)]:
            blob = grow_blob(rng, h, w, used, size)
            if blob is None: continue
            used |= blob
            for r, c in blob: g[r][c] = color
        return g
    if name == "all_odd":
        # all blobs odd → rule erases everything, output all-zero (no contrast either way)
        for size, color in [(1, 4), (3, 5), (5, 6)]:
            blob = grow_blob(rng, h, w, used, size)
            if blob is None: continue
            used |= blob
            for r, c in blob: g[r][c] = color
        return g
    if name == "no_blobs":
        # empty grid → rule no-op
        return g
    return g
