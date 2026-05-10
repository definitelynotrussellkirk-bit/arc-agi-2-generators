"""Generator for 3617dc99.

Rule: a red seed and a blue seed sit at opposite ends of a gray (color-5)
corridor with side branches.

Combinatorial axes (8): grid_h, grid_w, palette_kind, num_branches,
branch_offset, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_corridor, seeds_collide, no_branches.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7073328cf3f2"
VERSION = "1.1.0"
TASK_ID = "7073328cf3f2"
SUMMARY = "A red seed and blue seed sit at opposite ends of a gray corridor with optional side branches."

INVARIANTS = [
    "background is 0",
    "one red cell and one blue cell are connected by color-5 corridor cells",
    "side branches of color 5 touch the corridor near each seed",
]

PALETTE_KINDS = ("default", "narrow_corridor", "wide_corridor", "spread_branches")
DEGENERATE_TEXTURES = ("no_corridor", "seeds_collide", "no_branches")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "7", "valid": "7"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_branches":   {"type": "int", "default": "2", "valid": "2"},
    "branch_offset":  {"type": "str", "default": "rng", "valid": "rng"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "horizontal_corridor",
                       "valid": "horizontal_corridor"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        width = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        width = ctx.draw_int("grid_w", 10, 11)
    else:
        width = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    h = 7
    mid = h // 2
    g = full_grid(h, width, 0)
    left = 1
    right = width - 2
    g[mid][left] = 2
    g[mid][right] = 1
    for c in range(left + 1, right):
        g[mid][c] = 5
    red_branch_c = rng.randint(left + 1, left + 2)
    blue_branch_c = rng.randint(right - 2, right - 1)
    for r in range(1, mid):
        g[r][red_branch_c] = 5
    for r in range(mid + 1, h - 1):
        g[r][blue_branch_c] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    mid = h // 2
    g = full_grid(h, w, 0)
    if name == "no_corridor":
        # red + blue but no gray cells connecting them
        g[mid][1] = 2
        g[mid][w - 2] = 1
        return g
    if name == "seeds_collide":
        # red and blue at the same cell — invalid endpoints
        g[mid][3] = 2
        g[mid][3] = 1
        for c in range(1, w - 1):
            g[mid][c] = 5
        return g
    if name == "no_branches":
        # corridor exists but no side branches
        g[mid][1] = 2
        g[mid][w - 2] = 1
        for c in range(2, w - 2):
            g[mid][c] = 5
        return g
    return g
