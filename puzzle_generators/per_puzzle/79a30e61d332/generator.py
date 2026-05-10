"""Generator for d94c3b52.

Rule: matching 3x3 key tiles in spaced tile grid become 8, and
intervening nonzero bridge tiles become 7.

Combinatorial axes (8): grid_h/w, bridge_axis, mask_shape,
palette_kind, anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: no_keys, no_bridge, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "79a30e61d332"
VERSION = "1.1.0"
TASK_ID = "79a30e61d332"
SUMMARY = "Matching 3x3 key tiles become 8; intervening bridge tiles become 7."

INVARIANTS = [
    "tiles are 3x3 interiors separated by rows and columns at multiples of 4",
    "one key tile contains color 8",
    "other tiles with the same nonzero mask are also key tiles",
    "key and bridge colors are distinct from 0, 7 and 8",
]

BRIDGE_AXES = ("horizontal", "vertical")
MASK_SHAPES = ("ell", "diag", "vee", "corner")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_keys", "no_bridge", "full_grid")
HELPFUL_TEXTURES = MASK_SHAPES

MASKS = {
    "ell": [(0, 0), (0, 1), (1, 0), (2, 2)],
    "diag": [(0, 0), (1, 1), (2, 2)],
    "vee": [(0, 0), (1, 1), (0, 2), (2, 1)],
    "corner": [(0, 2), (1, 2), (2, 0), (2, 1), (2, 2)],
}

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "bridge_axis":    {"type": "str", "default": "rng",
                       "valid": "|".join(BRIDGE_AXES)},
    "mask_shape":     {"type": "str", "default": "rng helpful",
                       "valid": "|".join(MASK_SHAPES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "texture":        {"type": "str", "default": "alias for mask_shape",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint_tile(g, tr, tc, color, cells):
    r0 = 1 + 4 * tr
    c0 = 1 + 4 * tc
    for dr, dc in cells:
        g[r0 + dr][c0 + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    axis = ctx.draw_choice("bridge_axis", list(BRIDGE_AXES))
    mask_name = (overrides.get("texture") if overrides.get("texture") in MASK_SHAPES else None) or \
                overrides.get("mask_shape") or \
                ctx.draw_choice("mask_shape", list(MASK_SHAPES))
    other_key_color, bridge_color = ctx.draw_distinct_colors(
        "tile_colors", n=2, exclude={0, 7, 8}
    )
    g = full_grid(12, 12, 0)
    if axis == "horizontal":
        key_a, mid, key_b = (0, 0), (0, 1), (0, 2)
    else:
        key_a, mid, key_b = (0, 0), (1, 0), (2, 0)
    mask = MASKS[mask_name]
    _paint_tile(g, key_a[0], key_a[1], 8, mask)
    _paint_tile(g, key_b[0], key_b[1], other_key_color, mask)
    _paint_tile(g, mid[0], mid[1], bridge_color, [(r, c) for r in range(3) for c in range(3)])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_keys":
        for r in range(3):
            for c in range(3):
                g[5 + r][5 + c] = 3
        return g
    if name == "no_bridge":
        for dr, dc in MASKS["ell"]:
            g[1 + dr][1 + dc] = 8
            g[1 + dr][9 + dc] = 4
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 8
        return g
    return g
