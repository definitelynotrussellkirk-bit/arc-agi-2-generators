"""Generator for arc_puzzle_bank_twentysecond21:M148 — rebase blob from 1-anchor to 2-anchor.

Rule: 1-anchor is part of a blob (same connected region of cells in
color 5). 2-anchor is elsewhere. Output: move the blob (its 5-cells)
so 1 lands at 2's position. The 1-cell becomes 0; 2 stays 0 in output.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_1, missing_2, no_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "6b6e3acc8a0a"
VERSION = "1.1.0"
TASK_ID = "6b6e3acc8a0a"
SUMMARY = "1-anchor (inside blob) + 5-blob attached + 2-anchor elsewhere; rebased blob in-bounds."

INVARIANTS = [
    "background is 0",
    "exactly one 1-cell, one 2-cell, ≥2 5-cells in a connected blob 4-touching the 1",
    "rebased blob (shifted by 2-1) is in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_1", "missing_2", "no_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "2", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "1_inside_5_blob_2_elsewhere",
                       "valid": "1_inside_5_blob_2_elsewhere"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    # 1-anchor in upper-left
    one_r = rng.randint(1, h // 2 - 1)
    one_c = rng.randint(1, w // 2 - 1)
    g[one_r][one_c] = 1
    used = {(one_r, one_c)}
    # 5-blob next to the 1
    g[one_r][one_c + 1] = 5
    g[one_r + 1][one_c + 1] = 5
    used |= {(one_r, one_c + 1), (one_r + 1, one_c + 1)}
    # 2-anchor in lower-right
    two_r = rng.randint(h // 2 + 1, h - 2)
    two_c = rng.randint(w // 2 + 1, w - 2)
    if g[two_r][two_c] == 0:
        g[two_r][two_c] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "missing_1":
        # blob + 2-anchor, no 1 → no rebase source defined
        for r, c in [(2, 2), (3, 2)]: g[r][c] = 5
        g[5][6] = 2
        return g
    if name == "missing_2":
        # 1-anchor + blob, no 2 → no rebase target defined
        g[2][2] = 1
        for r, c in [(2, 3), (3, 3)]: g[r][c] = 5
        return g
    if name == "no_blob":
        # 1 + 2 markers but no 5-blob → nothing to rebase
        g[2][2] = 1
        g[5][6] = 2
        return g
    return g
