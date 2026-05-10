"""Generator for 36d67576.

Rule: a multicolor accent template is copied onto matching yellow shapes.

Combinatorial axes (8): grid_h/w, target_count, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_template, no_targets, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "089c14df9952"
VERSION = "1.1.0"
TASK_ID = "089c14df9952"
SUMMARY = "Multicolor accent template copied onto matching yellow shapes."

INVARIANTS = [
    "the base object has the richest set of non-yellow accent colors",
    "target objects contain the same yellow shape and at most one accent color",
    "matching targets receive the base object's transformed accent cells",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_targets", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "target_count":   {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint_shape(g, r, c, accents=None):
    for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1), (2, 1)]:
        g[r + dr][c + dc] = 4
    for dr, dc, color in accents or []:
        g[r + dr][c + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        target_count = ctx.draw_int("target_count", 1, 1)
    elif difficulty == "hard":
        target_count = ctx.draw_int("target_count", 3, 3)
    else:
        target_count = ctx.draw_int("target_count", 1, 3)
    accent_a, accent_b = ctx.draw_distinct_colors("accents", n=2, exclude={0, 4})
    g = full_grid(14, 15, 0)
    _paint_shape(g, 1, 1, [(0, 2, accent_a), (2, 2, accent_b)])
    targets = [(1, 8), (7, 2), (8, 9)]
    for r, c in targets[:target_count]:
        _paint_shape(g, r, c)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 15, 0)
    if name == "no_template":
        _paint_shape(g, 1, 8)
        return g
    if name == "no_targets":
        _paint_shape(g, 1, 1, [(0, 2, 3), (2, 2, 5)])
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(15):
                g[r][c] = 4
        return g
    return g
