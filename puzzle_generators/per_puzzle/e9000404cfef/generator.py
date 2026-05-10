"""Generator for arc_puzzle_bank_21_set23_s:S23_E1.

Rule: a 3x3 tile lattice is summarized by nonzero counts per tile.

Combinatorial axes (8): grid_h, grid_w, palette_kind, tile_rows, tile_cols,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_tiles, all_same_count, single_tile.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.lattice import assemble_tiles, blank_tile

GENERATOR_ID = "e9000404cfef"
VERSION = "1.1.0"
TASK_ID = "e9000404cfef"
SUMMARY = "A 3x3 tile lattice is summarized by nonzero counts per tile."

INVARIANTS = [
    "divider color is 9",
    "all tiles are equal-sized 3x3 grids",
    "each tile has a deterministic nonzero count",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_tiles", "all_same_count", "single_tile")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "tile_rows":      {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "tile_cols":      {"type": "int", "default": "rng 3..4", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "count_lo":       {"type": "int", "default": "1", "valid": "0..9"},
    "palette_size":   {"type": "int", "default": "rng 4..8", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "tile_grid",
                       "valid": "tile_grid"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..8", "valid": "1..9"},
    "density":        {"type": "str", "default": "tiles", "valid": "tiles"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _tile_with_count(rng, count: int, color: int):
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
    palette = [1, 2, 3, 4, 5, 6, 7, 8]
    tiles = []
    for r in range(rows):
        row = []
        for c in range(cols):
            count = rng.randint(1, 7)
            row.append(_tile_with_count(rng, count, palette[(r * cols + c) % len(palette)]))
        tiles.append(row)
    return assemble_tiles(tiles)


def _draw_from_degenerate(name, rng):
    if name == "empty_tiles":
        # all tiles empty → counts all 0, no signal
        tiles = [[blank_tile(3, 3) for _ in range(3)] for _ in range(2)]
        return assemble_tiles(tiles)
    if name == "all_same_count":
        # every tile has count 4 → output is uniform, no per-tile contrast
        rng = __import__("random").Random(0)
        tiles = []
        for r in range(2):
            row = []
            for c in range(3):
                row.append(_tile_with_count(rng, 4, 1 + ((r * 3 + c) % 8)))
            tiles.append(row)
        return assemble_tiles(tiles)
    if name == "single_tile":
        # 1×1 tile lattice → no per-tile comparison
        tile = blank_tile(3, 3)
        tile[1][1] = 4
        return assemble_tiles([[tile]])
    return blank_tile(3, 3)
