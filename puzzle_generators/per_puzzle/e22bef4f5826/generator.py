"""Generator for arc_puzzle_bank_21_set7:medium_g13 — checker-fill each bbox.

Rule: each blob → fill its bbox with a checker pattern in same color
(cells where (r-r1+c-c1)%2 == 0).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: single_cell_blobs, already_checker, blob_overlap.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "e22bef4f5826"
VERSION = "1.1.0"
TASK_ID = "e22bef4f5826"
SUMMARY = "2-3 distinct-color blobs whose checker bbox-fill differs from the input."

INVARIANTS = [
    "background is 0",
    "blobs are non-rectangular OR small (so checker-fill differs from input)",
    "blobs don't overlap or 4-touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_cell_blobs", "already_checker", "blob_overlap")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_blobs",
                       "valid": "spaced_blobs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 7, 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    used: set[tuple[int, int]] = set()
    for color in palette:
        cells = grow_blob(rng, h, w, used, rng.randint(2, 3), max_attempts=80)
        if cells is None:
            continue
        for r, c in cells:
            g[r][c] = color
        used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "single_cell_blobs":
        # 1x1 blobs → bbox is single cell, checker fill is trivial (same as input)
        g[1][2] = 4; g[3][5] = 6; g[5][7] = 3
        return g
    if name == "already_checker":
        # blob already has checker pattern in its bbox → rule is identity
        for (r, c) in [(1, 1), (1, 3), (2, 2), (3, 1), (3, 3)]: g[r][c] = 4
        return g
    if name == "blob_overlap":
        # two blobs share cells → "each blob's bbox" is ambiguous in overlap
        for (r, c) in [(1, 1), (1, 2), (2, 2)]: g[r][c] = 4
        for (r, c) in [(2, 2), (2, 3), (3, 3)]: g[r][c] = 6  # overlaps at (2,2)
        return g
    return g
