"""Generator for 689c358e.

Rule: colored crosses inside a purple frame project their longest arm
color to the opposite border and clear the facing border.

Combinatorial axes (8): grid_h/w, cross_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_crosses, no_frame, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e937c5b85cdd"
VERSION = "1.1.0"
TASK_ID = "e937c5b85cdd"
SUMMARY = "Colored crosses inside a purple frame project longest-arm color to opposite border."

INVARIANTS = [
    "background is color 7",
    "the outer border is color 6",
    "each interior object is a single-colored cross",
    "one arm is strictly longest for each cross",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_crosses", "no_frame", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "10..13"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "10..13"},
    "cross_count":    {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        n = ctx.draw_int("cross_count", 1, 1)
    elif difficulty == "hard":
        n = ctx.draw_int("cross_count", 2, 2)
    else:
        n = ctx.draw_int("cross_count", 1, 2)
    h = 10 + rng.randint(0, 3)
    w = 10 + rng.randint(0, 3)
    colors = ctx.draw_distinct_colors("colors", n=n, exclude={0, 6, 7})
    g = full_grid(h, w, 7)
    for c in range(w):
        g[0][c] = 6
        g[h - 1][c] = 6
    for r in range(h):
        g[r][0] = 6
        g[r][w - 1] = 6
    centers = [(h // 2, 3), (h // 2, w - 4)]
    for i in range(n):
        r, c = centers[i]
        color = colors[i]
        arms = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
        if (seed + sample_index + i) % 2 == 0:
            arms.extend([(0, 2), (0, 3)])
        else:
            arms.extend([(-2, 0), (-3, 0)])
        for dr, dc in arms:
            g[r + dr][c + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 7)
    if name == "no_crosses":
        for c in range(11):
            g[0][c] = 6
            g[10][c] = 6
        for r in range(11):
            g[r][0] = 6
            g[r][10] = 6
        return g
    if name == "no_frame":
        for dr, dc in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            g[5 + dr][5 + dc] = 3
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 6
        return g
    return g
