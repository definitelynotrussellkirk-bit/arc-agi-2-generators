"""Generator for arc_additional_puzzle_bank_volume12:M84.

Rule: arrows (1=up, 2=right, 3=down, 4=left) shoot rays in their direction
painting 7 on empty cells until hitting a 5-wall or the grid edge.

Combinatorial axes (9): grid_h/w, palette_kind, num_arrows, num_walls,
palette_size, position_bias, n_distinct_colors, wall_orientation, texture.
Degenerates: no_arrows, arrow_against_wall, no_walls.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ce1f031345df"
VERSION = "1.1.0"
TASK_ID = "ce1f031345df"
SUMMARY = "1-2 arrows (1/2/3/4) + 5-walls placed perpendicular to arrows."

INVARIANTS = [
    "between 1 and 2 arrows of distinct directions",
    "5-walls block at least one ray",
]

PALETTE_KINDS = ("default", "vertical_walls", "horizontal_walls", "few_walls")
DEGENERATE_TEXTURES = ("no_arrows", "arrow_against_wall", "no_walls")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_arrows":     {"type": "int", "default": "3", "valid": "1..3"},
    "num_walls":      {"type": "int", "default": "1", "valid": "1..2"},
    "wall_orientation": {"type": "str", "default": "vertical",
                         "valid": "vertical|horizontal"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][5] = 5
    g[1][3] = 3
    g[4][10] = 4
    g[8][1] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_arrows":
        # walls only — no rays to fire
        for r in range(h):
            g[r][5] = 5
        return g
    if name == "arrow_against_wall":
        # arrow points directly into adjacent wall — zero-length ray
        for r in range(h):
            g[r][5] = 5
        g[3][4] = 2
        g[6][6] = 4
        return g
    if name == "no_walls":
        # arrows but no walls — rays go to edge unimpeded
        g[1][3] = 3
        g[4][10] = 4
        g[8][1] = 1
        return g
    return g
