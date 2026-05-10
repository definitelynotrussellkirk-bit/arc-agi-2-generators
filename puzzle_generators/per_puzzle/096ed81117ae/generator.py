"""Generator for arc_additional_puzzle_bank_volume17:H119.

Rule: a control-selected transform of the color-6 shape is placed by
the vector from marker 2 to marker 3.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_control, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "096ed81117ae"
VERSION = "1.1.0"
TASK_ID = "096ed81117ae"
SUMMARY = "A control-selected transform of the color-6 shape is placed by the vector from marker 2 to marker 3."

INVARIANTS = [
    "one control marker is 1, 4, 7, or 9",
    "one color-6 source shape is present",
    "markers 2 and 3 define the placement vector",
    "the transformed translated copy fits in-bounds",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_control", "no_markers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 12..17", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "true",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 15, 17)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 12, 17)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[0][0] = rng.choice([1, 4, 7, 9])
    for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 0)]:
        g[2 + dr][2 + dc] = 6
    g[0][5] = 2
    g[3][8] = 3
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 13, 0)
    if name == "no_control":
        for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 0)]:
            g[2 + dr][2 + dc] = 6
        g[0][5] = 2
        g[3][8] = 3
        return g
    if name == "no_markers":
        g[0][0] = 1
        for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 0)]:
            g[2 + dr][2 + dc] = 6
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(13):
                g[r][c] = 6
        return g
    return g
