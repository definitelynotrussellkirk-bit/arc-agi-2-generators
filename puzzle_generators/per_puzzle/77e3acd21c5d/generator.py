"""Generator for 57edb29d.

Rule: marker positions from a wide source rectangle are anchored into a
marker-free rectangle.

Combinatorial axes (8): grid_h/w, empty_size, marker_layout, palette_kind,
anchor_corner, asymmetry_force, palette_size, n_distinct_colors.
Degenerates: no_source, no_empty, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "77e3acd21c5d"
VERSION = "1.1.0"
TASK_ID = "77e3acd21c5d"
SUMMARY = "Marker positions from wide source rectangle anchored into marker-free rectangle."

INVARIANTS = [
    "the background is zero",
    "one solid rectangle has a single color and supplies the output size",
    "one wider rectangle has a dominant fill color and a few same-color markers",
    "marker offsets are interpreted by nearest source corners and transferred to the empty rectangle",
]

EMPTY_SIZES = ("e5x6", "e6x5", "e6x7")
LAYOUTS = ("corners", "edge", "mixed")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_source", "no_empty", "full_grid")
HELPFUL_TEXTURES = LAYOUTS

AXES = {
    "grid_h":         {"type": "int", "default": "18", "valid": "18"},
    "grid_w":         {"type": "int", "default": "18", "valid": "18"},
    "empty_size":     {"type": "str", "default": "rng",
                       "valid": "5x6|6x5|6x7"},
    "marker_layout":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(LAYOUTS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for marker_layout",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    eh, ew = ctx.draw_choice("empty_size", [(5, 6), (6, 5), (6, 7)])
    layout = (overrides.get("texture") if overrides.get("texture") in LAYOUTS else None) or \
             overrides.get("marker_layout") or \
             ctx.draw_choice("marker_layout", list(LAYOUTS))
    empty_color, body_color, marker_color = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    g = full_grid(18, 18, 0)
    draw_rect(g, 1, 1, eh, ew, empty_color)
    sh, sw = 5, 9
    sr, sc = 10, 4
    draw_rect(g, sr, sc, sh, sw, body_color)
    marker_sets = {
        "corners": [(0, 1), (1, sw - 2), (sh - 2, 1)],
        "edge": [(1, 2), (1, sw - 3), (sh - 2, sw // 2)],
        "mixed": [(0, sw // 2), (sh // 2, 1), (sh - 1, sw - 2)],
    }
    for dr, dc in marker_sets[layout]:
        g[sr + dr][sc + dc] = marker_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(18, 18, 0)
    if name == "no_source":
        draw_rect(g, 1, 1, 5, 6, 3)
        return g
    if name == "no_empty":
        draw_rect(g, 10, 4, 5, 9, 4)
        return g
    if name == "full_grid":
        for r in range(18):
            for c in range(18):
                g[r][c] = 4
        return g
    return g
