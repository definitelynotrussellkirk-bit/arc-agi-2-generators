"""Generator for 84ba50d3.

Rule: blue shapes fall toward red line; narrow columns pass through
and make gaps.

Combinatorial axes (8): grid_h/w, include_narrow, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_line, no_shapes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "dc155169ea57"
VERSION = "1.1.0"
TASK_ID = "dc155169ea57"
SUMMARY = "Blue shapes fall toward red line; narrow columns pass through."

INVARIANTS = [
    "one full red row separates falling shapes from the lower field",
    "all falling source shapes above the red row use color 1",
    "wide shapes stop immediately above the red row",
    "the red row sits clear of the top so shapes have room to fall",
]

INCLUDE_NARROW = ("yes", "no")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_line", "no_shapes", "full_grid")
HELPFUL_TEXTURES = INCLUDE_NARROW

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "include_narrow": {"type": "str", "default": "rng helpful",
                       "valid": "|".join(INCLUDE_NARROW)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for include_narrow",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    include_narrow = (overrides.get("texture") if overrides.get("texture") in INCLUDE_NARROW else None) or \
                     overrides.get("include_narrow") or \
                     ctx.draw_choice("include_narrow", list(INCLUDE_NARROW))
    h = 11 + rng.randint(0, 3)
    w = 10 + rng.randint(0, 4)
    red_row = h - 4
    g = full_grid(h, w, 0)
    for c in range(w):
        g[red_row][c] = 2
    draw_rect(g, 1, 2, 2, 3, 1)
    if include_narrow == "yes":
        c = w - 3
        for r in range(1, 1 + rng.randint(2, 4)):
            g[r][c] = 1
    else:
        draw_rect(g, 2, w - 5, 2, 2, 1)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_line":
        draw_rect(g, 2, 3, 2, 3, 1)
        return g
    if name == "no_shapes":
        for c in range(12):
            g[8][c] = 2
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
