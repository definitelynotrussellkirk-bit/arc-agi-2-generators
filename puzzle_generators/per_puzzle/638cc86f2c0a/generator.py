"""Generator for arc_puzzle_bank_sixth_21_bundle:hard_42_chamber_elbow_paths.

Rule: inside each color-5 chamber, connect same-color point pairs with
vertical-first elbow paths.

Combinatorial axes (8): grid_h, grid_w, palette_kind, variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_chambers, no_pairs, mismatched_pair_colors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "638cc86f2c0a"
VERSION = "1.1.0"
TASK_ID = "638cc86f2c0a"
SUMMARY = "Inside each color-5 chamber, connect same-color point pairs with vertical-first elbow paths."

INVARIANTS = [
    "color-5 rectangular frames define independent chambers",
    "inside each chamber, a color appears exactly twice as path endpoints",
    "the rule draws a vertical-first orthogonal elbow between each same-color pair",
    "frame borders and unrelated outside markers are preserved",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_chambers", "no_pairs", "mismatched_pair_colors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "7", "valid": "7..7"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "variant":        {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "two_chambers_with_pairs",
                       "valid": "two_chambers_with_pairs"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PAIRS = [
    ((0, 0), (3, 4)),
    ((0, 3), (3, 1)),
    ((1, 0), (3, 3)),
    ((0, 4), (2, 1)),
    ((2, 0), (0, 3)),
]

_COLORS = [1, 2, 3, 4, 6]


def _add_pair_frame(g, top, left, color, pair):
    draw_frame(g, top, left, top + 5, left + 6, 5)
    for r, c in pair:
        g[top + 1 + r][left + 1 + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        variant = (ctx.draw_int("variant", 0, 1) + sample_index) % 2
    elif difficulty == "hard":
        variant = (ctx.draw_int("variant", 2, 4) + sample_index) % 5
    else:
        variant = (ctx.draw_int("variant", 0, len(_PAIRS) - 1) + sample_index) % len(_PAIRS)
    g = full_grid(7, 15, 0)
    _add_pair_frame(g, 0, 0, _COLORS[variant], _PAIRS[variant])
    _add_pair_frame(g, 0, 8, 6 + (variant % 4), _PAIRS[-1 - variant])
    g[6][(sample_index * 2 + variant) % 15] = 9
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 15, 0)
    if name == "no_chambers":
        # endpoint pairs but no 5-chambers → no scope to connect within
        g[1][1] = 4; g[4][5] = 4
        g[1][9] = 6; g[4][13] = 6
        return g
    if name == "no_pairs":
        # chambers exist but no endpoint pairs inside → nothing to connect
        draw_frame(g, 0, 0, 5, 6, 5)
        draw_frame(g, 0, 8, 5, 14, 5)
        return g
    if name == "mismatched_pair_colors":
        # chamber endpoints use different colors → no same-color pair to connect
        draw_frame(g, 0, 0, 5, 6, 5)
        draw_frame(g, 0, 8, 5, 14, 5)
        g[1][1] = 4; g[4][5] = 6   # mismatched
        g[1][9] = 7; g[4][13] = 8  # mismatched
        return g
    return g
