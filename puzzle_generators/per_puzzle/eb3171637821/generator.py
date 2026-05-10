"""Generator for 7039b2d7.

Rule: uniform divider rows/cols define grid; output is cell-count
rectangle in other color.

Combinatorial axes (8): row_bands, col_bands, palette_kind, band_h_max,
band_w_max, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_dividers, all_dividers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "eb3171637821"
VERSION = "1.1.0"
TASK_ID = "eb3171637821"
SUMMARY = "Uniform divider rows + cols define grid; output is cell-count rectangle."

INVARIANTS = [
    "the input uses exactly one divider color and one cell color",
    "divider rows and columns are solid full lines",
    "non-divider bands have positive height and width",
    "the output dimensions equal the number of row bands by column bands",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_dividers", "all_dividers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "row_bands":      {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "col_bands":      {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "band_h_max":     {"type": "int", "default": "3", "valid": "1..5"},
    "band_w_max":     {"type": "int", "default": "3", "valid": "1..5"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
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
    if difficulty == "easy":
        rb_lo, rb_hi = 1, 2
        cb_lo, cb_hi = 1, 2
    elif difficulty == "hard":
        rb_lo, rb_hi = 4, 6
        cb_lo, cb_hi = 4, 6
    else:
        rb_lo, rb_hi = 2, 4
        cb_lo, cb_hi = 2, 4
    row_bands = ctx.draw_int("row_bands", rb_lo, rb_hi)
    col_bands = ctx.draw_int("col_bands", cb_lo, cb_hi)
    div_color, cell_color = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    bh_max = int(overrides.get("band_h_max", 3))
    bw_max = int(overrides.get("band_w_max", 3))
    band_h = [rng.randint(1, bh_max) for _ in range(row_bands)]
    band_w = [rng.randint(1, bw_max) for _ in range(col_bands)]
    h = sum(band_h) + row_bands - 1
    w = sum(band_w) + col_bands - 1
    g = full_grid(h, w, cell_color)
    r = band_h[0]
    for bh in band_h[1:]:
        for c in range(w):
            g[r][c] = div_color
        r += 1 + bh
    c = band_w[0]
    for bw in band_w[1:]:
        for rr in range(h):
            g[rr][c] = div_color
        c += 1 + bw
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    if name == "no_dividers":
        return full_grid(h, w, 2)
    if name == "all_dividers":
        return full_grid(h, w, 5)
    if name == "full_grid":
        return full_grid(h, w, 5)
    return full_grid(h, w, 2)
