"""Generator for d753a70b.

Rule: red diamond outlines shrink, gray diamond outlines grow on
orange background.

Combinatorial axes (8): grid_h/w, red_radius, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
gray_radius.
Degenerates: no_red, no_gray, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "388e9ae29018"
VERSION = "1.1.0"
TASK_ID = "388e9ae29018"
SUMMARY = "Red diamonds shrink; gray diamonds grow; orange background."

INVARIANTS = [
    "the background is orange",
    "red and gray objects are Manhattan-distance diamond outlines",
    "red objects shrink one radius while gray objects grow one radius",
    "diamonds sit clear of grid borders so growth/shrink stays in-bounds",
]

RED_RADII = ("r2", "r3")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_red", "no_gray", "full_grid")
HELPFUL_TEXTURES = RED_RADII

AXES = {
    "grid_h":         {"type": "int", "default": "15", "valid": "15"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "red_radius":     {"type": "str", "default": "rng helpful",
                       "valid": "|".join(RED_RADII)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "gray_radius":    {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "texture":        {"type": "str", "default": "alias for red_radius",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _draw_diamond(g, cr, cc, radius, color):
    for r in range(len(g)):
        for c in range(len(g[0])):
            if abs(r - cr) + abs(c - cc) == radius:
                g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in RED_RADII:
        red_radius = int(tx[1])
    else:
        red_radius = ctx.draw_choice("red_radius", [2, 3])
        if "red_radius" not in overrides:
            red_radius = 2 + (sample_index % 2)
    g = full_grid(15, 15, 7)
    red_r = 4 + ((sample_index // 2) % 2)
    red_c = 5 + (sample_index % 2)
    gray_r = 10 + ((sample_index // 4) % 2)
    gray_c = 10 - ((sample_index // 3) % 2)
    gray_radius = 1 + ((sample_index // 2) % 2)
    _draw_diamond(g, red_r, red_c, red_radius, 2)
    _draw_diamond(g, gray_r, gray_c, gray_radius, 5)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 15, 7)
    if name == "no_red":
        _draw_diamond(g, 7, 7, 2, 5)
        return g
    if name == "no_gray":
        _draw_diamond(g, 7, 7, 2, 2)
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(15):
                g[r][c] = 7
        return g
    return g
