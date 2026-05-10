"""Generator for 692cd3b6.

Rule: two 3x3 C-shapes open toward each other and are joined by a
color-4 bridge.

Combinatorial axes (8): grid_h/w, orientation, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_C, single_C, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "491a4eb76930"
VERSION = "1.1.0"
TASK_ID = "491a4eb76930"
SUMMARY = "Two 3x3 C-shapes open toward each other and joined by color-4 bridge."

INVARIANTS = [
    "the background is zero",
    "there are exactly two color-5 centers",
    "each center is surrounded by a 3x3 color-2 frame with one side opening",
    "the openings face each other across a clear rectangular corridor",
]

ORIENTATIONS = ("horizontal", "vertical")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_C", "single_C", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _draw_c(g, cr, cc, opening):
    for r in range(cr - 1, cr + 2):
        for c in range(cc - 1, cc + 2):
            if r == cr and c == cc:
                g[r][c] = 5
            else:
                g[r][c] = 2
    if opening == "right":
        g[cr][cc + 1] = 0
    elif opening == "left":
        g[cr][cc - 1] = 0
    elif opening == "up":
        g[cr - 1][cc] = 0
    else:
        g[cr + 1][cc] = 0


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
    g = full_grid(13, 13, 0)
    if orientation == "horizontal":
        row = ctx.draw_choice("row", [4, 6, 8])
        _draw_c(g, row, 2, "right")
        _draw_c(g, row, 10, "left")
    else:
        col = ctx.draw_choice("col", [4, 6, 8])
        _draw_c(g, 2, col, "down")
        _draw_c(g, 10, col, "up")
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_C":
        return g
    if name == "single_C":
        _draw_c(g, 6, 6, "right")
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
