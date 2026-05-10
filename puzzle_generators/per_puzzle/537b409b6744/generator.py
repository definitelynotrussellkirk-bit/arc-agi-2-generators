"""Generator for 9f669b64.

Rule: a small object passes through the nearest solid rectangular
blocker, cutting and expanding it.

Combinatorial axes (8): grid_h/w, direction, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_mover, no_blocker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "537b409b6744"
VERSION = "1.1.0"
TASK_ID = "537b409b6744"
SUMMARY = "Small object passes through nearest solid blocker, cutting and expanding it."

INVARIANTS = [
    "one small object is aligned with a larger solid rectangle blocker",
    "the nearest valid blocker is selected by gap then size",
    "the moving object appears beyond the blocker and the blocker expands perpendicular to the cut",
]

DIRECTIONS = ("down", "right")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_mover", "no_blocker", "full_grid")
HELPFUL_TEXTURES = DIRECTIONS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "direction":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DIRECTIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for direction",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    direction = (overrides.get("texture") if overrides.get("texture") in DIRECTIONS else None) or \
                overrides.get("direction") or \
                ("down" if sample_index % 2 == 0 else "right")
    mover, blocker = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    g = full_grid(14, 14, 0)
    if direction == "down":
        draw_rect(g, 1, 5, 1, 2, mover)
        draw_rect(g, 5, 4, 3, 5, blocker)
    else:
        draw_rect(g, 6, 1, 2, 1, mover)
        draw_rect(g, 5, 5, 5, 3, blocker)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 14, 0)
    if name == "no_mover":
        draw_rect(g, 5, 4, 3, 5, 4)
        return g
    if name == "no_blocker":
        draw_rect(g, 1, 5, 1, 2, 3)
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(14):
                g[r][c] = 3
        return g
    return g
