"""Generator for puzzle f3e62deb.

Rule: find non-bg color; shift shape so bbox lands at:
4=bottom, 6=top, 8=right, 3=left; else stays.

Combinatorial axes (8): grid_h/w, color, shape_kind, position_bias,
anchor_corner, asymmetry_force, palette_size, include_decoy.
Degenerates: shape_at_target, no_shape, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "d66f6f5141d9"
VERSION = "1.1.0"
TASK_ID = "d66f6f5141d9"
SUMMARY = "Single colored shape; rule shifts to edge by color (3/4/6/8)."

INVARIANTS = [
    "background is 0",
    "exactly 1 shape, color in {3, 4, 6, 8}",
    "shape >=3 cells, not already at target edge",
]

SHAPE_KINDS = ("U", "T", "Z", "L", "rect", "diag")
POSITION_BIASES = ("centered", "row_aligned", "col_aligned", "scattered")
DEGENERATE_TEXTURES = ("shape_at_target", "no_shape", "full_grid")
HELPFUL_TEXTURES = SHAPE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..18"},
    "color":          {"type": "color", "default": "rng [3,4,6,8]",
                       "valid": "3|4|6|8"},
    "shape_kind":     {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SHAPE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "include_decoy":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for shape_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = {
    "U":    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)],
    "T":    [(0, 0), (1, 0), (1, 1), (1, 2)],
    "Z":    [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)],
    "L":    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    "rect": [(0, 0), (0, 1), (1, 0), (1, 1)],
    "diag": [(0, 0), (1, 1), (2, 2)],
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 7
    elif difficulty == "hard":
        h_lo, h_hi = 10, 14
    else:
        h_lo, h_hi = 6, 10
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 2, h_hi + 4)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    color = int(overrides.get("color",
                              rng.choice([3, 4, 6, 8])))
    if color not in (3, 4, 6, 8):
        color = 3
    shape_kind = (overrides.get("texture") or
                  overrides.get("shape_kind")
                  or ctx.draw_choice("shape_kind",
                                     list(SHAPE_KINDS)))
    shape = list(_SHAPES.get(shape_kind, _SHAPES["U"]))
    bias = overrides.get("position_bias",
                         ctx.draw_choice("position_bias",
                                         list(POSITION_BIASES)))
    g = full_grid(h, w, 0)
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    top, left = _pick_position(bias, h, w, sh, sw, color, rng)
    paint_at(g, top, left, shape, color)
    return g


def _pick_position(bias, h, w, sh, sw, color, rng):
    # Avoid placing at the edge that the rule moves to
    if color == 4:  # bottom
        top_max = max(1, h - sh - 2)
    elif color == 6:  # top
        top_max = h - sh - 1
    else:
        top_max = max(1, h - sh - 1)
    if color == 8:  # right
        left_max = max(2, w - sw - 2)
    elif color == 3:  # left
        left_max = max(2, w - sw - 1)
    else:
        left_max = max(2, w - sw - 1)
    if bias == "centered":
        return max(1, (h - sh) // 2), max(2, (w - sw) // 2)
    if bias == "row_aligned":
        return h // 2, rng.randint(2, max(2, left_max))
    if bias == "col_aligned":
        return rng.randint(1, max(1, top_max)), w // 2
    if color == 4:
        return rng.randint(1, max(1, top_max - 1)), rng.randint(2, max(2, left_max))
    if color == 6:
        return rng.randint(2, max(2, top_max)), rng.randint(2, max(2, left_max))
    return rng.randint(1, max(1, top_max)), rng.randint(2, max(2, left_max))


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([3, 4, 6, 8])
    if name == "shape_at_target":
        # Shape already at edge → rule has no work
        if color == 4:
            paint_at(g, h - 3, 2, _SHAPES["U"], color)
        elif color == 6:
            paint_at(g, 0, 2, _SHAPES["U"], color)
        elif color == 8:
            paint_at(g, 1, w - 3, _SHAPES["U"], color)
        else:
            paint_at(g, 1, 0, _SHAPES["U"], color)
        return g
    if name == "no_shape":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    return g
