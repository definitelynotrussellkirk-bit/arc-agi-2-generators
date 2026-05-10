"""Generator for puzzle 9f8de559.

Rule: arrow (head=2, tail=6) + orange(7) shape. Output shoots ray
from arrow through orange interior; punches hole at first non-interior
cell.

Combinatorial axes (8): grid_h/w, arrow_direction, arrow_position,
shape_h, shape_w, shape_position, anchor_corner, asymmetry_force.
Degenerates: no_arrow, no_shape, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "b8e2a07c1b6c"
VERSION = "1.1.0"
TASK_ID = "b8e2a07c1b6c"
SUMMARY = "Arrow + orange shape; rule shoots ray + punches hole."

INVARIANTS = [
    "background is 0",
    "exactly 1 red(2) head adjacent to 1 magenta(6) tail",
    "head + tail aligned horizontally OR vertically",
    "arrow's ray hits a solid orange(7) shape",
]

ARROW_DIRECTIONS = ("right", "left", "down", "up")
DEGENERATE_TEXTURES = ("no_arrow", "no_shape", "full_grid")
HELPFUL_TEXTURES = ARROW_DIRECTIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "grid_w":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "arrow_direction":{"type": "str", "default": "rng helpful",
                       "valid": "|".join(ARROW_DIRECTIONS)},
    "shape_h":        {"type": "int", "default": "rng 3..5", "valid": "3..7"},
    "shape_w":        {"type": "int", "default": "rng 3..5", "valid": "3..7"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "include_decoy":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for arrow_direction",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 10, 13
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
    else:
        h_lo, h_hi = 12, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    direction = (overrides.get("texture") or
                 overrides.get("arrow_direction")
                 or ctx.draw_choice("arrow_direction",
                                    list(ARROW_DIRECTIONS)))
    rh = int(overrides.get("shape_h",
                           ctx.draw_int("shape_h", 3, 5)))
    rw = int(overrides.get("shape_w",
                           ctx.draw_int("shape_w", 3, 5)))
    rh = max(3, min(7, rh))
    rw = max(3, min(7, rw))
    g = full_grid(h, w, 0)
    if direction == "right":
        ar = rng.randint(2, h - 3)
        g[ar][1] = 6  # tail
        g[ar][2] = 2  # head
        rr = max(0, ar - 1)
        rc = rng.randint(w // 2, max(w // 2, w - rw - 1))
        if rr + rh > h:
            rr = h - rh
        draw_rect(g, rr, rc, rh, rw, 7)
    elif direction == "left":
        ar = rng.randint(2, h - 3)
        g[ar][w - 2] = 6  # tail
        g[ar][w - 3] = 2  # head
        rr = max(0, ar - 1)
        rc = rng.randint(0, max(0, w // 2 - rw))
        if rr + rh > h:
            rr = h - rh
        draw_rect(g, rr, rc, rh, rw, 7)
    elif direction == "down":
        ac = rng.randint(2, w - 3)
        g[1][ac] = 6
        g[2][ac] = 2
        rc = max(0, ac - 1)
        rr = rng.randint(h // 2, max(h // 2, h - rh - 1))
        if rc + rw > w:
            rc = w - rw
        draw_rect(g, rr, rc, rh, rw, 7)
    else:  # up
        ac = rng.randint(2, w - 3)
        g[h - 2][ac] = 6
        g[h - 3][ac] = 2
        rc = max(0, ac - 1)
        rr = rng.randint(0, max(0, h // 2 - rh))
        if rc + rw > w:
            rc = w - rw
        draw_rect(g, rr, rc, rh, rw, 7)
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_arrow":
        draw_rect(g, h // 2, w // 2, 3, 3, 7)
        return g
    if name == "no_shape":
        ar = h // 2
        g[ar][1] = 6
        g[ar][2] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 7
        return g
    return g
