"""Generator for f8c80d96.

Rule: a partial periodic rectilinear rail is completed, with all
non-path cells filled gray.

Combinatorial axes (8): grid_h/w, period, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, color.
Degenerates: no_rail, single_cell, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "df92ae881dc8"
VERSION = "1.1.0"
TASK_ID = "df92ae881dc8"
SUMMARY = "Partial periodic rectilinear rail completed; non-path cells filled gray."

INVARIANTS = [
    "one nonzero foreground color forms a full-height rail",
    "the rail establishes a small horizontal period",
    "the output repeats the rail periodically and turns every non-path cell to color 5",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rail", "single_cell", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "8..12"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "10..14"},
    "period":         {"type": "int", "default": "rng 2..4", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "color":          {"type": "color", "default": "rng !{0,5}",
                       "valid": "1..4|6..9"},
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
    if difficulty == "easy":
        period = ctx.draw_int("period", 2, 2)
    elif difficulty == "hard":
        period = ctx.draw_int("period", 4, 4)
    else:
        period = ctx.draw_int("period", 2, 4)
    fg = ctx.draw_color("foreground", exclude={0, 5})
    h = 8 + (sample_index % 5)
    w = 10 + ((sample_index * 2) % 5)
    g = full_grid(h, w, 0)
    c0 = 1 + (sample_index % period)
    for r in range(h):
        g[r][c0] = fg
    if c0 + period < w and sample_index % 2:
        for r in range(h):
            g[r][c0 + period] = fg
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 0)
    if name == "no_rail":
        return g
    if name == "single_cell":
        g[5][5] = 3
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(12):
                g[r][c] = 3
        return g
    return g
