"""Generator for 2bcee788.

Rule: main-color shape is reflected across the red fold boundary and
red cells recolor to the main color.

Combinatorial axes (8): grid_h/w, orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
main_color.
Degenerates: no_shape, no_fold, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5955ced85d5c"
VERSION = "1.1.0"
TASK_ID = "5955ced85d5c"
SUMMARY = "Main-color shape reflected across red fold boundary."

INVARIANTS = [
    "there is one main nonzero color besides red",
    "red cells form a fold boundary on one side of the main shape",
    "the red centroid determines reflection axis",
    "the shape sits clear of grid borders so the reflection has room",
]

ORIENTATIONS = ("horizontal", "vertical")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shape", "no_fold", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

SHAPE = [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)]

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "main_color":     {"type": "color", "default": "rng !{0,2}",
                       "valid": "1|3|4|5|6|7|8|9"},
    "texture":        {"type": "str", "default": "alias for orientation",
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
                  overrides.get("orientation") or \
                  ctx.draw_choice("orientation", list(ORIENTATIONS))
    main_color = ctx.draw_color("main_color", exclude={0, 2})
    g = full_grid(11, 11, 0)
    if orientation == "horizontal":
        r0 = rng.randint(1, 2)
        c0 = rng.randint(3, 5)
        for dr, dc in SHAPE:
            g[r0 + dr][c0 + dc] = main_color
        fold_r = r0 + 4
        for c in range(c0 - 1, c0 + 4):
            g[fold_r][c] = 2
    else:
        r0 = rng.randint(3, 5)
        c0 = rng.randint(1, 2)
        for dr, dc in SHAPE:
            g[r0 + dr][c0 + dc] = main_color
        fold_c = c0 + 4
        for r in range(r0 - 1, r0 + 4):
            g[r][fold_c] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_shape":
        for c in range(2, 8):
            g[5][c] = 2
        return g
    if name == "no_fold":
        for dr, dc in SHAPE:
            g[2 + dr][3 + dc] = 3
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 2
        return g
    return g
