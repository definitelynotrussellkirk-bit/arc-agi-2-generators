"""Generator for arc_puzzle_bank_21_set23_s:S23_E2.

Rule: tiles with nonzero main-diagonal corners receive an 8 center mark.

Combinatorial axes (8): grid_h, grid_w, palette_kind, tile_rows, tile_cols,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_diag_corners, all_diag_corners, single_tile.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.lattice import assemble_tiles, blank_tile

GENERATOR_ID = "bbd8360915fc"
VERSION = "1.1.0"
TASK_ID = "bbd8360915fc"
SUMMARY = "Tiles with nonzero main-diagonal corners receive an 8 center mark."

INVARIANTS = [
    "divider color is 9",
    "tiles are 3x3",
    "some tiles have both top-left and bottom-right corners nonzero",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_diag_corners", "all_diag_corners", "single_tile")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "tile_rows":      {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "tile_cols":      {"type": "int", "default": "rng 3..4", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "diag_prob":      {"type": "float", "default": "0.55", "valid": "0.0..1.0"},
    "palette_size":   {"type": "int", "default": "rng 4..8", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "tile_grid",
                       "valid": "tile_grid"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..8", "valid": "1..9"},
    "density":        {"type": "str", "default": "tiles", "valid": "tiles"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


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
            tile = blank_tile(3, 3)
            color = 1 + ((r * cols + c) % 8)
            if rng.random() < 0.55:
                tile[0][0] = color
                tile[2][2] = color
            else:
                tile[rng.choice([0, 2])][rng.choice([0, 2])] = color
            if rng.random() < 0.4:
                tile[0][2] = rng.choice([2, 3, 4, 5, 6, 7, 8])
            row.append(tile)
        tiles.append(row)
    return assemble_tiles(tiles)


def _draw_from_degenerate(name, rng):
    if name == "no_diag_corners":
        # no tile has main-diagonal corners both set → rule marks nothing
        tiles = []
        for r in range(2):
            row = []
            for c in range(3):
                tile = blank_tile(3, 3)
                color = 1 + ((r * 3 + c) % 8)
                tile[0][2] = color  # only anti-diagonal corner
                row.append(tile)
            tiles.append(row)
        return assemble_tiles(tiles)
    if name == "all_diag_corners":
        # every tile has main-diagonal corners → output marks every tile center (saturated)
        tiles = []
        for r in range(2):
            row = []
            for c in range(3):
                tile = blank_tile(3, 3)
                color = 1 + ((r * 3 + c) % 8)
                tile[0][0] = color
                tile[2][2] = color
                row.append(tile)
            tiles.append(row)
        return assemble_tiles(tiles)
    if name == "single_tile":
        # 1×1 tile grid → no per-tile structure to compare
        tile = blank_tile(3, 3)
        tile[0][0] = 4; tile[2][2] = 4
        return assemble_tiles([[tile]])
    return blank_tile(3, 3)
