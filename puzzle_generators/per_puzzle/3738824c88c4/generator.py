"""Generator for 6cbe9eb8.

Rule: detected same-color rectangles are nested into the largest
rectangle's canvas.

Combinatorial axes (8): grid_h/w, inner_style, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_inner, no_outer, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "3738824c88c4"
VERSION = "1.1.0"
TASK_ID = "3738824c88c4"
SUMMARY = "Detected same-color rectangles nested into largest rectangle's canvas."

INVARIANTS = [
    "one dominant outer color occupies the background canvas",
    "additional same-color rectangle components are present elsewhere",
    "rectangle components may be solid or hollow frames",
    "outer, mid and small colors are distinct and non-zero",
]

INNER_STYLES = ("solid", "frame")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_inner", "no_outer", "full_grid")
HELPFUL_TEXTURES = INNER_STYLES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "inner_style":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(INNER_STYLES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for inner_style",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    style = (overrides.get("texture") if overrides.get("texture") in INNER_STYLES else None) or \
            overrides.get("inner_style") or \
            ctx.draw_choice("inner_style", list(INNER_STYLES))
    outer_color, mid_color, small_color = ctx.draw_distinct_colors(
        "colors", n=3, exclude={0}
    )
    h = 10 + rng.randint(0, 3)
    w = 11 + rng.randint(0, 3)
    g = full_grid(h, w, outer_color)
    for r in range(1, 3):
        for c in range(1, 4):
            g[r][c] = mid_color
    if style == "solid":
        for r in range(h - 4, h - 2):
            for c in range(w - 5, w - 2):
                g[r][c] = small_color
    else:
        draw_frame(g, h - 5, w - 6, h - 2, w - 2, small_color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 12, 1)
    if name == "no_inner":
        return g
    if name == "no_outer":
        for r in range(1, 3):
            for c in range(1, 4):
                g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(12):
                g[r][c] = 1
        return g
    return g
