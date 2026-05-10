"""Generator for arc_puzzle_bank_21_set10_s:S10_E1.

Rule: color-2 emitters shoot rightward beams through zero cells until a
wall or grid edge.

Combinatorial axes (8): grid_h, grid_w, palette_kind, emitter_count,
palette_size, position_bias, n_distinct_colors, wall_density, texture.
Degenerates: no_emitters, emitter_at_right_edge, blocked_immediately.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fa2e57ec3fa2"
VERSION = "1.1.0"
TASK_ID = "fa2e57ec3fa2"
SUMMARY = "Color-2 emitters shoot rightward beams through zero cells until a wall or grid edge."

INVARIANTS = [
    "background is 0",
    "one to three color-2 emitters appear with clear cells to their right",
    "optional color-5 walls stop some beams",
    "beam cells are painted 7 by the oracle",
]

PALETTE_KINDS = ("default", "no_walls", "few_walls", "many_walls")
DEGENERATE_TEXTURES = ("no_emitters", "emitter_at_right_edge", "blocked_immediately")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "emitter_count":  {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rows", "valid": "rows"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "wall_density":   {"type": "str", "default": "mixed", "valid": "mixed"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        count = ctx.draw_int("emitter_count", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 12)
        count = ctx.draw_int("emitter_count", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 12)
        count = ctx.draw_int("emitter_count", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), count)
    for r in rows:
        c = rng.randint(0, w - 4)
        g[r][c] = 2
        if rng.random() < 0.65:
            wall_c = rng.randint(c + 2, w - 1)
            g[r][wall_c] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_emitters":
        # empty grid — no rays to project
        return g
    if name == "emitter_at_right_edge":
        # emitter on rightmost col → ray length 0 (no cells to paint)
        g[3][w - 1] = 2
        return g
    if name == "blocked_immediately":
        # emitter with a wall on the very next cell → ray length 0
        g[3][2] = 2
        g[3][3] = 5
        return g
    return g
