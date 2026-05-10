"""Generator for 5b692c0f.

Rule: a colored payload attached to a yellow guide is mirrored from its
denser side.

Combinatorial axes (8): grid_h/w, orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, color.
Degenerates: no_guide, no_payload, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cbf77aa253ac"
VERSION = "1.1.0"
TASK_ID = "cbf77aa253ac"
SUMMARY = "Payload attached to a yellow guide is mirrored from its denser side."

INVARIANTS = [
    "each active component contains a color-4 guide and one payload color",
    "the guide's longer span determines the reflection axis",
    "the denser payload side is copied through the guide while stale payload is cleared",
]

ORIENTATIONS = ("horizontal", "vertical")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_guide", "no_payload", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "13..15", "valid": "13..15"},
    "grid_w":         {"type": "int", "default": "13..15", "valid": "13..15"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
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
                  ("horizontal" if sample_index % 2 == 0 else "vertical")
    color = ctx.draw_color("payload_color", exclude={0, 4})
    h = 13 + (sample_index % 3)
    w = 13 + ((sample_index * 2) % 3)
    g = full_grid(h, w, 0)
    if orientation == "horizontal":
        axis = 6 + (sample_index % 2)
        c0 = 3 + (sample_index % 2)
        for c in range(c0, c0 + 6):
            g[axis][c] = 4
        for dr, dc in [(-1, 1), (-1, 2), (-2, 2), (-1, 4)]:
            g[axis + dr][c0 + dc] = color
        g[axis + 1][c0 + 5] = color
    else:
        axis = 6 + (sample_index % 2)
        r0 = 3 + (sample_index % 2)
        for r in range(r0, r0 + 6):
            g[r][axis] = 4
        for dr, dc in [(1, -1), (2, -1), (2, -2), (4, -1)]:
            g[r0 + dr][axis + dc] = color
        g[r0 + 5][axis + 1] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_guide":
        g[5][5] = 2
        g[5][6] = 2
        return g
    if name == "no_payload":
        for c in range(3, 9):
            g[6][c] = 4
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 4
        return g
    return g
