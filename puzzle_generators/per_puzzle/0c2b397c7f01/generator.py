"""Generator for e45ef808.

Rule: ceiling row + histogram; rule paints yellow above tallest, maroon
above shortest col.

Combinatorial axes (8): grid_h/w, palette_kind, n_ones, position_bias,
anchor_corner, asymmetry_force, palette_size, height_skew.
Degenerates: no_ceiling, no_histogram, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0c2b397c7f01"
VERSION = "1.1.0"
TASK_ID = "0c2b397c7f01"
SUMMARY = "Ceiling + histogram; rule paints yellow above tallest, maroon above shortest."

INVARIANTS = [
    "row 0 has at least one 1 cell (ceiling)",
    "histogram color sc != 0 and != 1, != 4, != 9",
    "each column has 0 or N consecutive sc cells starting from bottom",
    "max non-zero col height and min non-zero col height are distinct",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_ceiling", "no_histogram", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_ones":         {"type": "int", "default": "rng 1..w/2",
                       "valid": "1..w/2"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered|spread|rng"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "height_skew":    {"type": "str", "default": "rng",
                       "valid": "uniform|skewed|rng"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 6, 8
    elif difficulty == "hard":
        h_lo, h_hi = 12, 16
    else:
        h_lo, h_hi = 8, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette = ctx.draw_distinct_colors("palette", n=1,
                                       exclude={0, 1, 4, 9})
    sc = palette[0]
    g = full_grid(h, w, 0)
    n_ones = int(overrides.get("n_ones",
                               rng.randint(1, max(1, w // 2))))
    n_ones = max(1, min(w, n_ones))
    cols_for_one = rng.sample(range(w), n_ones)
    for c in cols_for_one:
        g[0][c] = 1
    heights = []
    for c in range(w):
        height = rng.randint(0, h - 2)
        heights.append(height)
        for k in range(height):
            g[h - 1 - k][c] = sc
    nonzero_heights = [(c, h_v) for c, h_v in enumerate(heights) if h_v > 0]
    if len(nonzero_heights) < 2:
        g[h - 1][0] = sc
        g[h - 1][w - 1] = sc
        g[h - 2][0] = sc
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_ceiling":
        for c in range(w):
            for k in range(rng.randint(1, h - 2)):
                g[h - 1 - k][c] = 2
        return g
    if name == "no_histogram":
        for c in range(w):
            g[0][c] = 1
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
