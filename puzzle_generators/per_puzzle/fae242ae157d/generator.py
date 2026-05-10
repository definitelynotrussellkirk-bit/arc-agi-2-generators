"""Generator for arc_puzzle_bank_21_set19_bundle:medium_p01 — area rank recolor (asc, +2).

Rule: sort blobs by ascending area; smallest gets color 2, next 3, etc.
Output keeps blob shapes, only colors change.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, single_blob, tied_sizes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "fae242ae157d"
VERSION = "1.1.0"
TASK_ID = "fae242ae157d"
SUMMARY = "3-4 blobs of strictly distinct sizes; original colors don't all match the rank order."

INVARIANTS = [
    "background is 0",
    "every blob has a strictly distinct size from every other (ranking is unambiguous)",
    "input colors aren't already the area-rank colors (so rule isn't identity)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "single_blob", "tied_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "spaced_distinct_size_blobs",
                       "valid": "spaced_distinct_size_blobs"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..5"},
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
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(3, 4)
    sizes = rng.sample(range(2, 8), n)
    palette = rng.sample([5, 6, 7, 8, 9], n)
    used: set[tuple[int, int]] = set()
    for size, color in zip(sizes, palette):
        cells = grow_blob(rng, h, w, used, size, max_attempts=80)
        if cells is None:
            continue
        for r, c in cells:
            g[r][c] = color
        used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # blank → no blobs to rank
        return g
    if name == "single_blob":
        # only one blob → ranking trivial; rule recolors uniquely with no contrast
        for r, c in [(2, 2), (2, 3), (3, 2)]: g[r][c] = 5
        return g
    if name == "tied_sizes":
        # two blobs same size → ambiguous rank
        g[1][1] = 5; g[1][2] = 5   # size 2
        g[6][7] = 6; g[6][8] = 6   # size 2 (tied)
        for r, c in [(4, 4), (4, 5), (5, 4), (5, 5)]: g[r][c] = 7   # size 4
        return g
    return g
