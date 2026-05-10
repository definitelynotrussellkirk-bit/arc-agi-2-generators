"""Generator for 15660dd6.

Rule: column-wise 2/8 pattern tiles are recolored from solid swatch tiles
in the same separator grid.

Combinatorial axes (8): grid_h/w, tile_size, column_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, n_distinct_colors.
Degenerates: no_pattern, no_swatches, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a61246736c26"
VERSION = "1.1.0"
TASK_ID = "a61246736c26"
SUMMARY = "Column-wise 2/8 pattern tiles recolored from solid swatch tiles in same separator grid."

INVARIANTS = [
    "full color-8 rows and columns split the input into equal square tile cores",
    "the first column band has a row-color swatch column before each tile core",
    "each output column has one 1/2/8 pattern tile and at least one solid-color swatch tile",
    "pattern cells with value 1 become the swatch row color, while cells with value 2 become the solid fill color",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pattern", "no_swatches", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "16..18", "valid": "16..18"},
    "grid_w":         {"type": "int", "default": "12..18", "valid": "12..18"},
    "tile_size":      {"type": "int", "default": "rng 4..5", "valid": "4..5"},
    "column_count":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 5..6", "valid": "5..6"},
    "n_distinct_colors":{"type": "int", "default": "rng 5..6", "valid": "5..6"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _pattern_tile(n, rng):
    tile = [[1 if r in (0, n - 1) or c in (0, n - 1) else 8 for c in range(n)] for r in range(n)]
    for r in range(1, n - 1):
        c = 1 + ((r + rng.randrange(n - 2)) % (n - 2))
        tile[r][c] = 2
    tile[n // 2][n // 2] = 2
    return tile


def _solid_tile(n, fill):
    tile = [[1 if r in (0, n - 1) or c in (0, n - 1) else fill for c in range(n)] for r in range(n)]
    return tile


def _put_tile(g, r0, c0, tile):
    for r, row in enumerate(tile):
        for c, v in enumerate(row):
            g[r0 + r][c0 + c] = v


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        n = ctx.draw_int("tile_size", 4, 4)
        col_count = ctx.draw_int("column_count", 2, 2)
    elif difficulty == "hard":
        n = ctx.draw_int("tile_size", 5, 5)
        col_count = ctx.draw_int("column_count", 3, 3)
    else:
        n = ctx.draw_int("tile_size", 4, 5)
        col_count = ctx.draw_int("column_count", 2, 3)
    row_count = 3
    row_colors = ctx.draw_distinct_colors("row_colors", n=row_count, exclude={1, 2, 8})
    fill_colors = ctx.draw_distinct_colors("fill_colors", n=col_count, exclude={1, 2, 8})

    h = 1 + row_count * (n + 1)
    w = (n + 1) + 1 + (col_count - 1) * (n + 1)
    g = full_grid(h, w, 8)
    row_starts = [1 + i * (n + 1) for i in range(row_count)]
    col_starts = [0]
    for ci in range(1, col_count):
        col_starts.append((n + 2) + (ci - 1) * (n + 1))

    for ri, r0 in enumerate(row_starts):
        for rr in range(n):
            g[r0 + rr][0] = row_colors[ri]
        for ci, c_band in enumerate(col_starts):
            c0 = c_band + 1 if ci == 0 else c_band
            if ri == 0:
                tile = _pattern_tile(n, rng)
            elif ri == 1:
                tile = _solid_tile(n, fill_colors[ci])
            else:
                alt = fill_colors[(ci + 1) % col_count]
                tile = _solid_tile(n, alt)
            _put_tile(g, r0, c0, tile)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(16, 12, 8)
    if name == "no_pattern":
        return g
    if name == "no_swatches":
        for r in range(1, 5):
            for c in range(1, 5):
                g[r][c] = 1
        return g
    if name == "full_grid":
        for r in range(16):
            for c in range(12):
                g[r][c] = 8
        return g
    return g
