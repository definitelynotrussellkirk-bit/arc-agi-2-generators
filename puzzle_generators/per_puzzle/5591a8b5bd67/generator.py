"""Generator for arc_puzzle_bank_tenth_21_bundle:easy_69_cast_rightward_rays_until_wall.

Rule: non-gray seeds cast rightward rays through zeros until gray walls.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rays,
palette_size, position_bias, n_distinct_colors, wall_density, texture.
Degenerates: no_seeds, seed_at_right_edge, blocked_immediately.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5591a8b5bd67"
VERSION = "1.1.0"
TASK_ID = "5591a8b5bd67"
SUMMARY = "Non-gray seeds cast rightward rays through zeros until gray walls."

INVARIANTS = [
    "background is 0",
    "wall color is 5",
    "each active row has one non-5 seed",
    "optional gray wall sits to the seed's right",
]

PALETTE_KINDS = ("default", "no_walls", "few_walls", "many_walls")
DEGENERATE_TEXTURES = ("no_seeds", "seed_at_right_edge", "blocked_immediately")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "3..16"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "4..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rays":           {"type": "int", "default": "rng 3..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 2..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "rows", "valid": "rows"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..5", "valid": "1..9"},
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
        w = ctx.draw_int("grid_w", 9, 11)
        target = min(ctx.draw_int("rays", 2, 3), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 12, 13)
        target = min(ctx.draw_int("rays", 4, 5), h)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 9, 13)
        target = min(ctx.draw_int("rays", 3, 5), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for r in rng.sample(range(h), target):
        c0 = rng.randint(0, w - 3)
        g[r][c0] = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
        if rng.randrange(2) == 0:
            g[r][rng.randint(c0 + 2, w - 1)] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 11
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # empty grid — no rays to cast
        return g
    if name == "seed_at_right_edge":
        # seed on rightmost col → ray length 0
        g[3][w - 1] = 4
        return g
    if name == "blocked_immediately":
        # seed with a wall immediately to its right → ray length 0
        g[3][2] = 4
        g[3][3] = 5
        return g
    return g
