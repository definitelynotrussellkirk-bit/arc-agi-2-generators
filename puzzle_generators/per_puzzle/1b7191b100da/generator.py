"""Generator for arc_puzzle_bank_21_set13_bundle:medium_m07 — repeat template by 9-count.

Rule: count of 9s in the grid = N. Crop the (single) non-9 blob's bbox
as template; output is template stamped N times horizontally with 1-col
separator gaps.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_9,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_9s, no_blob, multiple_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "1b7191b100da"
VERSION = "1.1.0"
TASK_ID = "1b7191b100da"
SUMMARY = "1-3 9-markers (count = stamp count) + one non-9 template blob."

INVARIANTS = [
    "background is 0",
    "1-3 9-cells (so stamp count is 1-3)",
    "exactly one non-9 connected blob (the template)",
    "blob is not at the same cells as the 9s",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_9s", "no_blob", "multiple_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_9":            {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "9_markers_with_template_blob",
                       "valid": "9_markers_with_template_blob"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    n_9 = rng.randint(1, 3)
    nine_positions = []
    for _ in range(40):
        if len(nine_positions) >= n_9:
            break
        r = rng.randint(0, h - 1)
        c = rng.randint(0, w - 1)
        if (r, c) not in used:
            nine_positions.append((r, c))
            used.add((r, c))
    for r, c in nine_positions:
        g[r][c] = 9
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
    cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
    if cells is None:
        return g
    for r, c in cells:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_9s":
        # template blob without 9-markers → no stamp count, undefined repeat
        for r, c in [(2, 2), (2, 3), (3, 3)]: g[r][c] = 4
        return g
    if name == "no_blob":
        # 9-markers without template → nothing to stamp
        g[1][1] = 9; g[3][5] = 9; g[6][7] = 9
        return g
    if name == "multiple_blobs":
        # 2 disjoint blobs → "exactly one" precondition fails, ambiguous template
        g[1][1] = 9; g[5][5] = 9
        for r, c in [(2, 2), (2, 3), (3, 3)]: g[r][c] = 4
        for r, c in [(7, 7), (7, 8)]: g[r][c] = 4  # second blob
        return g
    return g
