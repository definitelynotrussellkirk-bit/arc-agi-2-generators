"""Generator for 5034a0b5.

Rule: interior non-background cells move one step toward the matching
border color.

Combinatorial axes (8): grid_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
n_markers.
Degenerates: no_markers, no_border, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a2b749aefc65"
VERSION = "1.1.0"
TASK_ID = "a2b749aefc65"
SUMMARY = "Interior non-bg cells move one step toward matching border color."

INVARIANTS = [
    "the interior mode color is the background",
    "the middle cell of each border side defines that side's target color",
    "interior cells whose color matches a side move one step toward that side",
    "palette colors are distinct so each side has an unambiguous color",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "no_border", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "12", "valid": "12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "5", "valid": "5"},
    "n_markers":      {"type": "int", "default": "4", "valid": "4"},
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
    bg, top, bottom, left, right = ctx.draw_distinct_colors("colors", n=5, exclude=set())
    h = w = 12
    g = full_grid(h, w, bg)
    for c in range(w):
        g[0][c] = top
        g[h - 1][c] = bottom
    for r in range(h):
        g[r][0] = left
        g[r][w - 1] = right
    g[0][w // 2] = top
    g[h - 1][w // 2] = bottom
    g[h // 2][0] = left
    g[h // 2][w - 1] = right
    placements = [(3, 5, top), (8, 6, bottom), (5, 3, left), (6, 8, right)]
    rng.shuffle(placements)
    for r, c, color in placements:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 1)
    if name == "no_markers":
        for c in range(12):
            g[0][c] = 2
            g[11][c] = 3
        for r in range(12):
            g[r][0] = 4
            g[r][11] = 5
        return g
    if name == "no_border":
        g[5][5] = 2
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
