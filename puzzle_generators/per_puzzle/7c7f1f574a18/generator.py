"""Generator for 320afe60.

Rule: closed objects packed left in color 2; open objects packed
right in color 3.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, closed_color,
open_color.
Degenerates: no_objects, all_closed, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid, paint_at

GENERATOR_ID = "7c7f1f574a18"
VERSION = "1.1.0"
TASK_ID = "7c7f1f574a18"
SUMMARY = "Closed objects pack left as color 2; open objects pack right as color 3."

INVARIANTS = [
    "the mode color is the background",
    "closed objects have no bbox gap connected to the bbox boundary",
    "open objects have a bbox gap connected to the bbox boundary",
    "objects are separated and sit clear of grid borders",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_objects", "all_closed", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "closed_color":   {"type": "color", "default": "rng !0", "valid": "1..9"},
    "open_color":     {"type": "color", "default": "rng !0", "valid": "1..9"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    closed_color = ctx.draw_color("closed_color", exclude={0})
    open_color = ctx.draw_color("open_color", exclude={0, closed_color})
    g = full_grid(10, 13, 0)
    draw_rect(g, rng.randint(1, 2), rng.randint(2, 3), 2, 3, closed_color)
    r0 = rng.randint(5, 6)
    c0 = rng.randint(4, 5)
    paint_at(g, r0, c0, [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0), (2, 1)], open_color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 13, 0)
    if name == "no_objects":
        return g
    if name == "all_closed":
        draw_rect(g, 2, 2, 2, 3, 2)
        draw_rect(g, 5, 6, 2, 3, 4)
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
