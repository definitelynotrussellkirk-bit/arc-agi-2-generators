"""Generator for arc_puzzle_bank_21_set23_s:S23_E7 — flag vertically-symmetric tiles.

Rule: a macro-grid flags which tiles have vertical mirror symmetry.

Combinatorial axes (8): grid_h, grid_w, palette_kind, tile_cols,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_symmetric_tiles, all_symmetric_tiles, no_tiles.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.lattice import assemble_tiles, blank_tile

GENERATOR_ID = "dfc4967f816f"
VERSION = "1.1.0"
TASK_ID = "dfc4967f816f"
SUMMARY = "A macro-grid flags which tiles have vertical mirror symmetry."

INVARIANTS = [
    "divider color is 9",
    "tiles are 3x3",
    "some tiles are vertically symmetric and some are not",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_symmetric_tiles", "all_symmetric_tiles", "no_tiles")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "tile_rows":      {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "tile_cols":      {"type": "int", "default": "rng 3..4", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 6..8", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "lattice_3x3_tiles",
                       "valid": "lattice_3x3_tiles"},
    "n_distinct_colors": {"type": "int", "default": "rng 6..8", "valid": "2..9"},
    "density":        {"type": "str", "default": "dense", "valid": "dense"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _symmetric_tile(rng, color):
    tile = blank_tile(3, 3)
    for r in range(3):
        if rng.random() < 0.65:
            tile[r][0] = color
            tile[r][2] = color
        if rng.random() < 0.45:
            tile[r][1] = color
    return tile


def _asymmetric_tile(rng, color):
    tile = blank_tile(3, 3)
    tile[0][0] = color
    tile[1][2] = color
    if rng.random() < 0.5:
        tile[2][1] = color
    return tile


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        rows = ctx.draw_int("tile_rows", 2, 2)
        cols = ctx.draw_int("tile_cols", 3, 3)
    elif difficulty == "hard":
        rows = ctx.draw_int("tile_rows", 3, 3)
        cols = ctx.draw_int("tile_cols", 4, 4)
    else:
        rows = ctx.draw_int("tile_rows", 2, 3)
        cols = ctx.draw_int("tile_cols", 3, 4)
    rng = ctx.draw_rng("layout")
    tiles = []
    for r in range(rows):
        row = []
        for c in range(cols):
            color = 1 + ((r * cols + c) % 8)
            row.append(_symmetric_tile(rng, color) if rng.random() < 0.5 else _asymmetric_tile(rng, color))
        tiles.append(row)
    return assemble_tiles(tiles)


def _draw_from_degenerate(name, rng):
    import random
    rng = random.Random(0)
    if name == "no_symmetric_tiles":
        # all tiles asymmetric → flag is all-False, no contrast for the rule
        rows, cols = 2, 3
        tiles = [[_asymmetric_tile(rng, 1 + ((r * cols + c) % 8))
                  for c in range(cols)] for r in range(rows)]
        return assemble_tiles(tiles)
    if name == "all_symmetric_tiles":
        # all tiles symmetric → flag is all-True, no contrast
        rows, cols = 2, 3
        tiles = [[_symmetric_tile(rng, 1 + ((r * cols + c) % 8))
                  for c in range(cols)] for r in range(rows)]
        return assemble_tiles(tiles)
    if name == "no_tiles":
        # blank 1x1 lattice → no tiles to classify
        return assemble_tiles([[blank_tile(3, 3)]])
    return assemble_tiles([[blank_tile(3, 3)]])
