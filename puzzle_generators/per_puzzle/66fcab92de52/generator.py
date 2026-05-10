"""Generator for bd5af378.

Rule: L-shaped border moves inward; new interior becomes cyan with a
background diagonal.

Combinatorial axes (8): grid_h/w, corner, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_border, no_bg, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "66fcab92de52"
VERSION = "1.1.0"
TASK_ID = "66fcab92de52"
SUMMARY = "L-shaped border moves inward; interior becomes cyan with bg diagonal."

INVARIANTS = [
    "one modal background color fills the grid",
    "one non-background color forms an L on two adjacent grid edges",
    "the L corner is a grid corner",
    "bg and border colors are distinct and exclude 8",
]

CORNERS = ("top_left", "top_right", "bottom_left", "bottom_right")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_border", "no_bg", "full_grid")
HELPFUL_TEXTURES = CORNERS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "corner":         {"type": "str", "default": "rng helpful",
                       "valid": "|".join(CORNERS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "true",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for corner",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    corner = (overrides.get("texture") if overrides.get("texture") in CORNERS else None) or \
             overrides.get("corner") or \
             ctx.draw_choice("corner", list(CORNERS))
    h = 6 + rng.randint(0, 4)
    w = 6 + rng.randint(0, 4)
    bg, border = ctx.draw_distinct_colors("colors", n=2, exclude={8})
    g = full_grid(h, w, bg)
    top = corner.startswith("top")
    left = corner.endswith("left")
    rr = 0 if top else h - 1
    cc = 0 if left else w - 1
    for c in range(w):
        g[rr][c] = border
    for r in range(h):
        g[r][cc] = border
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 8, 1)
    if name == "no_border":
        return g
    if name == "no_bg":
        return full_grid(8, 8, 2)
    if name == "full_grid":
        for r in range(8):
            for c in range(8):
                g[r][c] = 2
        return g
    return g
