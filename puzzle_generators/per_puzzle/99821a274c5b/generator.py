"""Generator for arc_puzzle_bank_21_set19_bundle:medium_p06 — object column histogram.

Rule: take the first non-bg object. For each column of its bbox, count
how many cells are filled. Output is a bar histogram (height = max
count, columns = bbox width); each column's bar rises from the bottom.

Combinatorial axes (8): grid_h, grid_w, palette_kind, stair_w,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blob, multiple_blobs, uniform_columns.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "99821a274c5b"
VERSION = "1.1.0"
TASK_ID = "99821a274c5b"
SUMMARY = "One staircase blob (cols have strictly increasing fills) — clean histogram."

INVARIANTS = [
    "background is 0",
    "exactly one non-bg blob",
    "the blob is a 'staircase' shape so column counts vary (avoiding identity output)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blob", "multiple_blobs", "uniform_columns")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "stair_w":        {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "single_staircase_blob",
                       "valid": "single_staircase_blob"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        sw = ctx.draw_int("stair_w", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        sw = ctx.draw_int("stair_w", 4, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 12)
        sw = ctx.draw_int("stair_w", 3, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    sh = sw
    r0 = rng.randint(0, h - sh)
    c0 = rng.randint(0, w - sw)
    for k in range(sw):
        for j in range(k + 1):
            r = r0 + sh - 1 - j
            c = c0 + k
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_blob":
        # blank → no blob to histogram
        return g
    if name == "multiple_blobs":
        # 2 separate blobs → "first non-bg blob" is ambiguous
        for k in range(3):
            for j in range(k + 1):
                g[3 - j][1 + k] = 4
        for k in range(3):
            for j in range(k + 1):
                g[6 - j][6 + k] = 6
        return g
    if name == "uniform_columns":
        # solid rectangle → all column counts equal, output is identity (no signal)
        for r in range(2, 5):
            for c in range(3, 7):
                g[r][c] = 4
        return g
    return g
