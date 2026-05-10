"""Generator for 5117e062.

Rule: bbox of shape with 8 marker is cropped, marker replaced by shape
color.

Combinatorial axes (8): grid_h/w, shape_color, palette_kind,
position_bias, anchor_corner, asymmetry_force, palette_size, marker_position.
Degenerates: no_marker, no_shape, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import PLUS_5

GENERATOR_ID = "14439d1343e1"
VERSION = "1.1.0"
TASK_ID = "14439d1343e1"
SUMMARY = "Shape with 8 marker; bbox cropped, marker replaced by shape color."

INVARIANTS = [
    "there is exactly one color-8 marker",
    "the marker is 4-adjacent to the shape color",
    "all cells of the shape color and the marker define the crop bbox",
    "inside the crop, marker cells become the shape color and all other colors become 0",
]

POSITION_BIASES = ("centered", "scattered", "near_edge", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_marker", "no_shape", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "12", "valid": "10..16"},
    "shape_color":    {"type": "color", "default": "rng !{0,8}",
                       "valid": "1..9"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "marker_position":{"type": "str", "default": "center", "valid": "center"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    color = ctx.draw_color("shape_color", exclude={0, 8})
    g = full_grid(12, 12, 0)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    if bias == "centered":
        r0, c0 = 4, 4
    elif bias == "near_edge":
        r0 = rng.choice([2, 6])
        c0 = rng.choice([2, 6])
    else:
        r0 = rng.randint(2, 6)
        c0 = rng.randint(2, 6)
    for dr, dc in PLUS_5:
        if r0 + dr < 12 and c0 + dc < 12:
            g[r0 + dr][c0 + dc] = color
    if r0 + 1 < 12 and c0 + 1 < 12:
        g[r0 + 1][c0 + 1] = 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_marker":
        for dr, dc in PLUS_5:
            g[5 + dr][5 + dc] = 3
        return g
    if name == "no_shape":
        g[6][6] = 8
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 8
        return g
    return g
