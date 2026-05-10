"""Generator for additional_bank:M3.

Rule: find 5-divider column; for each cell, mirror left side to right
where right is 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_blob, right_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dce32baca018"
VERSION = "1.1.0"
TASK_ID = "dce32baca018"
SUMMARY = "Vertical 5-divider + small blob on left + empty right; output mirrors blob to right."

INVARIANTS = [
    "exactly one full-column 5-divider",
    "left side has 2-4 cells of 1-2 colors",
    "right side is fully 0 (so mirror has somewhere to write)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_blob", "right_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "left_blob_centered_div",
                       "valid": "left_blob_centered_div"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 7, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 7, 9)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    div = w // 2
    for r in range(h):
        g[r][div] = 5
    color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    n = rng.randint(2, 4)
    placed = 0
    while placed < n:
        r = rng.randint(0, h - 1); c = rng.randint(0, div - 1)
        if g[r][c] != 0: continue
        mc = 2 * div - c
        if not (0 <= mc < w): continue
        g[r][c] = color; placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # left blob without divider → no axis to mirror across
        g[1][1] = 4; g[2][2] = 4; g[4][1] = 4
        return g
    if name == "no_blob":
        # divider but no left cells → nothing to mirror
        for r in range(h): g[r][w // 2] = 5
        return g
    if name == "right_already_filled":
        # both sides populated → mirror collides with existing right cells
        for r in range(h): g[r][w // 2] = 5
        g[1][1] = 4; g[2][2] = 4
        g[1][w - 2] = 6; g[2][w - 3] = 6
        return g
    return g
