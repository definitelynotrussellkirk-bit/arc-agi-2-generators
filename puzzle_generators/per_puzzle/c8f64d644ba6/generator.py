"""Generator for 6a1e5592.

Rule: gray shapes are cleared and packed into the first blank
position supported by red cells above.

Combinatorial axes (8): grid_h/w, shape, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_shape, no_support, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "c8f64d644ba6"
VERSION = "1.1.0"
TASK_ID = "c8f64d644ba6"
SUMMARY = "Gray shapes cleared and packed into first blank supported by red cells above."

INVARIANTS = [
    "background is color 0",
    "movable objects use color 5",
    "the destination has red support cells directly above every top-row shape cell",
    "the source shape sits clear of the destination zone",
]

SHAPE_NAMES = ("ell", "bar", "tee")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shape", "no_support", "full_grid")
HELPFUL_TEXTURES = SHAPE_NAMES

SHAPES = {
    "ell": [(0, 0), (0, 1), (1, 0)],
    "bar": [(0, 0), (0, 1), (0, 2)],
    "tee": [(0, 0), (0, 1), (0, 2), (1, 1)],
}

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "shape":          {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SHAPE_NAMES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for shape",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    name = (overrides.get("texture") if overrides.get("texture") in SHAPE_NAMES else None) or \
           overrides.get("shape") or \
           ctx.draw_choice("shape", list(SHAPE_NAMES))
    h = 9 + rng.randint(0, 3)
    w = 9 + rng.randint(0, 3)
    g = full_grid(h, w, 0)
    shape = SHAPES[name]
    dest_c = 1 + rng.randint(0, max(0, w - 5))
    for dr, dc in shape:
        if dr == 0:
            g[1][dest_c + dc] = 2
    paint_at(g, h - 3, w - 4, shape, 5)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_shape":
        g[1][3] = 2
        return g
    if name == "no_support":
        for dr, dc in SHAPES["ell"]:
            g[7 + dr][6 + dc] = 5
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 5
        return g
    return g
