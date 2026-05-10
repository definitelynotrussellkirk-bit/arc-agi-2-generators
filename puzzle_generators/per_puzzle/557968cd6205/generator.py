"""Generator for arc_puzzle_bank_21_set18_bundle:medium_p02 — column height summary.

Rule: take the (single) non-bg blob, crop to its bbox, then output a
column-density bar histogram (height = max column count). Same shape
as 19:p06 but the source is the blob, not the whole grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, stair_w,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blob, uniform_columns, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "557968cd6205"
VERSION = "1.1.0"
TASK_ID = "557968cd6205"
SUMMARY = "One non-bg blob with a recognizable column-density shape."

INVARIANTS = [
    "background is 0",
    "exactly one connected non-bg blob",
    "the blob's column counts vary (so output isn't a solid block)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blob", "uniform_columns", "single_cell")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "stair_w":        {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "single_blob_with_varied_cols",
                       "valid": "single_blob_with_varied_cols"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        sw = ctx.draw_int("stair_w", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        sw = ctx.draw_int("stair_w", 4, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
        sw = ctx.draw_int("stair_w", 3, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    sh = sw
    r0 = rng.randint(1, h - sh - 1)
    c0 = rng.randint(1, w - sw - 1)
    pattern = [
        [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)],
    ]
    cells = rng.choice(pattern)
    for dr, dc in cells:
        rr, cc = r0 + dr, c0 + dc
        if 0 <= rr < h and 0 <= cc < w:
            g[rr][cc] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_blob":
        # blank → no blob to extract column histogram from
        return g
    if name == "uniform_columns":
        # solid rectangle → all column counts equal, no histogram contrast
        for r in range(2, 5):
            for c in range(3, 6):
                g[r][c] = 4
        return g
    if name == "single_cell":
        # 1 cell blob → bbox 1x1, histogram is single bar height 1
        g[3][4] = 4
        return g
    return g
