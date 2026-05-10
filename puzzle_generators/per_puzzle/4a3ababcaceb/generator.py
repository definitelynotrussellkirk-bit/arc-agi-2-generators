"""Generator for arc_puzzle_bank_21_set23_s:S23_E4.

The strongest color-2 source motif is copied as 8 into the color-3 target tile.

Combinatorial axes (8): tile_rows, tile_cols, palette_kind, src_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_source, no_target, no_divider.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.lattice import assemble_tiles, blank_tile

GENERATOR_ID = "4a3ababcaceb"
VERSION = "1.1.0"
TASK_ID = "4a3ababcaceb"
SUMMARY = "The strongest color-2 source motif is copied as 8 into the color-3 target tile."

INVARIANTS = [
    "divider color is 9",
    "one tile has the most color-2 cells",
    "exactly one tile contains color 3 as the target marker",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_source", "no_target", "no_divider")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "tile_rows":      {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "tile_cols":      {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "src_size":       {"type": "int", "default": "rng 4..6", "valid": "3..9"},
    "palette_size":   {"type": "int", "default": "rng 5..6", "valid": "4..8"},
    "position_bias":  {"type": "str", "default": "tile_lattice_with_src_target",
                       "valid": "tile_lattice_with_src_target"},
    "n_distinct_colors": {"type": "int", "default": "rng 5..6", "valid": "4..8"},
    "density":        {"type": "str", "default": "dense", "valid": "dense"},
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
    total = rows * cols
    src_idx, tgt_idx = rng.sample(range(total), 2)
    src_cells = rng.sample([(r, c) for r in range(3) for c in range(3)], rng.randint(4, 6))
    tiles = []
    for r in range(rows):
        row = []
        for c in range(cols):
            idx = r * cols + c
            tile = blank_tile(3, 3)
            if idx == src_idx:
                for rr, cc in src_cells:
                    tile[rr][cc] = 2
            elif idx == tgt_idx:
                tile[1][1] = 3
            else:
                for rr, cc in rng.sample([(0, 0), (0, 2), (2, 0), (2, 2)], rng.randint(0, 1)):
                    tile[rr][cc] = rng.choice([4, 5, 6, 7, 8])
            row.append(tile)
        tiles.append(row)
    return assemble_tiles(tiles)


def _draw_from_degenerate(name, rng):
    if name == "no_source":
        # tile lattice with target but no color-2 source motif
        tiles = []
        for r in range(2):
            row = []
            for c in range(3):
                tile = blank_tile(3, 3)
                if r == 0 and c == 1:
                    tile[1][1] = 3
                row.append(tile)
            tiles.append(row)
        return assemble_tiles(tiles)
    if name == "no_target":
        # tile lattice with source but no color-3 target marker
        tiles = []
        for r in range(2):
            row = []
            for c in range(3):
                tile = blank_tile(3, 3)
                if r == 0 and c == 0:
                    for rr, cc in [(0, 0), (1, 1), (2, 2)]:
                        tile[rr][cc] = 2
                row.append(tile)
            tiles.append(row)
        return assemble_tiles(tiles)
    if name == "no_divider":
        # source + target but no color-9 divider lattice → no tile structure
        from puzzle_generators.helpers.grid import full_grid
        g = full_grid(7, 11, 0)
        for r, c in [(0, 0), (1, 1), (2, 2)]:
            g[r][c] = 2
        g[5][8] = 3
        return g
    return blank_tile(3, 3)
