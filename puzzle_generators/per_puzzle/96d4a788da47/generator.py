"""Generator for arc_puzzle_bank_third21:M17 — slide every blob left.

Rule: each blob shifts horizontally so its bbox left col = 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: blobs_already_at_left, single_blob, blobs_share_rows.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "96d4a788da47"
VERSION = "1.1.0"
TASK_ID = "96d4a788da47"
SUMMARY = "2-3 distinct-color blobs at distinct rows, none touching col 0."

INVARIANTS = [
    "background is 0",
    "every blob's bbox left col >= 1",
    "blobs occupy disjoint row ranges (so sliding doesn't cause collision)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("blobs_already_at_left", "single_blob", "blobs_share_rows")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "right_offset",
                       "valid": "right_offset"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        n = 2
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
        n = 3
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
        n = None
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    # reserve col 0
    for r in range(h):
        used.add((r, 0))
    if n is None:
        n = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    rows_used = set()
    for color in palette:
        for _ in range(40):
            cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=20)
            if cells is None:
                continue
            rs = set(r for r, _ in cells)
            if rs & rows_used:
                continue
            for r, c in cells:
                g[r][c] = color
            used |= cells
            rows_used |= rs
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "blobs_already_at_left":
        # blobs already touch col 0 → sliding is identity, rule effect invisible
        for (r, c) in [(1, 0), (1, 1), (2, 0)]: g[r][c] = 4
        for (r, c) in [(5, 0), (5, 1), (6, 1)]: g[r][c] = 6
        return g
    if name == "single_blob":
        # one blob → sliding works but no comparison across blobs
        for (r, c) in [(3, 5), (3, 6), (4, 5), (4, 6)]: g[r][c] = 4
        return g
    if name == "blobs_share_rows":
        # two blobs share rows → sliding both to col 0 would collide; INVARIANT violated
        for (r, c) in [(3, 4), (3, 5), (4, 4)]: g[r][c] = 4
        for (r, c) in [(3, 8), (4, 8), (4, 9)]: g[r][c] = 6  # same rows as A
        return g
    return g
