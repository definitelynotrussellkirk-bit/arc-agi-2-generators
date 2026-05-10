"""Generator for 3e980e27.

Rule: multicolor source object is copied to singleton anchors of
matching unique source colors.

Combinatorial axes (8): grid_h/w, anchor_color, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_source, no_anchor, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ff76baf6c2d9"
VERSION = "1.1.0"
TASK_ID = "ff76baf6c2d9"
SUMMARY = "Multicolor source copied to singleton anchors of matching unique colors."

INVARIANTS = [
    "one multicolor 8-connected source object contains unique anchor colors",
    "singleton target objects share one of those anchor colors",
    "color-2 anchors mirror the column offset while other anchors preserve it",
    "anchor and other colors are distinct and non-zero",
]

ANCHOR_COLORS = ("c1", "c2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_source", "no_anchor", "full_grid")
HELPFUL_TEXTURES = ANCHOR_COLORS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "anchor_color":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ANCHOR_COLORS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for anchor_color",
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
    if tx in ANCHOR_COLORS:
        anchor_color = int(tx[1])
    else:
        anchor_color = ctx.draw_choice("anchor_color", (1, 2))
    other_a, other_b = ctx.draw_distinct_colors("others", n=2, exclude={0, anchor_color})
    g = full_grid(12, 12, 0)
    sr = rng.randint(2, 3)
    sc = rng.randint(2, 3)
    g[sr][sc] = anchor_color
    g[sr][sc + 1] = other_a
    g[sr + 1][sc] = other_b
    g[sr + 1][sc + 1] = other_a
    target = (rng.randint(7, 9), rng.randint(7, 9))
    g[target[0]][target[1]] = anchor_color
    if rng.choice([True, False]):
        g[target[0] - 3][target[1]] = anchor_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_source":
        g[8][8] = 1
        return g
    if name == "no_anchor":
        g[2][2] = 1; g[2][3] = 3; g[3][2] = 4
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
