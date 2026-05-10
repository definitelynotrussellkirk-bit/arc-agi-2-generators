"""Generator for additional_scaffolded:M4 — 7-marker shoots a 3-line into a 5-frame.

Rule: a 5-color rectangle frame has a 7-marker in the cell adjacent to
its outer edge. The interior cells along that 7's row (if 7 is left or
right) or column (if 7 is above or below) get painted with 3.

Combinatorial axes (8): grid_h, grid_w, palette_kind, side,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_marker, marker_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_frame

GENERATOR_ID = "a0c6005765ee"
VERSION = "1.1.0"
TASK_ID = "a0c6005765ee"
SUMMARY = "5-color rectangle frame with a 7-marker just outside one edge."

INVARIANTS = [
    "background is 0",
    "exactly one 5-color rectangle frame (full perimeter)",
    "exactly one 7-cell in the row/col adjacent to one frame edge",
    "the 7 aligns with a strict-interior column (top/bottom side) or row (left/right side)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_marker", "marker_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "side":           {"type": "choice", "default": "rng top|bot|left|right",
                       "valid": "top|bottom|left|right"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "5frame_with_7marker",
                       "valid": "5frame_with_7marker"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rh = rng.randint(4, 6)
    rw = rng.randint(4, 6)
    r1 = rng.randint(2, h - rh - 1)
    c1 = rng.randint(2, w - rw - 1)
    r2 = r1 + rh - 1
    c2 = c1 + rw - 1
    draw_frame(g, r1, c1, r2, c2, 5)
    side = rng.choice(["top", "bottom", "left", "right"])
    if side == "top":
        g[r1 - 1][rng.randint(c1 + 1, c2 - 1)] = 7
    elif side == "bottom":
        g[r2 + 1][rng.randint(c1 + 1, c2 - 1)] = 7
    elif side == "left":
        g[rng.randint(r1 + 1, r2 - 1)][c1 - 1] = 7
    else:
        g[rng.randint(r1 + 1, r2 - 1)][c2 + 1] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # 7-marker without frame → no enclosure for line to enter
        g[3][5] = 7
        return g
    if name == "no_marker":
        # frame without 7 → no marker direction defined
        draw_frame(g, 2, 2, 7, 7, 5)
        return g
    if name == "marker_at_corner":
        # 7 outside corner → not aligned with strict-interior, ambiguous direction
        draw_frame(g, 2, 2, 7, 7, 5)
        g[1][2] = 7  # at top-left corner column, not interior
        return g
    return g
