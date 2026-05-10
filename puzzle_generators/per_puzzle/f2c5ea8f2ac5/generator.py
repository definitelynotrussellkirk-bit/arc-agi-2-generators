"""Generator for arc_puzzle_bank_third21:M19 — crop to active area.

Rule: crop the grid to the bbox of all non-zero cells (smaller output).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, full_grid_active, blob_at_border.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "f2c5ea8f2ac5"
VERSION = "1.1.0"
TASK_ID = "f2c5ea8f2ac5"
SUMMARY = "Sparse content surrounded by ≥1 row of all-zero padding on every side."

INVARIANTS = [
    "background is 0",
    "≥1 all-zero row at top, bottom, ≥1 all-zero col at left, right",
    "≥1 non-zero blob inside the active area",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "full_grid_active", "blob_at_border")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "2", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "interior_padded",
                       "valid": "interior_padded"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    for r in range(h):
        used.add((r, 0)); used.add((r, w - 1))
    for c in range(w):
        used.add((0, c)); used.add((h - 1, c))
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
    for color in palette:
        cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
        if cells is None:
            continue
        for r, c in cells:
            g[r][c] = color
        used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # blank → no active area, rule undefined
        return g
    if name == "full_grid_active":
        # active cells span whole grid → crop is identity
        for r in range(h):
            for c in range(w):
                if (r + c) % 2 == 0: g[r][c] = 4
                else: g[r][c] = 6
        return g
    if name == "blob_at_border":
        # blob touches the outer border → no padding margin, crop is full grid
        for c in range(w): g[0][c] = 4
        g[3][3] = 6; g[4][4] = 6
        return g
    return g
