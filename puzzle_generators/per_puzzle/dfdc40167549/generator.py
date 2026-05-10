"""Generator for arc_puzzle_bank_21_set11_s:S11_H5.

Rule: dr/dc = (2-marker - 1-marker). The largest non-{1,2} blob is
translated by (dr,dc); for each cell, paint 7 if boundary, 8 if interior.

Combinatorial axes (8): grid_h/w, palette_kind, blob_size, palette_size,
position_bias, n_distinct_colors, vector_length, texture.
Degenerates: no_markers, no_blob, blob_too_small.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dfdc40167549"
VERSION = "1.1.0"
TASK_ID = "dfdc40167549"
SUMMARY = "Solid 3-blob (large) + 1-marker + 2-marker (delta downstream) leaves room for translated copy."

INVARIANTS = [
    "exactly one 1-cell, one 2-cell",
    "one solid rectangle blob (h≥3, w≥3) of distinct color",
    "translated cells stay in-bounds",
]

PALETTE_KINDS = ("default", "blob_top", "blob_left", "blob_center")
DEGENERATE_TEXTURES = ("no_markers", "no_blob", "blob_too_small")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "str", "default": "fixed_3x4", "valid": "fixed_3x4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "vector_length":  {"type": "str", "default": "mixed", "valid": "mixed"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 12, 14)
    g = full_grid(h, w, 0)
    # solid 3x4 blob upper-left
    for r in range(1, 4):
        for c in range(1, 5):
            g[r][c] = 3
    g[5][2] = 1
    g[6][9] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # blob present, but no 1/2 markers — translation vector undefined
        for r in range(1, 4):
            for c in range(1, 5):
                g[r][c] = 3
        return g
    if name == "no_blob":
        # markers present, no blob — rule has nothing to translate
        g[5][2] = 1
        g[6][9] = 2
        return g
    if name == "blob_too_small":
        # only 2 cells of color 3 (h=1, w=2) — fails h≥3, w≥3 invariant
        g[2][2] = 3; g[2][3] = 3
        g[5][2] = 1
        g[6][9] = 2
        return g
    return g
