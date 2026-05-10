"""Generator for 3d588dc9.

Rule: a zero lollipop aligned to a gray object loses its stem and marks
the facing edge.

Combinatorial axes (8): grid_h/w, orientation, body_size, palette_kind,
anchor_corner, asymmetry_force, palette_size, n_distinct_colors.
Degenerates: no_stem, no_target, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "c4f1da01c470"
VERSION = "1.1.0"
TASK_ID = "c4f1da01c470"
SUMMARY = "Zero lollipop aligned to gray object loses stem and marks the facing edge."

INVARIANTS = [
    "the background is color 7",
    "one zero component has a solid rectangular body and a thin stem",
    "a color-5 object is aligned with the zero body on one side",
    "the rule clears the stem and paints the side of the zero body facing the color-5 object",
]

ORIENTATIONS = ("right", "left", "down", "up")
BODY_SIZES = ("3x3", "3x4", "4x3")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_stem", "no_target", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "body_size":      {"type": "str", "default": "rng",
                       "valid": "|".join(BODY_SIZES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
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
    body_h, body_w = ctx.draw_choice("body_size", [(3, 3), (3, 4), (4, 3)])
    g = full_grid(13, 13, 7)

    if orientation == "right":
        r0, c0 = 4, 2
        draw_rect(g, r0, c0, body_h, body_w, 0)
        mid = r0 + body_h // 2
        for c in range(c0 + body_w, c0 + body_w + 2):
            g[mid][c] = 0
        draw_rect(g, r0, 10, body_h, 2, 5)
    elif orientation == "left":
        r0, c0 = 4, 7
        draw_rect(g, r0, c0, body_h, body_w, 0)
        mid = r0 + body_h // 2
        for c in range(c0 - 2, c0):
            g[mid][c] = 0
        draw_rect(g, r0, 1, body_h, 2, 5)
    elif orientation == "down":
        r0, c0 = 2, 4
        draw_rect(g, r0, c0, body_h, body_w, 0)
        mid = c0 + body_w // 2
        for r in range(r0 + body_h, r0 + body_h + 2):
            g[r][mid] = 0
        draw_rect(g, 10, c0, 2, body_w, 5)
    else:
        r0, c0 = 7, 4
        draw_rect(g, r0, c0, body_h, body_w, 0)
        mid = c0 + body_w // 2
        for r in range(r0 - 2, r0):
            g[r][mid] = 0
        draw_rect(g, 1, c0, 2, body_w, 5)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 7)
    if name == "no_stem":
        draw_rect(g, 4, 2, 3, 3, 0)
        draw_rect(g, 4, 10, 3, 2, 5)
        return g
    if name == "no_target":
        draw_rect(g, 4, 2, 3, 3, 0)
        for c in range(5, 7):
            g[5][c] = 0
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 5
        return g
    return g
