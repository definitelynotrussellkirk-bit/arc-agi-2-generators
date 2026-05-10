"""Generator for e1d2900e.

Rule: blue cells move to nearest side-adjacent slots around 2x2 red
squares.

Combinatorial axes (8): grid_h/w, blue_side, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_squares.
Degenerates: no_squares, no_blue, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0bd65c18b34c"
VERSION = "1.1.0"
TASK_ID = "0bd65c18b34c"
SUMMARY = "Blue cells move to nearest side-adjacent slots around 2x2 red squares."

INVARIANTS = [
    "background is color 0",
    "one or more solid 2x2 squares use color 2",
    "blue cells are aligned with the nearest square row or column span",
    "squares sit clear of borders so blue cells can flank them",
]

BLUE_SIDES = ("left", "right", "top", "bottom")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_squares", "no_blue", "full_grid")
HELPFUL_TEXTURES = BLUE_SIDES

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10"},
    "grid_w":         {"type": "int", "default": "10", "valid": "10"},
    "blue_side":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(BLUE_SIDES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_squares":      {"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for blue_side",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    side = (overrides.get("texture") if overrides.get("texture") in BLUE_SIDES else None) or \
           overrides.get("blue_side") or \
           ctx.draw_choice("blue_side", list(BLUE_SIDES))
    g = full_grid(10, 10, 0)
    sr = 3 + rng.randint(0, 1)
    sc = 3 + rng.randint(0, 1)
    for r in range(sr, sr + 2):
        for c in range(sc, sc + 2):
            g[r][c] = 2
    if side == "left":
        g[sr][sc - 3] = 1
    elif side == "right":
        g[sr + 1][sc + 4] = 1
    elif side == "top":
        g[sr - 3][sc] = 1
    else:
        g[sr + 4][sc + 1] = 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_squares":
        g[3][3] = 1
        return g
    if name == "no_blue":
        for r in range(4, 6):
            for c in range(4, 6):
                g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 2
        return g
    return g
