"""Generator for arc_puzzle_bank_eighteenth21:M120 — legend-driven recolor.

Rule: rows 0-1 hold a top-left legend (each column is a key→value
pair, key on row 0, value on row 1). The rest of the grid has
scattered single-cell markers in legend keys; output replaces each
key with its mapped value and erases the legend itself.

Combinatorial axes (8): grid_h, grid_w, palette_kind, K, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_markers, marker_unmapped.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "e1e7c467196f"
VERSION = "1.1.0"
TASK_ID = "e1e7c467196f"
SUMMARY = "Top-left 2×K legend (keys row 0, values row 1) + scattered key markers."

INVARIANTS = [
    "background is 0",
    "rows 0-1, cols 0..K-1 hold a legend: key/value pairs (K = 2 or 3)",
    "all keys distinct; all values distinct; key/value sets are disjoint",
    "elsewhere: 3-6 single-cell markers, each in one of the legend keys",
    "no markers in the legend rows/cols (so legend stays intact)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_markers", "marker_unmapped")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "K":              {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "n_markers":      {"type": "int", "default": "rng 3..6", "valid": "2..10"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "4..8"},
    "position_bias":  {"type": "str", "default": "top_left_legend_with_markers",
                       "valid": "top_left_legend_with_markers"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "4..8"},
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
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        K = ctx.draw_int("K", 2, 2)
        n_markers = ctx.draw_int("n_markers", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        K = ctx.draw_int("K", 3, 3)
        n_markers = ctx.draw_int("n_markers", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 10)
        K = ctx.draw_int("K", 2, 3)
        n_markers = ctx.draw_int("n_markers", 3, 6)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = list(random_palette(rng, 2 * K))
    keys = palette[:K]
    values = palette[K:]
    for i in range(K):
        g[0][i] = keys[i]
        g[1][i] = values[i]
    placed = 0
    for _ in range(80):
        if placed >= n_markers: break
        mr = rng.randint(2, h - 1)
        mc = rng.randint(0, w - 1)
        if g[mr][mc] != 0: continue
        g[mr][mc] = rng.choice(keys)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # rows 0-1 blank → no key→value mapping defined; rule has no instruction
        g[3][3] = 4; g[5][6] = 4  # marker color 4 with no legend entry
        return g
    if name == "no_markers":
        # legend present but no markers → rule has nothing to recolor
        g[0][0] = 4; g[1][0] = 6  # 4→6
        g[0][1] = 3; g[1][1] = 8  # 3→8
        return g
    if name == "marker_unmapped":
        # legend present but markers use colors not in legend keys → rule has no mapping
        g[0][0] = 4; g[1][0] = 6
        g[0][1] = 3; g[1][1] = 8
        g[3][3] = 7; g[5][5] = 9  # 7 and 9 are not legend keys
        return g
    return g
