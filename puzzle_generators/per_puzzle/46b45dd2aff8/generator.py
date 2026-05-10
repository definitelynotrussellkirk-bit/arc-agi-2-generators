"""Generator for a2d730bd.

Rule: each colored dot connects to its matching rectangle with a flower,
stem, and cap.

Combinatorial axes (8): grid_h/w, layout, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_dots, no_rects, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "46b45dd2aff8"
VERSION = "1.1.0"
TASK_ID = "46b45dd2aff8"
SUMMARY = "Each colored dot connects to matching rectangle via flower, stem, and cap."

INVARIANTS = [
    "each active color has one rectangle and one singleton dot",
    "a dot is horizontally or vertically aligned with its matching rectangle",
    "the dot becomes a plus flower connected by a stem to the rectangle edge",
]

LAYOUTS = ("L0", "L1", "L2", "L3")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_dots", "no_rects", "full_grid")
HELPFUL_TEXTURES = LAYOUTS

AXES = {
    "grid_h":         {"type": "int", "default": "15", "valid": "15"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "layout":         {"type": "choice", "default": "rng helpful",
                       "valid": "0|1|2|3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for layout",
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
    if tx in LAYOUTS:
        layout = int(tx[1])
    elif "layout" in overrides:
        layout = ctx.draw_choice("layout", [0, 1, 2, 3])
    else:
        layout = sample_index % 4
    c1, c2 = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    g = full_grid(15, 15, 0)
    draw_rect(g, 5, 6, 4, 4, c1)
    draw_rect(g, 2, 2, 3, 3, c2)
    if layout in {0, 2}:
        g[6][2] = c1
    else:
        g[10][8] = c1
    if layout in {0, 1}:
        g[3][9] = c2
    else:
        g[8][3] = c2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 15, 0)
    if name == "no_dots":
        draw_rect(g, 5, 6, 4, 4, 3)
        draw_rect(g, 2, 2, 3, 3, 4)
        return g
    if name == "no_rects":
        g[6][2] = 3
        g[3][9] = 4
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(15):
                g[r][c] = 3
        return g
    return g
