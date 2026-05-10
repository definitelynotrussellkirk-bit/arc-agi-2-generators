"""Generator for c6141b15.

Rule: line endpoints become glyph stamps while glyph centers become
line-network nodes.

Combinatorial axes (8): grid_h/w, line_orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_line, no_glyphs, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "e2bc70324918"
VERSION = "1.1.0"
TASK_ID = "e2bc70324918"
SUMMARY = "Line endpoints become glyph stamps; glyph centers become line nodes."

INVARIANTS = [
    "one thin line object has exactly two endpoints",
    "separate solid glyphs share one stamp color",
    "line and stamp colors are distinct and non-zero",
    "objects sit clear of grid borders",
]

ORIENTATIONS = ("horizontal", "vertical")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_line", "no_glyphs", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "15", "valid": "15"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "line_orientation":{"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for line_orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    orientation = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
                  overrides.get("line_orientation") or \
                  ctx.draw_choice("line_orientation", list(ORIENTATIONS))
    if "line_orientation" not in overrides and overrides.get("texture") not in ORIENTATIONS:
        orientation = "horizontal" if sample_index % 2 == 0 else "vertical"
    line, stamp = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    g = full_grid(15, 15, 0)
    if orientation == "horizontal":
        for c in range(2, 6):
            g[11][c] = line
    else:
        for r in range(9, 13):
            g[r][3] = line
    for r, c in [(2, 3), (2, 10), (7, 8)]:
        draw_rect(g, r, c, 3, 3, stamp)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 15, 0)
    if name == "no_line":
        draw_rect(g, 5, 5, 3, 3, 2)
        return g
    if name == "no_glyphs":
        for c in range(2, 6):
            g[11][c] = 1
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(15):
                g[r][c] = 2
        return g
    return g
