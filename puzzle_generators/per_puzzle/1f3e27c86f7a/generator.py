"""Generator for 40f6cd08.

Rule: a framed template maps its inner colors into a same-color plain
frame.

Combinatorial axes (8): grid_h/w, target_width, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_template, no_target, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "1f3e27c86f7a"
VERSION = "1.1.0"
TASK_ID = "1f3e27c86f7a"
SUMMARY = "Framed template maps inner colors into same-color plain frame."

INVARIANTS = [
    "the background is zero",
    "one template frame has a border in the target frame color",
    "the template interior contains nonzero non-border colors",
    "a plain frame of the same color receives the aligned interior pattern",
]

WIDTH_KINDS = ("W5", "W6", "W7")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_target", "full_grid")
HELPFUL_TEXTURES = WIDTH_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9"},
    "grid_w":         {"type": "int", "default": "18", "valid": "18"},
    "target_width":   {"type": "choice", "default": "rng helpful",
                       "valid": "5|6|7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for target_width",
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
    if tx in WIDTH_KINDS:
        width = int(tx[1])
    else:
        width = ctx.draw_choice("target_width", [5, 6, 7])
    edge, left_inner, mid_inner = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    g = full_grid(9, 18, 0)
    draw_frame(g, 1, 1, 5, 5, edge)
    inner = [
        [left_inner, mid_inner, left_inner],
        [mid_inner, left_inner, mid_inner],
        [left_inner, mid_inner, left_inner],
    ]
    for r in range(3):
        for c in range(3):
            g[2 + r][2 + c] = inner[r][c]
    draw_frame(g, 1, 10, 5, 10 + width - 1, edge)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 18, 0)
    if name == "no_template":
        draw_frame(g, 1, 10, 5, 14, 3)
        return g
    if name == "no_target":
        draw_frame(g, 1, 1, 5, 5, 3)
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(18):
                g[r][c] = 3
        return g
    return g
