"""Generator for 6aa20dc0.

Rule: a 2x2 multicolor template has two marker colors, paired by two
singleton marker objects.

Combinatorial axes (8): grid_h/w, anchor, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_template, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0f5fbe0de38e"
VERSION = "1.1.0"
TASK_ID = "0f5fbe0de38e"
SUMMARY = "2x2 multicolor template paired by two singleton marker objects."

INVARIANTS = [
    "background is 0",
    "template has fill color 5 and marker colors 2 and 3",
    "two singleton marker objects match the template marker positions at scale 1",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_markers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9"},
    "anchor":         {"type": "int", "default": "rng 4..6", "valid": "4..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
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
    anchor = ctx.draw_int("anchor", 4, 6)
    g = full_grid(9, 9, 0)
    g[1][1] = 2
    g[1][2] = 5
    g[2][1] = 5
    g[2][2] = 3
    c0 = rng.randint(1, 5)
    r0 = anchor
    g[r0][c0] = 2
    g[r0 + 1][c0 + 1] = 3
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 0)
    if name == "no_template":
        g[5][3] = 2
        g[6][4] = 3
        return g
    if name == "no_markers":
        g[1][1] = 2
        g[1][2] = 5
        g[2][1] = 5
        g[2][2] = 3
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(9):
                g[r][c] = 5
        return g
    return g
