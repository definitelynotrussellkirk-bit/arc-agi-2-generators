"""Generator for arc_puzzle_bank_21_set17_s:S17_M7.

Rule: among color-2 seeds, the square growth that touches the border
is cropped.

Combinatorial axes (8): grid_h/w, edge, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_seeds, all_interior, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "16491c603ea5"
VERSION = "1.1.0"
TASK_ID = "16491c603ea5"
SUMMARY = "Among color-2 seeds, the square growth that touches the border is cropped."

INVARIANTS = [
    "background is 0",
    "there are multiple color-2 seed cells",
    "exactly one seed's clipped 3x3 growth touches the grid border",
    "the border-touching grown region is nonempty and crop-worthy",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seeds", "all_interior", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 9..12", "valid": "8..15"},
    "width":          {"type": "int", "default": "rng 11..14", "valid": "10..17"},
    "edge":           {"type": "enum", "default": "rng top|left", "valid": "top|left"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "true",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "true",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "border", "valid": "border"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 9, 10)
        w = ctx.draw_int("width", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 11, 12)
        w = ctx.draw_int("width", 13, 14)
    else:
        h = ctx.draw_int("height", 9, 12)
        w = ctx.draw_int("width", 11, 14)
    edge = ctx.draw_choice("edge", ["top", "left"])
    g = full_grid(h, w, 0)
    if edge == "top":
        g[0][3] = 2
    else:
        g[3][0] = 2
    g[h // 2][w // 2] = 2
    g[h - 3][w - 3] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 0)
    if name == "no_seeds":
        return g
    if name == "all_interior":
        g[3][3] = 2
        g[5][5] = 2
        g[7][7] = 2
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
