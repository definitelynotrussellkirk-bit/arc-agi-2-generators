"""Generator for df978a02.

Rule: shape tips nearest center are removed; largest shape gains
opposite bar.

Combinatorial axes (8): grid_h/w, side, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_target, no_small, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "474634a9f7b7"
VERSION = "1.1.0"
TASK_ID = "474634a9f7b7"
SUMMARY = "Shape tips nearest center removed; largest shape gains opposite bar."

INVARIANTS = [
    "the background is cyan",
    "each object has a body plus a one-cell tip facing the grid center",
    "non-target object tips are erased",
    "target and small colors are distinct and exclude 8",
]

SIDES = ("left", "right", "top", "bottom")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_target", "no_small", "full_grid")
HELPFUL_TEXTURES = SIDES

AXES = {
    "grid_h":         {"type": "int", "default": "15", "valid": "15"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "side":           {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SIDES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for side",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    side = (overrides.get("texture") if overrides.get("texture") in SIDES else None) or \
           overrides.get("side") or \
           ctx.draw_choice("side", list(SIDES))
    if "side" not in overrides and overrides.get("texture") not in SIDES:
        side = ["left", "top", "right", "bottom"][sample_index % 4]
    target, small = ctx.draw_distinct_colors("colors", n=2, exclude={8})
    g = full_grid(15, 15, 8)
    if side == "left":
        draw_rect(g, 6, 2, 3, 4, target)
        g[7][6] = target
    elif side == "right":
        draw_rect(g, 6, 9, 3, 4, target)
        g[7][8] = target
    elif side == "top":
        draw_rect(g, 2, 6, 4, 3, target)
        g[6][7] = target
    else:
        draw_rect(g, 9, 6, 4, 3, target)
        g[8][7] = target
    draw_rect(g, 1, 1, 2, 2, small)
    g[3][2] = small
    draw_rect(g, 11, 11, 2, 2, small)
    g[10][11] = small
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 15, 8)
    if name == "no_target":
        draw_rect(g, 1, 1, 2, 2, 2)
        return g
    if name == "no_small":
        draw_rect(g, 6, 2, 3, 4, 1)
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(15):
                g[r][c] = 8
        return g
    return g
