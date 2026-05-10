"""Generator for arc_puzzle_bank_seventeenth21:M113 — recolor from 2-row legend.

Rule: top 2 rows hold (src, dst) pairs at the same column. Below row 1,
each non-zero cell with value v becomes dst if v matches some src.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_content, content_color_not_in_legend.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "0cf12bd584ef"
VERSION = "1.1.0"
TASK_ID = "0cf12bd584ef"
SUMMARY = "2-row legend (src on row 0, dst on row 1) at distinct cols + content below."

INVARIANTS = [
    "background is 0",
    "row 0 has 2 distinct src colors at 2 distinct cols",
    "row 1 has 2 dst colors at the same cols",
    "below row 1: blobs in src colors (so legend remap is non-trivial)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_content", "content_color_not_in_legend")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "2", "valid": "2..2"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "two_row_legend_top",
                       "valid": "two_row_legend_top"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    pal = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 4)
    src1, dst1, src2, dst2 = pal
    cols = sorted(rng.sample(range(w), 2))
    g[0][cols[0]] = src1; g[1][cols[0]] = dst1
    g[0][cols[1]] = src2; g[1][cols[1]] = dst2
    used = {(0, c) for c in cols} | {(1, c) for c in cols}
    for c in range(w):
        used.add((2, c))
    for src in (src1, src2):
        cells = grow_blob(rng, h, w, used, rng.randint(2, 3), max_attempts=80)
        if cells:
            for r, c in cells: g[r][c] = src
            used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # content but no top-row src/dst pairs → no remap dictionary
        for r, c in [(4, 2), (4, 3), (5, 3)]: g[r][c] = 4
        return g
    if name == "no_content":
        # only legend, no content below row 1 → identity output
        g[0][1] = 4; g[1][1] = 6
        g[0][5] = 7; g[1][5] = 8
        return g
    if name == "content_color_not_in_legend":
        # content uses a color not declared in legend → no remap applies
        g[0][1] = 4; g[1][1] = 6
        g[0][5] = 7; g[1][5] = 8
        for r, c in [(4, 2), (4, 3), (5, 3)]: g[r][c] = 9  # 9 not in legend
        return g
    return g
