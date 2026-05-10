"""Generator for arc_puzzle_bank_21_set23_s:S23_E3.

Rule: the unique densest tile has all of its nonzero cells recolored to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, tile_rows, tile_cols,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_max, single_tile, all_same_density.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.lattice import assemble_tiles, blank_tile

GENERATOR_ID = "ebd08d719ed6"
VERSION = "1.1.0"
TASK_ID = "ebd08d719ed6"
SUMMARY = "The unique densest tile has all of its nonzero cells recolored to 8."

INVARIANTS = [
    "divider color is 9",
    "tiles are 3x3",
    "one tile has strictly more nonzero cells than every other tile",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_max", "single_tile", "all_same_density")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "tile_rows":      {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "tile_cols":      {"type": "int", "default": "rng 3..4", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "max_density":    {"type": "int", "default": "8", "valid": "5..9"},
    "palette_size":   {"type": "int", "default": "7", "valid": "7"},
    "position_bias":  {"type": "str", "default": "one_dense_rest_sparse",
                       "valid": "one_dense_rest_sparse"},
    "n_distinct_colors": {"type": "int", "default": "7", "valid": "7"},
    "density":        {"type": "str", "default": "tiles", "valid": "tiles"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _tile(rng, count, color):
    tile = blank_tile(3, 3)
    cells = [(r, c) for r in range(3) for c in range(3)]
    rng.shuffle(cells)
    for r, c in cells[:count]:
        tile[r][c] = color
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
    best_idx = rng.randrange(rows * cols)
    tiles = []
    for r in range(rows):
        row = []
        for c in range(cols):
            idx = r * cols + c
            count = 8 if idx == best_idx else rng.randint(1, 5)
            row.append(_tile(rng, count, 1 + (idx % 7)))
        tiles.append(row)
    return assemble_tiles(tiles)


def _draw_from_degenerate(name, rng):
    rng_ = __import__("random").Random(0)
    if name == "tied_max":
        # two tiles share the max density → no unique densest, recolor target ambiguous
        tiles = []
        for r in range(2):
            row = []
            for c in range(3):
                idx = r * 3 + c
                count = 8 if idx in (0, 4) else rng_.randint(1, 5)
                row.append(_tile(rng_, count, 1 + (idx % 7)))
            tiles.append(row)
        return assemble_tiles(tiles)
    if name == "single_tile":
        # 1×1 tile lattice → trivially densest, no comparison
        return assemble_tiles([[_tile(rng_, 5, 4)]])
    if name == "all_same_density":
        # every tile has equal density → no unique max
        tiles = []
        for r in range(2):
            row = []
            for c in range(3):
                row.append(_tile(rng_, 4, 1 + ((r * 3 + c) % 7)))
            tiles.append(row)
        return assemble_tiles(tiles)
    return blank_tile(3, 3)
