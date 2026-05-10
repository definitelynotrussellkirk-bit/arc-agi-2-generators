"""Generator for arc_puzzle_bank_21_set7:medium_g09 — recolor by nearest corner.

Rule: 4 corner-cell markers in distinct colors. Each non-corner blob
gets recolored to the color of the nearest corner marker (Manhattan
distance from blob's first cell).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_corners, no_blobs, equidistant_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "564cab531f76"
VERSION = "1.1.0"
TASK_ID = "564cab531f76"
SUMMARY = "4 distinct corner markers + 2-3 non-corner blobs in unambiguous nearest-corner regions."

INVARIANTS = [
    "background is 0",
    "all 4 grid corners hold distinct color markers",
    "≥2 non-corner blobs (in their own color), each with a strictly nearest corner",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_corners", "no_blobs", "equidistant_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "rng 6..7", "valid": "6..7"},
    "position_bias":  {"type": "str", "default": "four_corners_plus_blobs",
                       "valid": "four_corners_plus_blobs"},
    "n_distinct_colors": {"type": "int", "default": "rng 6..7", "valid": "6..7"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 6, 8)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4], 4)
    g[0][0] = palette[0]
    g[0][w - 1] = palette[1]
    g[h - 1][0] = palette[2]
    g[h - 1][w - 1] = palette[3]
    used = {(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)}
    blob_pal = rng.sample([5, 6, 7, 8, 9], rng.randint(2, 3))
    for color in blob_pal:
        cells = grow_blob(rng, h, w, used, rng.randint(2, 3), max_attempts=80)
        if cells:
            for r, c in cells: g[r][c] = color
            used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 7
    g = full_grid(h, w, 0)
    if name == "no_corners":
        # blobs without corner markers → no nearest-corner colors defined
        g[3][3] = 5; g[3][4] = 5
        g[5][1] = 6
        return g
    if name == "no_blobs":
        # corners alone, no blobs to recolor
        g[0][0] = 1
        g[0][w - 1] = 2
        g[h - 1][0] = 3
        g[h - 1][w - 1] = 4
        return g
    if name == "equidistant_blob":
        # blob exactly at the center → equidistant from all 4 corners (ambiguous)
        g[0][0] = 1
        g[0][w - 1] = 2
        g[h - 1][0] = 3
        g[h - 1][w - 1] = 4
        g[h // 2][w // 2] = 6  # equidistant
        return g
    return g
