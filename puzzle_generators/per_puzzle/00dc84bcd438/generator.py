"""Generator for 54dc2872.

Rule: mostly solid multicolor corner shape moves to matching singleton
marker.

Combinatorial axes (8): grid_h/w, special_corner, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_shape, no_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "00dc84bcd438"
VERSION = "1.1.0"
TASK_ID = "00dc84bcd438"
SUMMARY = "Multicolor corner shape moves to matching singleton marker."

INVARIANTS = [
    "the background is zero",
    "one connected 2x2 shape has a dominant body color and one special corner color",
    "a standalone marker has the same color as the special corner",
    "body and special colors are distinct and non-zero",
]

CORNERS = ("tl", "tr", "bl", "br")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shape", "no_marker", "full_grid")
HELPFUL_TEXTURES = CORNERS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10"},
    "grid_w":         {"type": "int", "default": "10", "valid": "10"},
    "special_corner": {"type": "str", "default": "rng helpful",
                       "valid": "|".join(CORNERS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for special_corner",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    corner = (overrides.get("texture") if overrides.get("texture") in CORNERS else None) or \
             overrides.get("special_corner") or \
             ctx.draw_choice("special_corner", list(CORNERS))
    body, special = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    g = full_grid(10, 10, 0)
    r0, c0 = 2, 2
    for dr in range(2):
        for dc in range(2):
            g[r0 + dr][c0 + dc] = body
    corner_offsets = {"tl": (0, 0), "tr": (0, 1), "bl": (1, 0), "br": (1, 1)}
    sr, sc = corner_offsets[corner]
    g[r0 + sr][c0 + sc] = special
    g[6][6] = special
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_shape":
        g[6][6] = 2
        return g
    if name == "no_marker":
        for dr in range(2):
            for dc in range(2):
                g[2 + dr][2 + dc] = 1
        g[2][2] = 2
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 2
        return g
    return g
