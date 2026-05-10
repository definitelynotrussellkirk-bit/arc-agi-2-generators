"""Generator for arc_additional_puzzle_bank_volume9:M62 — Pick rectangle by aspect.

Rule: ctrl ∈ {2,3,4}: 2 → wide (w>h), 3 → tall (h>w), else → square.
Find solid 1-rectangle of matching aspect; output bbox crop.

Combinatorial axes (8): grid_h, grid_w, palette_kind, ctrl,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_ctrl, no_matching_aspect, missing_rect.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "93f403d486af"
VERSION = "1.1.0"
TASK_ID = "93f403d486af"
SUMMARY = "Ctrl at (0,0) ∈ {2,3,4} + 3 solid 1-rects (one wide, one tall, one square)."

INVARIANTS = [
    "(0,0) is ctrl ∈ {2,3,4}",
    "exactly one wide solid rect (w>h)",
    "exactly one tall solid rect (h>w)",
    "exactly one square solid rect",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_ctrl", "no_matching_aspect", "missing_rect")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "ctrl":           {"type": "int", "default": "rng 2..4", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "ctrl_with_3_aspect_rects",
                       "valid": "ctrl_with_3_aspect_rects"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _solid(g, r1, c1, r2, c2, color):
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 11, 12)
        ctrl = ctx.draw_int("ctrl", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
        ctrl = ctx.draw_int("ctrl", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
        ctrl = ctx.draw_int("ctrl", 2, 4)
    g = full_grid(h, w, 0)
    g[0][0] = ctrl
    # square (3x3)
    _solid(g, 1, 7, 3, 9, 1)
    # wide (1x4)
    _solid(g, 5, 1, 5, 4, 1)
    # tall (4x2)
    _solid(g, 6, 7, 9, 8, 1)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_ctrl":
        # (0,0) is 0 → no aspect code, rule has no selection criterion
        _solid(g, 1, 7, 3, 9, 1)
        _solid(g, 5, 1, 5, 4, 1)
        _solid(g, 6, 7, 9, 8, 1)
        return g
    if name == "no_matching_aspect":
        # ctrl=2 (asks for wide) but no wide rect → all rects tall/square
        g[0][0] = 2
        _solid(g, 1, 7, 3, 9, 1)            # square
        _solid(g, 5, 1, 9, 1, 1)            # tall (5x1)
        _solid(g, 6, 7, 9, 8, 1)            # tall (4x2)
        return g
    if name == "missing_rect":
        # ctrl=3 (asks for tall) but only one rect type present (squares)
        g[0][0] = 3
        _solid(g, 1, 1, 3, 3, 1)            # square
        _solid(g, 5, 5, 7, 7, 1)            # square
        return g
    return g
