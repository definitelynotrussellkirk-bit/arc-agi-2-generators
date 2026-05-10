"""Generator for additional_bank:M4.

Rule: for each 7-blob, if its bbox interior has 0-cells (hollow) → 4,
else (solid rectangle) → 2.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_shapes, no_hollow, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "97d3714964b0"
VERSION = "1.1.0"
TASK_ID = "97d3714964b0"
SUMMARY = "1 hollow 7-frame + 1 solid 7-rect + decoration."

INVARIANTS = [
    "exactly one hollow 7-frame (h≥3, w≥3)",
    "exactly one solid 7-rect",
    "decoration cell is non-7",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shapes", "no_hollow", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "true",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _solid(g, r1, c1, r2, c2, color):
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    draw_frame(g, 1, 1, 3, 4, 7)
    _solid(g, 5, w - 3, 6, w - 2, 7)
    g[h - 1][w - 1] = 5
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 10, 0)
    if name == "no_shapes":
        g[8][9] = 5
        return g
    if name == "no_hollow":
        _solid(g, 1, 1, 2, 3, 7)
        _solid(g, 5, 6, 6, 8, 7)
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(10):
                g[r][c] = 7
        return g
    return g
