"""Generator for arc_puzzle_bank_21_set7_s:S7_E1 — slide red component right.

Rule: a single red component slides right until blocked by a wall or
the grid edge.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blocker_kind,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_red, red_at_right_edge, red_against_wall.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bcf2f353f9e0"
VERSION = "1.1.0"
TASK_ID = "bcf2f353f9e0"

SUMMARY = "A single red component slides right until blocked by a wall or the grid edge."

INVARIANTS = [
    "background is 0",
    "there is exactly one color-2 component",
    "all other nonzero cells are blockers",
    "the red component has at least one clear rightward move",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_red", "red_at_right_edge", "red_against_wall")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blocker_kind":   {"type": "str", "default": "rng wall|edge", "valid": "wall|edge"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "left_red_with_blocker",
                       "valid": "left_red_with_blocker"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 10, 14)
    blocker_kind = ctx.draw_choice("blocker_kind", ["wall", "edge"])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shape = rng.choice(_SHAPES)
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    r0 = rng.randint(1, h - sh - 1)
    c0 = rng.randint(0, 2)
    for dr, dc in shape:
        g[r0 + dr][c0 + dc] = 2
    if blocker_kind == "wall":
        wall_c = rng.randint(c0 + sw + 2, w - 1)
        for r in range(max(0, r0 - 1), min(h, r0 + sh + 1)):
            g[r][wall_c] = 8
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 11
    g = full_grid(h, w, 0)
    if name == "no_red":
        # walls only, no red component → nothing to slide
        for r in range(h): g[r][7] = 8
        return g
    if name == "red_at_right_edge":
        # red already touching right edge → no rightward move possible
        g[3][w - 1] = 2
        g[4][w - 1] = 2
        return g
    if name == "red_against_wall":
        # red has wall right at its right side → rule is identity (no move)
        g[3][3] = 2
        g[4][3] = 2; g[4][4] = 2
        for r in range(2, 7): g[r][5] = 8
        return g
    return g
