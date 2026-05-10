"""Generator for arc_puzzle_bank_21_set23_s:S23_E5.

Rule: each tile's majority nonzero color becomes one macro-grid cell.

Combinatorial axes (8): grid_h, grid_w, palette_kind, tile_rows, tile_cols,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_majority, single_color_tiles, empty_tiles.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.lattice import assemble_tiles, blank_tile

GENERATOR_ID = "15949bcd466a"
VERSION = "1.1.0"
TASK_ID = "15949bcd466a"
SUMMARY = "Each tile's majority nonzero color becomes one macro-grid cell."

INVARIANTS = [
    "divider color is 9",
    "tiles are 3x3",
    "each tile has a strict nonzero-color majority",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_majority", "single_color_tiles", "empty_tiles")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "tile_rows":      {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "tile_cols":      {"type": "int", "default": "rng 3..4", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "majority_count": {"type": "int", "default": "5", "valid": "5..9"},
    "palette_size":   {"type": "int", "default": "8", "valid": "8"},
    "position_bias":  {"type": "str", "default": "tile_grid_majority",
                       "valid": "tile_grid_majority"},
    "n_distinct_colors": {"type": "int", "default": "8", "valid": "8"},
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
    cells = [(r, c) for r in range(3) for c in range(3)]
    tiles = []
    for r in range(rows):
        row = []
        for c in range(cols):
            tile = blank_tile(3, 3)
            main = 1 + ((r * cols + c) % 8)
            other = rng.choice([x for x in range(1, 9) if x != main])
            chosen = cells[:]
            rng.shuffle(chosen)
            for rr, cc in chosen[:5]:
                tile[rr][cc] = main
            for rr, cc in chosen[5:7]:
                tile[rr][cc] = other
            row.append(tile)
        tiles.append(row)
    return assemble_tiles(tiles)


def _draw_from_degenerate(name, rng):
    rng_ = __import__("random").Random(0)
    if name == "no_majority":
        # each tile has equal counts of two colors → no majority, rule undefined
        cells = [(r, c) for r in range(3) for c in range(3)]
        tiles = []
        for r in range(2):
            row = []
            for c in range(3):
                tile = blank_tile(3, 3)
                chosen = cells[:]
                rng_.shuffle(chosen)
                for i, (rr, cc) in enumerate(chosen[:8]):
                    tile[rr][cc] = (1 + ((r * 3 + c) % 8)) if i < 4 else (1 + ((r * 3 + c + 1) % 8))
                row.append(tile)
            tiles.append(row)
        return assemble_tiles(tiles)
    if name == "single_color_tiles":
        # all tiles uniformly the same color → macro grid is monochrome, no contrast
        tiles = []
        for r in range(2):
            row = []
            for c in range(3):
                tile = blank_tile(3, 3)
                for rr in range(3):
                    for cc in range(3): tile[rr][cc] = 4
                row.append(tile)
            tiles.append(row)
        return assemble_tiles(tiles)
    if name == "empty_tiles":
        # all tiles empty → no nonzero majority anywhere
        tiles = [[blank_tile(3, 3) for _ in range(3)] for _ in range(2)]
        return assemble_tiles(tiles)
    return blank_tile(3, 3)
