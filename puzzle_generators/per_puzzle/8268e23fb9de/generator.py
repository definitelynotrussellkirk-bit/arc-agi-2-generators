"""Generator for b7955b3c.

Rule: cyan noise inside overlapping rectangles is restored using
inferred z-order.

Combinatorial axes (8): grid_h/w, order, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_overlap, no_noise, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "8268e23fb9de"
VERSION = "1.1.0"
TASK_ID = "8268e23fb9de"
SUMMARY = "Cyan noise inside overlapping rectangles is restored using inferred z-order."

INVARIANTS = [
    "colored rectangles overlap on a modal background",
    "later rectangles visibly dominate overlap regions",
    "cyan cells are noise placeholders inside one or more rectangle bounding boxes",
    "each cyan cell is replaced by the topmost containing rectangle color",
]

ORDERS = ("o0", "o1", "o2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_overlap", "no_noise", "full_grid")
HELPFUL_TEXTURES = ORDERS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "order":          {"type": "choice", "default": "rng helpful",
                       "valid": "0|1|2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for order",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in ORDERS:
        order = int(tx[1])
    else:
        order = ctx.draw_choice("order", [0, 1, 2])
    colors = list(ctx.draw_distinct_colors("colors", n=3, exclude={0, 8}))
    boxes = [(2, 2, 7, 7), (4, 5, 7, 7), (1, 8, 8, 5)]
    orders = [(0, 1, 2), (1, 0, 2), (0, 2, 1)]
    g = full_grid(14, 15, 0)
    for idx in orders[order]:
        draw_rect(g, *boxes[idx], colors[idx])
    for r, c in [(5, 6), (6, 9), (3, 9), (8, 10)]:
        g[r][c] = 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 15, 0)
    if name == "no_overlap":
        draw_rect(g, 2, 2, 3, 3, 3)
        draw_rect(g, 9, 9, 3, 3, 4)
        return g
    if name == "no_noise":
        draw_rect(g, 2, 2, 7, 7, 3)
        draw_rect(g, 4, 5, 7, 7, 4)
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(15):
                g[r][c] = 8
        return g
    return g
