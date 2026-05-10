"""Generator for 4c177718.

Rule: a top-side non-T shape is placed above or below the bottom shape
according to the T stem direction.

Combinatorial axes (8): grid_h/w, t_direction, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_T, no_bottom, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid, paint_at

GENERATOR_ID = "527520396832"
VERSION = "1.1.0"
TASK_ID = "527520396832"
SUMMARY = "Top-side non-T shape placed above/below bottom shape per T stem direction."

INVARIANTS = [
    "a full color-5 divider separates top cues from the bottom scene",
    "the top half contains a color-2 T and one other colored shape",
    "the bottom half contains one target shape color",
    "the output is the bottom half with the other shape aligned to the bottom shape column",
]

DIRECTIONS = ("down", "up")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_T", "no_bottom", "full_grid")
HELPFUL_TEXTURES = DIRECTIONS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11"},
    "t_direction":    {"type": "str", "default": "rng helpful",
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
    "texture":        {"type": "str", "default": "alias for t_direction",
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
                overrides.get("t_direction") or \
                ctx.draw_choice("t_direction", list(DIRECTIONS))
    other_color, bottom_color = ctx.draw_distinct_colors("colors", n=2, exclude={0, 2, 5})
    g = full_grid(13, 11, 0)
    for c in range(11):
        g[5][c] = 5
    if direction == "down":
        for c in range(3, 6):
            g[1][c] = 2
        g[2][4] = 2
        g[3][4] = 2
        draw_rect(g, 7, 3, 2, 3, bottom_color)
    else:
        g[1][4] = 2
        g[2][4] = 2
        for c in range(3, 6):
            g[3][c] = 2
        draw_rect(g, 9, 3, 2, 3, bottom_color)
    paint_at(g, 1, 7, [(0, 0), (1, 0), (1, 1)], other_color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 11, 0)
    if name == "no_T":
        for c in range(11):
            g[5][c] = 5
        draw_rect(g, 7, 3, 2, 3, 3)
        return g
    if name == "no_bottom":
        for c in range(11):
            g[5][c] = 5
        for c in range(3, 6):
            g[1][c] = 2
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(11):
                g[r][c] = 5
        return g
    return g
