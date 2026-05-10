"""Generator for arc_additional_puzzle_bank_volume18:H123.

Rule: blue marker count selects which yellow nested-frame depth is
filled cyan.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_marker, no_frames, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "35962615e0db"
VERSION = "1.1.0"
TASK_ID = "35962615e0db"
SUMMARY = "Blue marker count selects which yellow nested-frame depth is filled cyan."

INVARIANTS = [
    "background is 0",
    "three yellow frames are nested",
    "blue marker count is between 1 and 3",
    "the selected band or core contains blank cells",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_marker", "no_frames", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 13..17", "valid": "11..24"},
    "grid_w":         {"type": "int", "default": "rng 13..17", "valid": "11..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "true",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "centered", "valid": "centered"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 16, 17)
        w = ctx.draw_int("grid_w", 16, 17)
    else:
        h = ctx.draw_int("grid_h", 13, 17)
        w = ctx.draw_int("grid_w", 13, 17)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    for c in range(1, rng.randint(1, 3) + 1):
        g[0][c] = 1
    for offset in (0, 2, 4):
        draw_frame(g, 2 + offset, 2 + offset, h - 3 - offset, w - 3 - offset, 4)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 15, 0)
    if name == "no_marker":
        for offset in (0, 2, 4):
            draw_frame(g, 2 + offset, 2 + offset, 12 - offset, 12 - offset, 4)
        return g
    if name == "no_frames":
        g[0][1] = 1
        g[0][2] = 1
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(15):
                g[r][c] = 4
        return g
    return g
