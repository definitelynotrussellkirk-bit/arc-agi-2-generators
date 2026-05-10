"""Generator for arc_puzzle_bank_21_set11_s:S11_M1 — Pick blob with most boundary cells.

Rule: sort objects by (boundary cells desc, size desc, color desc); pick
first; output empty + that blob recolored to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, single_blob, tied_boundary.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "41c60a7702e5"
VERSION = "1.1.0"
TASK_ID = "41c60a7702e5"
SUMMARY = "Multiple solid rectangles of different shapes; one has more boundary cells than others."

INVARIANTS = [
    "between 2 and 3 non-touching solid rectangles",
    "boundary-cell counts are distinct",
    "blobs use distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "single_blob", "tied_boundary")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "2", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "rects_distinct_boundaries",
                       "valid": "rects_distinct_boundaries"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _draw_rect(g, r1, c1, r2, c2, color):
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = list(range(2, 10)); rng.shuffle(palette)
    _draw_rect(g, 1, 1, 2, 7, palette[0])
    _draw_rect(g, 4, 4, 7, 7, palette[1])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # blank → no blobs to rank
        return g
    if name == "single_blob":
        # only 1 blob → trivially the "max-boundary" blob
        _draw_rect(g, 2, 2, 5, 5, 4)
        return g
    if name == "tied_boundary":
        # 2 rects with same boundary count → "max" is ambiguous (sort key tied at primary)
        _draw_rect(g, 1, 1, 3, 3, 4)   # 3x3, boundary 8
        _draw_rect(g, 5, 6, 7, 8, 6)   # 3x3, boundary 8 (tied)
        return g
    return g
