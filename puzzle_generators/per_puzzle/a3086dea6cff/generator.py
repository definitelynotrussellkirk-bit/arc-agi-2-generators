"""Generator for arc_additional_puzzles_21_set4:M26.

Rule: pairs of same-colored points sharing a row or column are
completed into straight segments.

Combinatorial axes (8): grid_h, grid_w, palette_kind, orientation,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_aligned_pairs, single_endpoint, span_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a3086dea6cff"
VERSION = "1.1.0"
TASK_ID = "a3086dea6cff"
SUMMARY = "Pairs of same-colored points sharing a row or column are completed into straight segments."

INVARIANTS = [
    "each active color appears exactly twice",
    "same-row pairs fill the horizontal segment between endpoints",
    "same-column pairs fill the vertical segment between endpoints",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_aligned_pairs", "single_endpoint", "span_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10"},
    "grid_w":         {"type": "int", "default": "10", "valid": "10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "orientation":    {"type": "str", "default": "both",
                       "valid": "horizontal|vertical|both"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "axis_aligned",
                       "valid": "axis_aligned"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    orientation = ctx.draw_choice("orientation", ["horizontal", "vertical", "both"])
    if "orientation" not in overrides:
        orientation = ["horizontal", "vertical", "both"][sample_index % 3]
    a, b = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    g = full_grid(10, 10, 0)
    if orientation in ("horizontal", "both"):
        r = 2 + (sample_index % 4)
        g[r][1] = a
        g[r][7] = a
    if orientation in ("vertical", "both"):
        c = 3 + ((sample_index // 2) % 4)
        g[1][c] = b
        g[8][c] = b
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_aligned_pairs":
        # color pairs exist but neither shares a row or column → no segments to draw
        g[1][1] = 3; g[5][7] = 3
        g[2][3] = 4; g[7][8] = 4
        return g
    if name == "single_endpoint":
        # only one point per color → no pair, rule has no segment to draw
        g[3][2] = 5
        g[6][7] = 6
        return g
    if name == "span_already_filled":
        # span between endpoints is already painted with another color → conflict
        g[3][1] = 4; g[3][7] = 4
        for c in range(2, 7):
            g[3][c] = 6
        return g
    return g
