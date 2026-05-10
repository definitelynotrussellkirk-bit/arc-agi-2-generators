"""Generator for arc_puzzle_bank_21_set10_e:medium_j10 — Largest blob row-count bar chart.

Rule: largest blob (by size); crop to bbox; for each row of crop, count
non-zero cells. Output: row r has obj-color for first count_r cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape_variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blob, multiple_equal_blobs, uniform_rows.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "399cf1e9e577"
VERSION = "1.1.0"
TASK_ID = "399cf1e9e577"
SUMMARY = "Single asymmetric color blob in interior; output is row-count bar chart of its bbox."

INVARIANTS = [
    "exactly one connected blob",
    "blob has varied row-counts (so output isn't trivially uniform)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blob", "multiple_equal_blobs", "uniform_rows")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_variant":  {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "single_asymmetric_blob",
                       "valid": "single_asymmetric_blob"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    shapes = [
        [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
    ]
    shape = rng.choice(shapes)
    bh = max(r for r, _ in shape) + 1
    bw = max(c for _, c in shape) + 1
    r0 = rng.randint(1, h - bh - 1)
    c0 = rng.randint(1, w - bw - 1)
    for dr, dc in shape:
        g[r0 + dr][c0 + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_blob":
        # blank → no blob to histogram
        return g
    if name == "multiple_equal_blobs":
        # 2 blobs of same size → "largest" is ambiguous
        for r, c in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 4
        for r, c in [(5, 5), (5, 6), (6, 5)]: g[r][c] = 6
        return g
    if name == "uniform_rows":
        # solid rectangle → all row counts equal, histogram is identity (no signal)
        for r in range(2, 5):
            for c in range(2, 6):
                g[r][c] = 4
        return g
    return g
