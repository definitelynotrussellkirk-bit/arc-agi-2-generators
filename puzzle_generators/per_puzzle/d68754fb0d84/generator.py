"""Generator for arc_additional_puzzle_bank_volume6:H41.

Rule: each local control code immediately left of a maroon anchor
stamps a dihedral variant of the blue template in green.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_anchors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, missing_anchor, missing_code.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "d68754fb0d84"
VERSION = "1.1.0"
TASK_ID = "d68754fb0d84"
SUMMARY = "Each local control code immediately left of a maroon anchor stamps a dihedral variant of the blue template in green."

INVARIANTS = [
    "one blue template appears before all control cells",
    "each maroon anchor has a transform code immediately to its left",
    "all selected variants fit in-bounds",
    "the output contains only green stamped variants",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "missing_anchor", "missing_code")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..15", "valid": "9..24"},
    "grid_w":         {"type": "int", "default": "rng 14..19", "valid": "11..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_anchors":      {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "template_left",
                       "valid": "template_left"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
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
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 14, 16)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 17, 19)
    else:
        h = ctx.draw_int("grid_h", 11, 15)
        w = ctx.draw_int("grid_w", 14, 19)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, [(0, 0), (1, 0), (2, 0), (2, 1)], 2)
    spots = [(1, w - 6), (h // 2, w - 6), (h - 5, 3)]
    codes = [1, 5, 7, 8, 3, 4, 6]
    rng.shuffle(codes)
    for (r, c), code in zip(spots, codes):
        g[r][c] = code
        g[r][c + 1] = 9
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 16
    g = full_grid(h, w, 0)
    if name == "no_template":
        # no blue template → no variant to stamp from
        for (r, c), code in zip([(1, w - 6), (5, w - 6), (h - 5, 3)], [1, 5, 7]):
            g[r][c] = code
            g[r][c + 1] = 9
        return g
    if name == "missing_anchor":
        # control codes exist but no maroon (9) anchor follows → no stamp target
        paint_at(g, 1, 1, [(0, 0), (1, 0), (2, 0), (2, 1)], 2)
        g[1][w - 6] = 1
        g[5][w - 6] = 5
        return g
    if name == "missing_code":
        # maroon anchors exist but the cell immediately left is empty → control undefined
        paint_at(g, 1, 1, [(0, 0), (1, 0), (2, 0), (2, 1)], 2)
        g[1][w - 5] = 9
        g[5][w - 5] = 9
        return g
    return g
