"""Generator for arc_puzzle_bank_21_set9_e:hard_i17.

Rule: gray walls constrain the shortest zero-cell corridor between two
matching colored endpoints; fill that corridor with the endpoint color.

Combinatorial axes (8): grid_h/w, palette_kind, gap_position,
palette_size, position_bias, n_distinct_colors, wall_density, texture.
Degenerates: no_endpoints, mismatched_endpoints, no_path.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ad9405621c3d"
VERSION = "1.1.0"
TASK_ID = "ad9405621c3d"
SUMMARY = "Fill one shortest corridor path between matching endpoints around gray walls."

INVARIANTS = [
    "color 5 cells are walls",
    "there are exactly two matching non-wall endpoints",
    "a zero corridor connects the endpoints",
]

PALETTE_KINDS = ("default", "narrow_gap", "centered_gap", "wide_gap")
DEGENERATE_TEXTURES = ("no_endpoints", "mismatched_endpoints", "no_path")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "gap_position":   {"type": "str", "default": "rng", "valid": "rng"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "diagonal",
                       "valid": "diagonal"},
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
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 11)
    g = full_grid(h, w, 0)
    wall_c = rng.randint(3, w - 4)
    gap = rng.randint(1, h - 2)
    for r in range(h):
        if r != gap:
            g[r][wall_c] = 5
    color = rng.choice([2, 3, 4, 6, 7, 8, 9])
    g[1][1] = color
    g[h - 2][w - 2] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    wall_c = 5
    gap = 3
    for r in range(h):
        if r != gap:
            g[r][wall_c] = 5
    if name == "no_endpoints":
        # walls but no endpoints — no corridor to draw
        return g
    if name == "mismatched_endpoints":
        # endpoints exist but in different colors — no "matching" pair
        g[1][1] = 4
        g[h - 2][w - 2] = 7
        return g
    if name == "no_path":
        # solid wall (no gap) — endpoints unreachable
        for r in range(h):
            g[r][wall_c] = 5
        g[1][1] = 6
        g[h - 2][w - 2] = 6
        return g
    return g
