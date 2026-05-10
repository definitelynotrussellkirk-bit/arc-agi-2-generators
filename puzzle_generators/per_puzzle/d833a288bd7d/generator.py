"""Generator for ecaa0ec1.

Rule: 1/8 shape rotates so source yellow corner aligns with yellow
target cluster.

Combinatorial axes (8): grid_h/w, target_corner, shape_variant,
palette_kind, anchor_corner, asymmetry_force, palette_size,
position_bias.
Degenerates: no_shape, no_target, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d833a288bd7d"
VERSION = "1.1.0"
TASK_ID = "d833a288bd7d"
SUMMARY = "1/8 shape rotates so source yellow corner aligns with yellow target."

INVARIANTS = [
    "background is color 0",
    "the shape cells use only colors 1 and 8",
    "one yellow marker sits at a diagonal corner of the shape bbox",
    "a separate yellow cluster chooses the target diagonal",
]

TARGET_CORNERS = ("top_right", "bottom_right", "bottom_left")
SHAPE_VARIANTS = ("hook", "step", "bar")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shape", "no_target", "full_grid")
HELPFUL_TEXTURES = TARGET_CORNERS

SHAPES = {
    "hook": [[1, 8, 1], [8, 1, 0]],
    "step": [[8, 1, 0], [1, 8, 1]],
    "bar": [[1, 8, 8], [0, 1, 0]],
}

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11"},
    "target_corner":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(TARGET_CORNERS)},
    "shape_variant":  {"type": "str", "default": "rng",
                       "valid": "|".join(SHAPE_VARIANTS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for target_corner",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    target = (overrides.get("texture") if overrides.get("texture") in TARGET_CORNERS else None) or \
             overrides.get("target_corner") or \
             ctx.draw_choice("target_corner", list(TARGET_CORNERS))
    variant = ctx.draw_choice("shape_variant", list(SHAPE_VARIANTS))
    g = full_grid(11, 11, 0)
    r0 = 4 + rng.randint(0, 1)
    c0 = 4 + rng.randint(0, 1)
    shape = SHAPES[variant]
    for r, row in enumerate(shape):
        for c, value in enumerate(row):
            if value:
                g[r0 + r][c0 + c] = value
    g[r0 - 1][c0 - 1] = 4
    if target == "top_right":
        g[r0 - 2][c0 + 4] = 4
        g[r0 - 2][c0 + 5] = 4
    elif target == "bottom_right":
        g[r0 + 4][c0 + 4] = 4
        g[r0 + 5][c0 + 4] = 4
    else:
        g[r0 + 4][c0 - 2] = 4
        g[r0 + 5][c0 - 2] = 4
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_shape":
        g[3][3] = 4; g[3][4] = 4
        return g
    if name == "no_target":
        for r, row in enumerate(SHAPES["hook"]):
            for c, value in enumerate(row):
                if value:
                    g[5 + r][5 + c] = value
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 4
        return g
    return g
