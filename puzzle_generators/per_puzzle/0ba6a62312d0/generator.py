"""Generator for arc_puzzle_bank_21_set3:S3_M7 — pivot rotation CW.

Rule: 6-pivot + a single non-{0,6} blob. Output: empty grid + blob
rotated 90° CW around the pivot.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pivot, no_blob, blob_already_4fold_symmetric.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0ba6a62312d0"
VERSION = "1.1.0"
TASK_ID = "0ba6a62312d0"
SUMMARY = "6-pivot at center + a small blob in upper-left whose CW rotation lands in-bounds."

INVARIANTS = [
    "background is 0",
    "exactly one 6-cell at center",
    "non-6 blob in upper-left so rotation lands in lower-left",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pivot", "no_blob", "blob_already_4fold_symmetric")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "1", "valid": "1..1"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "pivot_with_quadrant_blob",
                       "valid": "pivot_with_quadrant_blob"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    pr = h // 2; pc = w // 2
    g[pr][pc] = 6
    color = rng.choice([2, 3, 4, 5, 7, 8])
    cells = []
    for _ in range(40):
        r = rng.randint(0, pr - 1)
        c = rng.randint(0, pc - 1)
        if (r, c) in cells: continue
        rr = pr + (c - pc); cc = pc - (r - pr)
        if not (0 <= rr < h and 0 <= cc < w): continue
        cells.append((r, c))
        if len(cells) >= 3: break
    for r, c in cells:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    pr, pc = h // 2, w // 2
    if name == "no_pivot":
        # cells exist but no 6-pivot → no center of rotation
        g[1][2] = 4
        g[2][3] = 4
        return g
    if name == "no_blob":
        # pivot only → nothing to rotate
        g[pr][pc] = 6
        return g
    if name == "blob_already_4fold_symmetric":
        # cells already 4-fold symmetric around pivot → CW rotation is identity
        g[pr][pc] = 6
        for (r, c) in [(1, 2), (2, 7), (7, 6), (6, 1)]:
            g[r][c] = 4
        return g
    return g
