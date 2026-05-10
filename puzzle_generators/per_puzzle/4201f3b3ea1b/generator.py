"""Generator for set10:E64 — Stamp motif (relative to 5-anchor) at each 6-anchor.

Rule: src=first 5 cell, anchors=6-cells, motif=non-{0,5,6} cells.
For each anchor, stamp motif relative offsets onto grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_motif,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, no_motif, no_targets.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4201f3b3ea1b"
VERSION = "1.1.0"
TASK_ID = "4201f3b3ea1b"
SUMMARY = "8×8 grid: 1 5-anchor + 2-4 motif cells nearby + 1-2 6-anchors elsewhere."

INVARIANTS = [
    "exactly one 5-cell (motif anchor)",
    "2-4 motif cells of colors not in {0,5,6} near the 5",
    "1-2 6-anchors at clear distance from the motif",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "no_motif", "no_targets")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "8", "valid": "8..8"},
    "grid_w":         {"type": "int", "default": "8", "valid": "8..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_motif":        {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "2..7"},
    "position_bias":  {"type": "str", "default": "5anchor_motif_plus_6targets",
                       "valid": "5anchor_motif_plus_6targets"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "2..7"},
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
        n_motif_lo, n_motif_hi = 2, 2
        n_anchor_hi = 1
    elif difficulty == "hard":
        n_motif_lo, n_motif_hi = 3, 4
        n_anchor_hi = 2
    else:
        n_motif_lo, n_motif_hi = 2, 4
        n_anchor_hi = 2
    h = w = 8
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    sr = rng.randint(2, h - 3)
    sc = rng.randint(2, w - 3)
    g[sr][sc] = 5
    n_motif = rng.randint(n_motif_lo, n_motif_hi)
    palette = rng.sample([1, 2, 3, 4, 7, 8, 9], 4)
    placed = 0
    while placed < n_motif:
        for _ in range(20):
            dr = rng.randint(-2, 2)
            dc = rng.randint(-2, 2)
            if dr == 0 and dc == 0:
                continue
            r, c = sr + dr, sc + dc
            if 0 <= r < h and 0 <= c < w and g[r][c] == 0:
                g[r][c] = rng.choice(palette)
                placed += 1
                break
        else:
            break
    n_anchors = rng.randint(1, n_anchor_hi)
    placed_anchors = 0
    attempts = 0
    while placed_anchors < n_anchors and attempts < 60:
        attempts += 1
        ar = rng.randint(0, h - 1)
        ac = rng.randint(0, w - 1)
        if g[ar][ac] != 0:
            continue
        if abs(ar - sr) < 3 and abs(ac - sc) < 3:
            continue
        g[ar][ac] = 6
        placed_anchors += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # motif present but no 5-anchor → no reference for motif offsets
        g[3][3] = 4; g[3][4] = 6
        g[5][6] = 6  # 6-target but no 5 to define motif
        return g
    if name == "no_motif":
        # 5-anchor + 6-target but no motif cells → nothing to stamp
        g[3][3] = 5
        g[6][6] = 6
        return g
    if name == "no_targets":
        # 5 + motif but no 6-anchors → motif has nowhere to be stamped
        g[3][3] = 5
        g[2][3] = 4; g[3][4] = 7
        return g
    return g
