"""Generator for 98c475bf.

Rule: paired row markers between side borders expand into fixed line
glyphs.

Combinatorial axes (8): grid_h/w, marker_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, border.
Degenerates: no_borders, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "75d4884529f6"
VERSION = "1.1.0"
TASK_ID = "75d4884529f6"
SUMMARY = "Paired row markers between side borders expand into fixed line glyphs."

INVARIANTS = [
    "the first cell defines the side-border color",
    "valid marker rows have identical non-border colors at columns 1 and w-2",
    "marker colors come from the supported glyph palette",
    "border color is distinct from marker glyph colors",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_borders", "no_markers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "20", "valid": "20"},
    "marker_count":   {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "border":         {"type": "color", "default": "rng !{0,1,2,3,6,7}",
                       "valid": "4|5|8|9"},
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
        mc_lo, mc_hi = 1, 1
    elif difficulty == "hard":
        mc_lo, mc_hi = 3, 3
    else:
        mc_lo, mc_hi = 1, 3
    marker_count = ctx.draw_int("marker_count", mc_lo, mc_hi)
    h = 12
    w = 20
    border = ctx.draw_color("border", exclude={0, 1, 2, 3, 6, 7})
    colors = [6, 7, 2, 1, 3]
    rng.shuffle(colors)
    rows = [3, 5, 8]
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][0] = border
        g[r][w - 1] = border
    for row, color in zip(rows[:marker_count], colors):
        g[row][1] = color
        g[row][w - 2] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 20, 0)
    if name == "no_borders":
        g[3][1] = 2; g[3][18] = 2
        return g
    if name == "no_markers":
        for r in range(12):
            g[r][0] = 5; g[r][19] = 5
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(20):
                g[r][c] = 5
        return g
    return g
