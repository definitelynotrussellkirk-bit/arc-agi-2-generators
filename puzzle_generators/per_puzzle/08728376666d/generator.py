"""Generator for arc_additional_puzzles_21_set5:H31 — Output color row sorted by frequency.

Rule: get all distinct non-bg colors. Sort by (count desc, color asc).
Output is single row of these colors in that order.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_counts, single_color, no_colors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "08728376666d"
VERSION = "1.1.0"
TASK_ID = "08728376666d"
SUMMARY = "Several non-touching colored blobs with distinct counts; output is colors sorted by count desc."

INVARIANTS = [
    "between 3 and 4 distinct non-bg colors",
    "all distinct counts (so order is unambiguous)",
    "blobs are non-touching",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_counts", "single_color", "no_colors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "blobs_distinct_counts",
                       "valid": "blobs_distinct_counts"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        n_colors = ctx.draw_int("n_colors", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
        n_colors = ctx.draw_int("n_colors", 4, 4)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 14)
        n_colors = ctx.draw_int("n_colors", 3, 4)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = list(range(1, 10)); rng.shuffle(palette)
    palette = palette[:n_colors]
    counts = list(range(2, 2 + n_colors + 3)); rng.shuffle(counts)
    counts = counts[:n_colors]
    used = set()
    for color, total in zip(palette, counts):
        rem = total
        while rem > 0:
            bs = min(rem, rng.randint(1, 3))
            blob = grow_blob(rng, h, w, used, bs)
            if blob is None: rem = 0; break
            used |= blob
            for r, c in blob: g[r][c] = color
            rem -= len(blob)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "tied_counts":
        # all colors share same count → secondary sort key (color asc) is the only signal
        for (r, c) in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 4
        for (r, c) in [(1, 5), (1, 6), (2, 5)]: g[r][c] = 6
        for (r, c) in [(5, 2), (5, 3), (6, 2)]: g[r][c] = 3
        return g
    if name == "single_color":
        # only one color → output is single-cell, weakly tests sorting
        for (r, c) in [(1, 1), (1, 2), (2, 1), (3, 5), (5, 7)]: g[r][c] = 4
        return g
    if name == "no_colors":
        # blank → no colors to sort, output undefined
        return g
    return g
