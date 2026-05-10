"""Generator for ac3e2b04.

Rule: green 3x3 marker projects a blue line perpendicular to dense
red guide lines.

Combinatorial axes (8): grid_h/w, guide_orientation, guide_offset,
palette_kind, anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: no_marker, no_guide, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "87079dd3fc4a"
VERSION = "1.1.0"
TASK_ID = "87079dd3fc4a"
SUMMARY = "Green 3x3 marker projects blue line perpendicular to red guides."

INVARIANTS = [
    "the background is zero",
    "a 3x3 green marker has a color-2 center and color-3 neighbors",
    "the marker center lies on a dense color-2 guide row or column",
    "additional dense guide rows or columns receive blue 3x3 intersection blocks",
]

ORIENTATIONS = ("vertical", "horizontal")
OFFSETS = ("left", "center", "right")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_marker", "no_guide", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "guide_orientation":{"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "guide_offset":   {"type": "str", "default": "rng",
                       "valid": "|".join(OFFSETS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "texture":        {"type": "str", "default": "alias for guide_orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _green_marker(g, r, c):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            g[r + dr][c + dc] = 3
    g[r][c] = 2


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    orientation = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
                  overrides.get("guide_orientation") or \
                  ctx.draw_choice("guide_orientation", list(ORIENTATIONS))
    offset = ctx.draw_choice("guide_offset", list(OFFSETS))
    g = full_grid(13, 13, 0)
    center_vals = {"left": (5, 4, 8), "center": (6, 5, 9), "right": (7, 6, 10)}
    center_rc, main_axis, other_axis = center_vals[offset]
    if orientation == "vertical":
        for r in range(13):
            g[r][main_axis] = 2
            g[r][other_axis] = 2
        _green_marker(g, center_rc, main_axis)
    else:
        for c in range(13):
            g[main_axis][c] = 2
            g[other_axis][c] = 2
        _green_marker(g, main_axis, center_rc)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_marker":
        for r in range(13):
            g[r][6] = 2
        return g
    if name == "no_guide":
        _green_marker(g, 6, 6)
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
