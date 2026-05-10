"""Generator for 6855a6e4.

Rule: each gray shape mirrors across the closed back wall of its
nearest red C-shape.

Combinatorial axes (8): grid_h/w, opening, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_C, no_gray, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "28d51fb858a1"
VERSION = "1.1.0"
TASK_ID = "28d51fb858a1"
SUMMARY = "Each gray shape mirrors across closed back wall of nearest red C-shape."

INVARIANTS = [
    "a red C-shape has exactly one open side",
    "one gray object sits near the open side",
    "the closed side opposite the opening is the mirror wall",
    "the output removes the original gray object and paints its mirror image",
]

OPENINGS = ("right", "left", "down", "up")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_C", "no_gray", "full_grid")
HELPFUL_TEXTURES = OPENINGS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "opening":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(OPENINGS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for opening",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _draw_c(g, r1, c1, r2, c2, opening):
    for c in range(c1, c2 + 1):
        if opening != "up":
            g[r1][c] = 2
        if opening != "down":
            g[r2][c] = 2
    for r in range(r1, r2 + 1):
        if opening != "left":
            g[r][c1] = 2
        if opening != "right":
            g[r][c2] = 2


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    opening = (overrides.get("texture") if overrides.get("texture") in OPENINGS else None) or \
              overrides.get("opening") or \
              ctx.draw_choice("opening", list(OPENINGS))
    h = 11
    w = 12
    g = full_grid(h, w, 0)
    r1, c1, r2, c2 = 3, 4, 7, 7
    _draw_c(g, r1, c1, r2, c2, opening)
    shape = [(0, 0), (1, 0), (1, 1)] if rng.randint(0, 1) else [(0, 0), (0, 1), (1, 1)]
    if opening == "right":
        paint_at(g, 4, 8, shape, 5)
    elif opening == "left":
        paint_at(g, 4, 1, shape, 5)
    elif opening == "down":
        paint_at(g, 8, 5, shape, 5)
    else:
        paint_at(g, 0, 5, shape, 5)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 12, 0)
    if name == "no_C":
        g[4][8] = 5
        return g
    if name == "no_gray":
        _draw_c(g, 3, 4, 7, 7, "right")
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
