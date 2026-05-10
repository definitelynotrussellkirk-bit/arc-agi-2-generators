"""Generator for arc_puzzle_bank_sixteenth_21_bundle:easy_112_cast_rightward_rays_until_blockers.

Rule: each row has a colored emitter; rays extend right in emitter color
until they hit a gray (8) blocker.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rays,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blocker, blocker_left_of_emitter, no_emitter.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f8b9516df05e"
VERSION = "1.1.0"
TASK_ID = "f8b9516df05e"
SUMMARY = "Each active row has a colored emitter and a gray blocker to its right."

INVARIANTS = [
    "background is 0",
    "blocker color is 8",
    "active rows have one non-8 emitter left of one blocker",
    "cells between emitter and blocker are initially empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blocker", "blocker_left_of_emitter", "no_emitter")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "3..18"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "5..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rays":           {"type": "int", "default": "rng 3..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "emitter_then_blocker",
                       "valid": "emitter_then_blocker"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "density":        {"type": "str", "default": "row_pairs", "valid": "row_pairs"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        target = min(ctx.draw_int("rays", 3, 3), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 13)
        target = min(ctx.draw_int("rays", 4, 5), h)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 13)
        target = min(ctx.draw_int("rays", 3, 5), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), target)
    for r in rows:
        c0 = rng.randint(0, w - 4)
        c1 = rng.randint(c0 + 2, w - 1)
        g[r][c0] = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
        g[r][c1] = 8
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_blocker":
        # emitter without rightward 8-blocker → ray would extend off the grid
        g[2][1] = 3
        g[5][2] = 6
        return g
    if name == "blocker_left_of_emitter":
        # 8-blocker left of emitter → ray fired right has no blocker to stop at
        g[2][1] = 8; g[2][5] = 4
        g[5][2] = 8; g[5][6] = 6
        return g
    if name == "no_emitter":
        # blockers but no emitters → no rays to cast
        g[2][5] = 8
        g[5][6] = 8
        return g
    return g
