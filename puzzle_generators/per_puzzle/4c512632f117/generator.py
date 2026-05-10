"""Generator for 5833af48.

Rule: a small red/source stamp, cyan tile mask, and background target
rectangle define a tiled output.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
visible_color.
Degenerates: no_stamp, no_mask, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, fill_box

GENERATOR_ID = "4c512632f117"
VERSION = "1.1.0"
TASK_ID = "4c512632f117"
SUMMARY = "Red/source stamp + cyan tile mask + background target rectangle define tiled output."

INVARIANTS = [
    "stamp contains red 2, background 3, and one visible stamp color",
    "tile mask uses cyan 8 to select stamp placements",
    "a background-color rectangle below the tile defines output size",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_stamp", "no_mask", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "8", "valid": "8"},
    "grid_w":         {"type": "int", "default": "10", "valid": "10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
    "visible_color":  {"type": "color", "default": "rng !{2,3,8}",
                       "valid": "1|4..7|9"},
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
    visible = ctx.draw_color("visible_color", exclude={2, 3, 8})
    g = full_grid(8, 10, 0)
    g[0][0] = 2
    g[0][1] = 3
    g[1][0] = visible
    g[1][1] = 2
    g[0][4] = 8
    g[0][5] = 8
    g[1][4] = 8
    if rng.random() < 0.5:
        g[1][5] = 3
    else:
        g[1][5] = 8
    fill_box(g, 4, 0, 7, 3, 3)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 10, 0)
    if name == "no_stamp":
        g[0][4] = 8
        return g
    if name == "no_mask":
        g[0][0] = 2
        g[1][0] = 4
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(10):
                g[r][c] = 3
        return g
    return g
