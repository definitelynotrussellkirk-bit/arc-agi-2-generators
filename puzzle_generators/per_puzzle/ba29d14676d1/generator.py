"""Generator for arc_puzzle_bank_21_set23_s:S23_E6.

Rule: every tile in the lattice is mirrored horizontally in place.

Combinatorial axes (8): tile_rows, tile_cols, palette_kind, palette_size,
position_bias, n_distinct_colors, tile_density, texture.
Degenerates: empty_tiles, lr_symmetric_tiles, no_tiles.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.lattice import assemble_tiles, blank_tile

GENERATOR_ID = "ba29d14676d1"
VERSION = "1.1.0"
TASK_ID = "ba29d14676d1"
SUMMARY = "Every tile in the lattice is mirrored horizontally in place."

INVARIANTS = [
    "divider color is 9",
    "tiles are equal-sized 3x3 grids",
    "tile contents are arbitrary sparse colors",
]

PALETTE_KINDS = ("default", "sparse", "dense", "varied_palette")
DEGENERATE_TEXTURES = ("empty_tiles", "lr_symmetric_tiles", "no_tiles")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "tile_rows":      {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "tile_cols":      {"type": "int", "default": "rng 3..4", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "tile", "valid": "tile"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6", "valid": "1..8"},
    "tile_density":   {"type": "str", "default": "mixed", "valid": "mixed"},
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
        rows = ctx.draw_int("tile_rows", 2, 2)
        cols = ctx.draw_int("tile_cols", 3, 3)
    elif difficulty == "hard":
        rows = ctx.draw_int("tile_rows", 3, 3)
        cols = ctx.draw_int("tile_cols", 4, 4)
    else:
        rows = ctx.draw_int("tile_rows", 2, 3)
        cols = ctx.draw_int("tile_cols", 3, 4)
    rng = ctx.draw_rng("layout")
    cells = [(r, c) for r in range(3) for c in range(3)]
    tiles = []
    for r in range(rows):
        row = []
        for c in range(cols):
            tile = blank_tile(3, 3)
            for rr, cc in rng.sample(cells, rng.randint(2, 5)):
                tile[rr][cc] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
            row.append(tile)
        tiles.append(row)
    return assemble_tiles(tiles)


def _draw_from_degenerate(name, rng):
    if name == "empty_tiles":
        # all-blank tiles — flip is identity (no visible effect)
        tiles = [[blank_tile(3, 3) for _ in range(3)] for _ in range(2)]
        return assemble_tiles(tiles)
    if name == "lr_symmetric_tiles":
        # already-LR-symmetric tiles → mirror is identity
        tiles = []
        for _ in range(2):
            row = []
            for _ in range(3):
                t = blank_tile(3, 3)
                t[0][0] = 4; t[0][2] = 4
                t[1][1] = 6
                t[2][0] = 5; t[2][2] = 5
                row.append(t)
            tiles.append(row)
        return assemble_tiles(tiles)
    if name == "no_tiles":
        # 1x1 lattice — single tile, mirror still applies but minimal
        return assemble_tiles([[blank_tile(3, 3)]])
    return assemble_tiles([[blank_tile(3, 3)]])
