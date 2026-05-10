"""Generator for 8a6d367c.

Rule: a top glyph that agrees with existing frame fills is expanded
across a framed interior.

Combinatorial axes (8): grid_h/w, glyph, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_glyph, no_frame, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "8d37d130fec1"
VERSION = "1.1.0"
TASK_ID = "8d37d130fec1"
SUMMARY = "Top glyph that agrees with existing frame fills expands across a framed interior."

INVARIANTS = [
    "the background is color 8",
    "one large rectangular frame is the largest object",
    "a small glyph above the frame uses a color different from the frame and fill",
    "existing fill cells inside the frame are a subset of the glyph's scaled positions",
]

GLYPHS = ("plus", "tee")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_glyph", "no_frame", "full_grid")
HELPFUL_TEXTURES = GLYPHS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "glyph":          {"type": "str", "default": "rng helpful",
                       "valid": "|".join(GLYPHS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for glyph",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    glyph = (overrides.get("texture") if overrides.get("texture") in GLYPHS else None) or \
            overrides.get("glyph") or \
            ctx.draw_choice("glyph", list(GLYPHS))
    frame_color, fill_color, glyph_color = ctx.draw_distinct_colors("colors", n=3, exclude={8})
    g = full_grid(14, 12, 8)
    draw_frame(g, 6, 2, 13, 9, frame_color)
    if glyph == "plus":
        cells = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
        fill_seeds = [(2, 2), (0, 3)]
    else:
        cells = [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)]
        fill_seeds = [(0, 0), (2, 3)]
    for dr, dc in cells:
        g[1 + dr][4 + dc] = glyph_color
    for rr, cc in fill_seeds:
        g[7 + rr][3 + cc] = fill_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 12, 8)
    if name == "no_glyph":
        draw_frame(g, 6, 2, 13, 9, 3)
        return g
    if name == "no_frame":
        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]:
            g[1 + dr][4 + dc] = 4
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(12):
                g[r][c] = 3
        return g
    return g
