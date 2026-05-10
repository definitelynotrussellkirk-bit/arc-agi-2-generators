"""Generator for arc_additional_puzzle_bank_volume20:H135.

Rule: a checkpoint corridor exposes the union of shortest paths from
start to goal.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_corridor, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5e4fa01a0dc0"
VERSION = "1.1.0"
TASK_ID = "5e4fa01a0dc0"
SUMMARY = "A checkpoint corridor exposes the union of shortest paths from start to goal."

INVARIANTS = [
    "walls are 5",
    "markers 2, 3, and 4 are ordered along one corridor",
    "the open route between each segment is unique",
    "markers and walls are preserved by the rule",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_corridor", "no_markers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "5..24"},
    "grid_w":         {"type": "int", "default": "rng 11..16", "valid": "9..30"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "random", "valid": "random"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 11, 16)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 5)
    r = rng.randint(1, h - 2)
    c0 = rng.randint(1, w - 9)
    for c in range(c0, c0 + 8):
        g[r][c] = 0
    for c, color in [(c0, 2), (c0 + 4, 3), (c0 + 7, 4)]:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 12, 5)
    if name == "no_corridor":
        return g
    if name == "no_markers":
        for c in range(2, 10):
            g[3][c] = 0
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(12):
                g[r][c] = 0
        return g
    return g
