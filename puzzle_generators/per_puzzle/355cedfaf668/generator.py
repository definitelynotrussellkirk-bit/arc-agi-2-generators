"""Generator for arc_puzzle_bank_21_set14_s:S14_M2.

Rule: a corner code chooses row-span or column-span closure for all
non-marker objects.

Combinatorial axes (8): grid_h, grid_w, palette_kind, mode,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_code, invalid_code, no_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "355cedfaf668"
VERSION = "1.1.0"
TASK_ID = "355cedfaf668"
SUMMARY = "A corner code chooses row-span or column-span closure for all non-marker objects."

INVARIANTS = [
    "background is 0",
    "cell (0,0) is a marker: 1 chooses row closure and 2 chooses column closure",
    "marker colors 1 and 2 are excluded from closure",
    "at least one colored object has a span gap along the chosen axis",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_code", "invalid_code", "no_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..15"},
    "grid_w":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "mode":           {"type": "str", "default": "rng row|col",
                       "valid": "row|col"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "code_top_left",
                       "valid": "code_top_left"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

ROW_GAP = [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)]
COL_GAP = [(0, 0), (2, 0), (0, 1), (1, 1), (2, 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 9, 10)
        w = ctx.draw_int("width", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 11, 12)
        w = ctx.draw_int("width", 14, 15)
    else:
        h = ctx.draw_int("height", 9, 12)
        w = ctx.draw_int("width", 12, 15)
    mode = ctx.draw_choice("mode", ["row", "col"])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)

    g[0][0] = 1 if mode == "row" else 2
    paint_at(g, rng.randint(2, 3), 2, ROW_GAP, 3)
    paint_at(g, h - 5, w - 5, COL_GAP, 4)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "missing_code":
        # cell (0,0) is bg → no closure axis chosen, rule is undefined
        paint_at(g, 2, 2, ROW_GAP, 3)
        paint_at(g, h - 5, w - 5, COL_GAP, 4)
        return g
    if name == "invalid_code":
        # cell (0,0) holds a non-{1,2} value → closure axis not specified
        g[0][0] = 5
        paint_at(g, 2, 2, ROW_GAP, 3)
        paint_at(g, h - 5, w - 5, COL_GAP, 4)
        return g
    if name == "no_objects":
        # marker present but no other objects → closure has nothing to apply to
        g[0][0] = 1
        return g
    return g
