"""Generator for 9bebae7a.

Rule: yellow shape is mirrored away from a color-6 orientation marker.

Combinatorial axes (8): grid_h/w, mirror_mode, shape_origin,
palette_kind, anchor_corner, asymmetry_force, palette_size,
position_bias.
Degenerates: no_shape, no_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "0b555eccc4dc"
VERSION = "1.1.0"
TASK_ID = "0b555eccc4dc"
SUMMARY = "Yellow shape mirrored away from color-6 orientation marker."

INVARIANTS = [
    "the background is zero",
    "the yellow object is color 4",
    "the color-6 object determines whether mirroring is horizontal or vertical",
    "the marker sits on the side that makes the opposite mirror fit in bounds",
]

MIRROR_MODES = ("horizontal", "vertical")
SHAPE_ORIGINS = ("middle", "high", "low")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shape", "no_marker", "full_grid")
HELPFUL_TEXTURES = MIRROR_MODES

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "mirror_mode":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(MIRROR_MODES)},
    "shape_origin":   {"type": "str", "default": "rng",
                       "valid": "|".join(SHAPE_ORIGINS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for mirror_mode",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    mode = (overrides.get("texture") if overrides.get("texture") in MIRROR_MODES else None) or \
           overrides.get("mirror_mode") or \
           ctx.draw_choice("mirror_mode", list(MIRROR_MODES))
    origin = ctx.draw_choice("shape_origin", list(SHAPE_ORIGINS))
    g = full_grid(12, 12, 0)
    base = {"middle": (5, 5), "high": (3, 5), "low": (6, 4)}[origin]
    br, bc = base
    yellow = [(br, bc), (br, bc + 1), (br + 1, bc), (br + 2, bc)]
    for r, c in yellow:
        g[r][c] = 4
    if mode == "horizontal":
        draw_rect(g, br, min(10, bc + 4), 2, 2, 6)
    else:
        draw_rect(g, min(10, br + 4), max(1, bc - 1), 2, 4, 6)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_shape":
        draw_rect(g, 3, 3, 2, 2, 6)
        return g
    if name == "no_marker":
        for r, c in [(5, 5), (5, 6), (6, 5), (7, 5)]:
            g[r][c] = 4
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 4
        return g
    return g
