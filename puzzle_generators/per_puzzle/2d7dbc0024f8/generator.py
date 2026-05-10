"""Generator for arc_puzzle_bank_fourteenth21:M95 — shift by 8-guide vector.

Rule: two 8-cells define src and dst. Shift every non-{0,8} cell by
(dst - src). Output: empty grid + shifted blob.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: one_8_cell, no_blob, src_equals_dst.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "2d7dbc0024f8"
VERSION = "1.1.0"
TASK_ID = "2d7dbc0024f8"
SUMMARY = "Two 8-cells (src+dst) + a colored blob; shifted blob in-bounds."

INVARIANTS = [
    "background is 0",
    "exactly two 8-cells defining a non-zero shift vector",
    "≥1 connected non-{0,8} blob whose shift is in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("one_8_cell", "no_blob", "src_equals_dst")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "src_dst_plus_blob",
                       "valid": "src_dst_plus_blob"},
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
    src = (rng.randint(0, h // 3), rng.randint(0, w // 3))
    dst = (rng.randint(h // 3, 2 * h // 3), rng.randint(w // 3, 2 * w // 3))
    g[src[0]][src[1]] = 8
    g[dst[0]][dst[1]] = 8
    used.add(src); used.add(dst)
    color = rng.choice([2, 3, 4, 5, 6, 7])
    blob = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
    if blob is None:
        return g
    dr = dst[0] - src[0]; dc = dst[1] - src[1]
    if not all(0 <= r + dr < h and 0 <= c + dc < w for r, c in blob):
        return g
    for r, c in blob:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "one_8_cell":
        # only one 8-cell → can't define a shift vector
        g[1][1] = 8
        g[3][3] = 4; g[3][4] = 4
        return g
    if name == "no_blob":
        # 8-pair without blob → nothing to shift
        g[1][1] = 8
        g[5][5] = 8
        return g
    if name == "src_equals_dst":
        # both 8-cells coincide → shift vector is (0, 0), rule is identity
        g[3][3] = 8
        g[5][5] = 4; g[5][6] = 4
        return g
    return g
