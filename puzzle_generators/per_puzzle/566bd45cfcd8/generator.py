"""Generator for arc_puzzle_bank_seventh_21_bundle:hard_43_local_marked_rowcol_crossings_in_frames.

Combinatorial axes (8): grid_h, grid_w, palette_kind, variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, no_keys, no_markers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "566bd45cfcd8"
VERSION = "1.1.0"
TASK_ID = "566bd45cfcd8"
SUMMARY = "Inside each keyed frame, paint row-marker and column-marker intersections with the frame key."

INVARIANTS = [
    "color-5 rectangular frames contain local row endpoint markers in color 2",
    "the same interiors contain local column endpoint markers in color 3",
    "a nonzero key marker above each frame gives the intersection fill color",
    "only local row/column crossings inside each frame are filled",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_keys", "no_markers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "8", "valid": "8..8"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "variant":        {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "two_keyed_5frames",
                       "valid": "two_keyed_5frames"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _add_frame(g, top, left, key, row_offsets, col_offsets):
    draw_frame(g, top, left, top + 5, left + 5, 5)
    g[top - 1][left + 2] = key
    ir0, ic0, ir1, ic1 = top + 1, left + 1, top + 4, left + 4
    for roff in row_offsets:
        r = ir0 + roff
        g[r][ic0] = 2
        g[r][ic1] = 2
    for coff in col_offsets:
        c = ic0 + coff
        g[ir0][c] = 3
        g[ir1][c] = 3


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        variant = ctx.draw_int("variant", 0, 1)
    elif difficulty == "hard":
        variant = ctx.draw_int("variant", 2, 4)
    else:
        variant = ctx.draw_int("variant", 0, 4)
    g = full_grid(8, 14, 0)
    row_choices = [[1], [2], [1, 2], [0, 2], [1, 3]]
    col_choices = [[1], [2], [1, 2], [0, 3], [2, 3]]
    _add_frame(g, 1, 1, 4 + (variant % 4), row_choices[variant], col_choices[variant])
    _add_frame(g, 1, 8, 7 + (variant % 3), row_choices[-1 - variant], col_choices[variant])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 14, 0)
    if name == "no_frames":
        # markers + keys without 5-frames → no scope to find crossings inside
        g[0][3] = 4; g[0][10] = 6
        g[3][1] = 2; g[3][8] = 2
        g[1][3] = 3; g[1][10] = 3
        return g
    if name == "no_keys":
        # frames + markers but no key colors → no fill color defined
        draw_frame(g, 1, 1, 6, 6, 5)
        draw_frame(g, 1, 8, 6, 13, 5)
        for r in [3]: g[r][2] = 2; g[r][5] = 2
        for c in [3]: g[2][c] = 3; g[5][c] = 3
        return g
    if name == "no_markers":
        # frames + keys but no row/col markers → no crossings to compute
        draw_frame(g, 1, 1, 6, 6, 5)
        draw_frame(g, 1, 8, 6, 13, 5)
        g[0][3] = 4; g[0][10] = 6
        return g
    return g
