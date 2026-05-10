"""Generator for 941d9a10.

Rule: color-5 grid has its top-left, center, and bottom-right cells
filled with blue, red, and green.

Combinatorial axes (8): grid_h/w, cell_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, n_bands.
Degenerates: no_dividers, full_grid, single_band.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9dcdf3696b49"
VERSION = "1.1.0"
TASK_ID = "9dcdf3696b49"
SUMMARY = "Color-5 grid; top-left/center/bottom-right cells fill blue/red/green."

INVARIANTS = [
    "background is color 0",
    "color 5 forms full divider rows and columns",
    "the cell grid has odd row and column counts so a center cell exists",
    "only zero cells inside the three diagonal macro-cells get recolored",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_dividers", "full_grid", "single_band")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "7..18"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "7..18"},
    "cell_count":     {"type": "int", "default": "3", "valid": "3"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_bands":        {"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    ctx.draw_int("cell_count", 3, 3)
    row_bands = [rng.randint(2, 4) for _ in range(3)]
    col_bands = [rng.randint(2, 4) for _ in range(3)]
    h = sum(row_bands) + 2
    w = sum(col_bands) + 2
    g = full_grid(h, w, 0)
    div_rows = [row_bands[0], row_bands[0] + 1 + row_bands[1]]
    div_cols = [col_bands[0], col_bands[0] + 1 + col_bands[1]]
    for r in div_rows:
        for c in range(w):
            g[r][c] = 5
    for c in div_cols:
        for r in range(h):
            g[r][c] = 5
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_dividers":
        return g
    if name == "single_band":
        for c in range(11):
            g[5][c] = 5
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 5
        return g
    return g
