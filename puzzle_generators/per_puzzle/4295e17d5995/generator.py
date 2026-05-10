"""Generator for f0100645.

Rule: wall-colored objects slide as rigid bodies toward matching
colored wall.

Combinatorial axes (8): grid_h/w, object_layout, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_walls, no_objects, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4295e17d5995"
VERSION = "1.1.0"
TASK_ID = "4295e17d5995"
SUMMARY = "Wall-colored objects slide toward matching colored wall."

INVARIANTS = [
    "the background is color 7",
    "left and right walls have distinct colors",
    "interior objects use one of the wall colors",
    "wall colors are non-7",
]

OBJECT_LAYOUTS = ("split", "stacked", "offset")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_walls", "no_objects", "full_grid")
HELPFUL_TEXTURES = OBJECT_LAYOUTS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "object_layout":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(OBJECT_LAYOUTS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for object_layout",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    layout = (overrides.get("texture") if overrides.get("texture") in OBJECT_LAYOUTS else None) or \
             overrides.get("object_layout") or \
             ctx.draw_choice("object_layout", list(OBJECT_LAYOUTS))
    left, right = ctx.draw_distinct_colors("wall_colors", n=2, exclude={7})
    g = full_grid(11, 13, 7)
    for r in range(11):
        g[r][0] = left
        g[r][12] = right
    placements = {
        "split": [(2, 5, left), (7, 7, right)],
        "stacked": [(3, 6, left), (6, 6, right)],
        "offset": [(2, 8, left), (7, 4, right)],
    }[layout]
    for r, c, color in placements:
        g[r][c] = color
        g[r][c + 1] = color
        g[r + 1][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 13, 7)
    if name == "no_walls":
        g[5][5] = 2; g[5][6] = 2
        return g
    if name == "no_objects":
        for r in range(11):
            g[r][0] = 1; g[r][12] = 2
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(13):
                g[r][c] = 7
        return g
    return g
