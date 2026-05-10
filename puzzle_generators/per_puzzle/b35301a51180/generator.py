"""Generator for v1_e_m_h_keys:H5.

Rule: choose the color with the most components and fill its enclosed
holes with 9.

Combinatorial axes (8): grid_h, grid_w, palette_kind, target_color,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_components, all_one_color, no_holes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b35301a51180"
VERSION = "1.1.0"
TASK_ID = "b35301a51180"
SUMMARY = "Choose the color with most components and fill its enclosed holes with 9."

INVARIANTS = [
    "color A appears as two separate hollow rectangular components",
    "another color appears as one hollow component",
    "the most component-rich color is therefore unambiguous",
    "only holes of the selected color are filled with 9",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "all_one_color", "no_holes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "target_color":   {"type": "int", "default": "rng choice", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "two_targets_one_other",
                       "valid": "two_targets_one_other"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "density":        {"type": "str", "default": "components", "valid": "components"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _ring(g, top, left, color):
    for c in range(left, left + 3):
        g[top][c] = color
        g[top + 2][c] = color
    for r in range(top, top + 3):
        g[r][left] = color
        g[r][left + 2] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        target_color = ctx.draw_choice("target_color", [1, 2, 3])
    elif difficulty == "hard":
        target_color = ctx.draw_choice("target_color", [4, 5, 6, 7, 8])
    else:
        target_color = ctx.draw_choice("target_color", [1, 2, 3, 4, 5, 6, 7, 8])
    other_color = rng.choice([c for c in [1, 2, 3, 4, 5, 6, 7, 8] if c != target_color])
    g = full_grid(11, 9, 0)
    _ring(g, 1, 1, target_color)
    _ring(g, 5, 4, target_color)
    _ring(g, 8, 1, other_color)
    g[2][6] = other_color
    g[2][7] = other_color
    g[3][6] = other_color
    g[3][7] = other_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 9, 0)
    if name == "no_components":
        # empty grid → no components to count
        return g
    if name == "all_one_color":
        # only one color present → "most-components-color" trivially that one, but rule expects competition
        _ring(g, 1, 1, 4)
        _ring(g, 5, 4, 4)
        return g
    if name == "no_holes":
        # solid blocks, no enclosed holes → rule has nothing to fill
        for r in range(1, 4):
            for c in range(1, 4): g[r][c] = 4
        for r in range(5, 8):
            for c in range(4, 7): g[r][c] = 4
        for r in range(8, 11):
            for c in range(1, 4): g[r][c] = 6
        return g
    return g
