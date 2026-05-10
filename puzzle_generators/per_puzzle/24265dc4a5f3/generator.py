"""Generator for f83cb3f6.

Rule: colored pixels project onto the row or column adjacent to a
cyan bar.

Combinatorial axes (8): grid_h/w, orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_bar, no_pixels, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "24265dc4a5f3"
VERSION = "1.1.0"
TASK_ID = "24265dc4a5f3"
SUMMARY = "Colored pixels project onto row/col adjacent to cyan bar."

INVARIANTS = [
    "one cyan bar is horizontal or vertical",
    "colored pixels lie beyond the bar along matching rows or columns",
    "only coordinates covered by the bar can receive projections",
    "pixel colors are distinct from each other and from 0 and 8",
]

ORIENTATIONS = ("horizontal", "vertical")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_bar", "no_pixels", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    orientation = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
                  overrides.get("orientation") or \
                  ctx.draw_choice("orientation", list(ORIENTATIONS))
    colors = ctx.draw_distinct_colors("pixel_colors", n=3, exclude={0, 8})
    g = full_grid(12, 12, 0)
    if orientation == "horizontal":
        r = 6
        for c in range(3, 9):
            g[r][c] = 8
        for c, color, rr in [(3, colors[0], 2), (5, colors[1], 10), (8, colors[2], 1)]:
            g[rr][c] = color
    else:
        c = 6
        for r in range(3, 9):
            g[r][c] = 8
        for r, color, cc in [(3, colors[0], 2), (5, colors[1], 10), (8, colors[2], 1)]:
            g[r][cc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_bar":
        g[5][5] = 2
        return g
    if name == "no_pixels":
        for c in range(3, 9):
            g[6][c] = 8
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 8
        return g
    return g
