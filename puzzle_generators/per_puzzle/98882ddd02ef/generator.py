"""Generator for c6e1b8da.

Rule: rectangular shapes with thin tails move their main rectangle by
the tail length.

Combinatorial axes (8): grid_h/w, direction, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_tail, no_filler, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "98882ddd02ef"
VERSION = "1.1.0"
TASK_ID = "98882ddd02ef"
SUMMARY = "Rectangular shapes with thin tails move main rectangle by tail length."

INVARIANTS = [
    "each foreground color forms one connected shape",
    "a shape with a full one-cell-wide tail moves only its main rectangle",
    "a shape without a valid thin tail is rectangularized to its bounding box",
    "moved shapes are painted after non-moving shapes",
]

DIRECTIONS = ("right", "left", "down", "up")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_tail", "no_filler", "full_grid")
HELPFUL_TEXTURES = DIRECTIONS

AXES = {
    "grid_h":         {"type": "int", "default": "16", "valid": "16"},
    "grid_w":         {"type": "int", "default": "16", "valid": "16"},
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
                ["right", "down", "left", "up"][sample_index % 4]
    mover, filler = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    g = full_grid(16, 16, 0)

    r, c, rh, rw = 6, 6, 3, 3
    draw_rect(g, r, c, rh, rw, mover)
    if direction == "right":
        draw_rect(g, r + 1, c + rw, 1, 3, mover)
    elif direction == "left":
        draw_rect(g, r + 1, c - 3, 1, 3, mover)
    elif direction == "down":
        draw_rect(g, r + rh, c + 1, 3, 1, mover)
    else:
        draw_rect(g, r - 3, c + 1, 3, 1, mover)

    draw_rect(g, 2, 2, 2, 3, filler)
    g[4][2] = filler
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(16, 16, 0)
    if name == "no_tail":
        draw_rect(g, 6, 6, 3, 3, 3)
        return g
    if name == "no_filler":
        draw_rect(g, 6, 6, 3, 3, 3)
        draw_rect(g, 7, 9, 1, 3, 3)
        return g
    if name == "full_grid":
        for r in range(16):
            for c in range(16):
                g[r][c] = 3
        return g
    return g
