"""Generator for arc_puzzle_bank_eleventh_21_bundle:easy_76_cast_vertical_rays_downward.

Rule: place colored emitters in distinct columns; each casts a vertical
ray downward to the grid bottom.

Combinatorial axes (8): grid_h, grid_w, palette_kind, emitters,
palette_size, position_bias, n_distinct_colors, emitter_density, texture.
Degenerates: no_emitters, emitter_at_bottom, two_emitters_same_col.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8fca6bf05488"
VERSION = "1.1.0"
TASK_ID = "8fca6bf05488"
SUMMARY = "Place colored emitters in distinct columns; each casts a vertical ray downward."

INVARIANTS = [
    "background is 0",
    "every nonzero cell is a vertical ray emitter",
    "emitters occupy distinct columns",
    "each emitter has at least one empty cell below it",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_emitters", "emitter_at_bottom", "two_emitters_same_col")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "3..16"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "3..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "emitters":       {"type": "int", "default": "rng 2..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 2..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "distinct_cols", "valid": "distinct_cols"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..5", "valid": "1..9"},
    "emitter_density": {"type": "str", "default": "mixed", "valid": "mixed"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        target = min(ctx.draw_int("emitters", 2, 3), w)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        target = min(ctx.draw_int("emitters", 4, 5), w)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
        target = min(ctx.draw_int("emitters", 2, 5), w)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for c in rng.sample(range(w), target):
        r = rng.randint(0, h - 2)
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_emitters":
        # empty grid — no rays to cast
        return g
    if name == "emitter_at_bottom":
        # emitter on bottom row → ray has zero length below
        g[h - 1][3] = 5
        return g
    if name == "two_emitters_same_col":
        # two emitters share a column → ray-source ambiguity
        g[1][4] = 4
        g[3][4] = 7
        return g
    return g
