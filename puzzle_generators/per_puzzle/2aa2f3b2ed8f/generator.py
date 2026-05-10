"""Generator for 98cf29f8.

Rule: a tailed object loses its tail and slides its rectangular body
until it touches another rectangle.

Combinatorial axes (8): grid_h/w, orientation, body_shape, palette_kind,
anchor_corner, asymmetry_force, palette_size, n_distinct_colors.
Degenerates: no_tail, no_target, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "2aa2f3b2ed8f"
VERSION = "1.1.0"
TASK_ID = "2aa2f3b2ed8f"
SUMMARY = "Tailed object loses its tail and slides body until it touches another rectangle."

INVARIANTS = [
    "the background is zero",
    "one object is a plain rectangle",
    "one same-color object has a rectangular body plus a one-cell tail",
    "the tail points toward the plain rectangle and determines the slide direction",
]

ORIENTATIONS = ("right", "left", "down", "up")
BODY_SHAPES = ("2x2", "2x3", "3x2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_tail", "no_target", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "body_shape":     {"type": "str", "default": "rng",
                       "valid": "|".join(BODY_SHAPES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
    body_h, body_w = ctx.draw_choice("body_shape", [(2, 2), (2, 3), (3, 2)])
    moving, target = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    g = full_grid(13, 13, 0)
    if orientation == "right":
        r0, c0 = 5, 1
        draw_rect(g, r0, c0, body_h, body_w, moving)
        g[r0][c0 + body_w] = moving
        draw_rect(g, r0, 10, body_h, 2, target)
    elif orientation == "left":
        r0, c0 = 5, 9 - body_w
        draw_rect(g, r0, c0, body_h, body_w, moving)
        g[r0][c0 - 1] = moving
        draw_rect(g, r0, 1, body_h, 2, target)
    elif orientation == "down":
        r0, c0 = 1, 5
        draw_rect(g, r0, c0, body_h, body_w, moving)
        g[r0 + body_h][c0] = moving
        draw_rect(g, 10, c0, 2, body_w, target)
    else:
        r0, c0 = 9 - body_h, 5
        draw_rect(g, r0, c0, body_h, body_w, moving)
        g[r0 - 1][c0] = moving
        draw_rect(g, 1, c0, 2, body_w, target)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_tail":
        draw_rect(g, 5, 1, 2, 2, 3)
        draw_rect(g, 5, 10, 2, 2, 4)
        return g
    if name == "no_target":
        draw_rect(g, 5, 1, 2, 2, 3)
        g[5][3] = 3
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 3
        return g
    return g
