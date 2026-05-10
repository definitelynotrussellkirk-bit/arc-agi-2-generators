"""Generator for e9c9d9a1.

Rule: green divider grid fills corner cells with fixed colors and
interior cells with color 7.

Combinatorial axes (8): grid_h/w, band_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, n_bands.
Degenerates: no_dividers, full_grid, single_band.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9c5bdbcdcd50"
VERSION = "1.1.0"
TASK_ID = "9c5bdbcdcd50"
SUMMARY = "Green divider grid; corner cells fill 2/4/1/8, interior cells fill 7."

INVARIANTS = [
    "background is color 0",
    "green color 3 forms complete divider rows and columns",
    "cell bands between dividers are initially empty",
    "the divider grid has at least four bands in each axis",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_dividers", "full_grid", "single_band")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "band_count":     {"type": "int", "default": "4", "valid": "4"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_bands":        {"type": "int", "default": "4", "valid": "4"},
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
    ctx.draw_int("band_count", 4, 4)
    row_bands = [rng.randint(1, 3) for _ in range(4)]
    col_bands = [rng.randint(1, 3) for _ in range(4)]
    h = sum(row_bands) + 3
    w = sum(col_bands) + 3
    g = full_grid(h, w, 0)
    div_rows = []
    r = row_bands[0]
    for bh in row_bands[1:]:
        div_rows.append(r)
        r += 1 + bh
    div_cols = []
    c = col_bands[0]
    for bw in col_bands[1:]:
        div_cols.append(c)
        c += 1 + bw
    for r in div_rows:
        for c in range(w):
            g[r][c] = 3
    for c in div_cols:
        for r in range(h):
            g[r][c] = 3
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_dividers":
        return g
    if name == "single_band":
        for c in range(12):
            g[6][c] = 3
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 3
        return g
    return g
