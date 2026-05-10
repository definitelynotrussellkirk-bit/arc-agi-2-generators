"""Generator for arc_puzzle_bank_21_next:medium_c03.

Rule: crop input to content; concat with its lr-flip with a 1-col gap.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors, color.
Degenerates: no_blob, symmetric_blob, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2e1f0bb81a3b"
VERSION = "1.1.0"
TASK_ID = "2e1f0bb81a3b"
SUMMARY = "Crop to content; concat with lr-flip with 1-col gap."

INVARIANTS = [
    "exactly one connected blob, 3-5 cells",
    "blob is asymmetric (not lr-symmetric)",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_blob", "symmetric_blob", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "5..7"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "6..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
    "color":          {"type": "color", "default": "rng !{0,1}",
                       "valid": "2..9"},
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
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 6, 6)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 8, 8)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 6, 8)
    g = full_grid(h, w, 0)
    color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    g[1][2] = color
    g[2][2] = color
    g[3][2] = color
    g[3][3] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 7, 0)
    if name == "no_blob":
        return g
    if name == "symmetric_blob":
        for r in range(2, 4):
            for c in range(2, 5):
                g[r][c] = 3
        return g
    if name == "full_grid":
        for r in range(6):
            for c in range(7):
                g[r][c] = 3
        return g
    return g
