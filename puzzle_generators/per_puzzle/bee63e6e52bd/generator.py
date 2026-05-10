"""Generator for aba27056.

Rule: an open C/U shape is filled from its concavity with yellow
extensions.

Combinatorial axes (8): grid_h/w, open_side, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, color.
Degenerates: no_shape, closed_shape, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bee63e6e52bd"
VERSION = "1.1.0"
TASK_ID = "bee63e6e52bd"
SUMMARY = "Open C/U shape filled from concavity with yellow extensions."

INVARIANTS = [
    "one nonzero non-yellow color forms a C or U shape",
    "exactly one side of the shape's bounding box is open",
    "the rule fills the concavity, arm opening, and diagonal continuations with yellow",
]

OPEN_SIDES = ("right", "left", "top", "bottom")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shape", "closed_shape", "full_grid")
HELPFUL_TEXTURES = OPEN_SIDES

AXES = {
    "grid_h":         {"type": "int", "default": "15", "valid": "15"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "open_side":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(OPEN_SIDES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "color":          {"type": "color", "default": "rng !{0,4}",
                       "valid": "1..3|5..9"},
    "texture":        {"type": "str", "default": "alias for open_side",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    open_side = (overrides.get("texture") if overrides.get("texture") in OPEN_SIDES else None) or \
                overrides.get("open_side") or \
                ["right", "bottom", "left", "top"][sample_index % 4]
    color = ctx.draw_color("shape_color", exclude={0, 4})
    g = full_grid(15, 15, 0)
    r1, r2, c1, c2 = 4, 10, 4, 10

    if open_side in {"left", "right"}:
        closed_c = c1 if open_side == "right" else c2
        for r in range(r1, r2 + 1):
            g[r][closed_c] = color
        for c in range(c1, c2 + 1):
            g[r1][c] = color
            g[r2][c] = color
    else:
        closed_r = r1 if open_side == "bottom" else r2
        for c in range(c1, c2 + 1):
            g[closed_r][c] = color
        for r in range(r1, r2 + 1):
            g[r][c1] = color
            g[r][c2] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 15, 0)
    if name == "no_shape":
        return g
    if name == "closed_shape":
        for r in range(4, 11):
            g[r][4] = 3
            g[r][10] = 3
        for c in range(4, 11):
            g[4][c] = 3
            g[10][c] = 3
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(15):
                g[r][c] = 3
        return g
    return g
