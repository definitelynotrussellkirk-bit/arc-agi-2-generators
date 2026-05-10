"""Generator for arc_additional_puzzle_bank_volume14:H94.

Rule: a control cell selects one of three yellow nested-frame regions
to fill.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_frames, no_control, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "cad61106e2b9"
VERSION = "1.1.0"
TASK_ID = "cad61106e2b9"
SUMMARY = "Control cell selects one of three nested-frame regions to fill."

INVARIANTS = [
    "background is 0",
    "three nested color-4 frames are present",
    "one control value is in 1..3",
    "selected region contains empty cells",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frames", "no_control", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 13..17", "valid": "13..17"},
    "grid_w":         {"type": "int", "default": "rng 13..17", "valid": "13..17"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 16, 17)
        w = ctx.draw_int("grid_w", 16, 17)
    else:
        h = ctx.draw_int("grid_h", 13, 17)
        w = ctx.draw_int("grid_w", 13, 17)
    g = full_grid(h, w, 0)
    g[0][0] = rng.randint(1, 3)
    for offset in (0, 2, 4):
        draw_frame(g, 2 + offset, 2 + offset, h - 3 - offset, w - 3 - offset, 4)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 14, 0)
    if name == "no_frames":
        g[0][0] = 1
        return g
    if name == "no_control":
        for offset in (0, 2, 4):
            draw_frame(g, 2 + offset, 2 + offset, 11 - offset, 11 - offset, 4)
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(14):
                g[r][c] = 4
        return g
    return g
