"""Generator for arc_puzzle_bank_twentieth21:M136 — repeat prototype by header K.

Rule: row 0 has K 1-markers + a single non-1 prototype blob below.
Output: prototype repeated K times horizontally with 1-col gap.

Combinatorial axes (8): grid_h, grid_w, palette_kind, K,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, no_prototype, K_too_large.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "cb439f1b5f4a"
VERSION = "1.1.0"
TASK_ID = "cb439f1b5f4a"
SUMMARY = "Row 0 has K 1-markers (K=2..3) + a single non-1 blob below."

INVARIANTS = [
    "background is 0",
    "row 0 has 2-3 1-cells",
    "exactly one non-1 connected blob below row 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_prototype", "K_equals_one")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "K":              {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "row0_K_markers_with_blob_below",
                       "valid": "row0_K_markers_with_blob_below"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        w = ctx.draw_int("grid_w", 7, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    K = rng.randint(2, 3)
    cols = rng.sample(range(w), K)
    for c in cols:
        g[0][c] = 1
    used = {(0, c) for c in cols}
    for c in range(w):
        used.add((1, c))
    color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
    if cells:
        for r, c in cells:
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 9
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # row 0 empty → K = 0, no copies to make
        g[3][3] = 4; g[3][4] = 4
        return g
    if name == "no_prototype":
        # markers but no blob → K copies of nothing
        g[0][1] = 1; g[0][3] = 1; g[0][5] = 1
        return g
    if name == "K_equals_one":
        # only 1 marker → output identical to prototype (K = 1, no real repetition)
        g[0][2] = 1
        g[3][3] = 4; g[3][4] = 4
        return g
    return g
