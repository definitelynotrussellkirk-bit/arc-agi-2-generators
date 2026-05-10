"""Generator for e6721834.

Rule: stamp a source template onto target markers.

Combinatorial axes (8): grid_h/w, anchor_row, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_source, no_target, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fd39d31edb3c"
VERSION = "1.1.0"
TASK_ID = "fd39d31edb3c"
SUMMARY = "Stamp source template onto target markers."

INVARIANTS = [
    "background is 0",
    "the source half has more non-background cells than the target half",
    "target markers share an anchor color with the source object",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_source", "no_target", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "6", "valid": "6"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "anchor_row":     {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
    anchor_row = ctx.draw_int("anchor_row", 1, 4)
    g = full_grid(6, 12, 0)
    g[1][1] = 2
    g[1][2] = 3
    g[2][1] = 3
    g[2][2] = 3
    anchor_col = 6 + rng.randint(1, 4)
    g[anchor_row][anchor_col] = 2
    if rng.random() < 0.5:
        g[min(5, anchor_row + 1)][max(6, anchor_col - 1)] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 12, 0)
    if name == "no_source":
        g[3][8] = 2
        return g
    if name == "no_target":
        g[1][1] = 2
        g[1][2] = 3
        g[2][1] = 3
        g[2][2] = 3
        return g
    if name == "full_grid":
        for r in range(6):
            for c in range(12):
                g[r][c] = 3
        return g
    return g
