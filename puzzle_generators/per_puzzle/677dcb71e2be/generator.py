"""Generator for arc_additional_puzzles_21_set3:H19 — Pack objects sorted by size desc into single row.

Rule: sort objects by (size desc, color asc); concat each as size-many
copies of color, separated by 1 zero. Output single row.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, single_blob, tied_sizes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "677dcb71e2be"
VERSION = "1.1.0"
TASK_ID = "677dcb71e2be"
SUMMARY = "3 distinct-color blobs of distinct sizes."

INVARIANTS = [
    "exactly 3 non-touching blobs of distinct sizes",
    "blobs use distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "single_blob", "tied_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "9..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "distinct_size_blobs",
                       "valid": "distinct_size_blobs"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..4"},
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
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = [2, 3, 4, 6, 7, 8, 9]; rng.shuffle(palette)
    sizes = rng.sample([2, 3, 4, 5, 6], 3)
    positions = [(1, 1), (3, w - 5), (h - 4, 1)]
    rng.shuffle(positions)
    for (top, left), sz, col in zip(positions, sizes, palette[:3]):
        cells = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)][:sz]
        for dr, dc in cells:
            r, c = top + dr, left + dc
            if 0 <= r < h and 0 <= c < w:
                g[r][c] = col
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # blank → no objects to pack
        return g
    if name == "single_blob":
        # only 1 blob → packed output is just that blob
        paint_at(g, 3, 3, [(0, 0), (0, 1), (1, 0)], 4)
        return g
    if name == "tied_sizes":
        # 3 blobs same size → sort key tied (sort-by-color tiebreak only)
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0)], 4)
        paint_at(g, 1, 6, [(0, 0), (0, 1), (1, 0)], 6)
        paint_at(g, 6, 3, [(0, 0), (0, 1), (1, 0)], 3)
        return g
    return g
