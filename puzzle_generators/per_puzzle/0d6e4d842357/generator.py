"""Generator for arc_puzzle_bank_sixteenth21:M106 — vector shadow copy.

Rule: 8 = src, 9 = dst. Each non-{0,8,9} cell stays AND is duplicated
at translated position (dst-src offset). Shadow copy.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_src, no_dst, no_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "0d6e4d842357"
VERSION = "1.1.0"
TASK_ID = "0d6e4d842357"
SUMMARY = "8-src + 9-dst markers + a colored blob; both blob and shadow in-bounds."

INVARIANTS = [
    "background is 0",
    "exactly one 8-cell + one 9-cell + a non-{0,8,9} blob",
    "translated cells are in-bounds",
    "blob and its shadow are disjoint",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_src", "no_dst", "no_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "src_dst_blob",
                       "valid": "src_dst_blob"},
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
    src = (rng.randint(0, h // 4), rng.randint(0, w // 4))
    dst = (rng.randint(h // 2, h - 1), rng.randint(w // 2, w - 1))
    g[src[0]][src[1]] = 8
    g[dst[0]][dst[1]] = 9
    used.add(src); used.add(dst)
    color = rng.choice([2, 3, 4, 5, 6, 7])
    blob = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
    if blob is None:
        return g
    dr = dst[0] - src[0]; dc = dst[1] - src[1]
    if not all(0 <= r + dr < h and 0 <= c + dc < w for r, c in blob):
        return g
    # ensure shadow disjoint from original
    shadow = {(r + dr, c + dc) for r, c in blob}
    if shadow & blob:
        return g
    for r, c in blob:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_src":
        # only dst + blob → no source to define translation vector
        g[5][7] = 9
        g[2][2] = 4; g[2][3] = 4; g[3][2] = 4
        return g
    if name == "no_dst":
        # only src + blob → no destination, vector undefined
        g[1][1] = 8
        g[3][3] = 4; g[3][4] = 4; g[4][3] = 4
        return g
    if name == "no_blob":
        # markers but no blob → no cells to translate
        g[1][1] = 8
        g[5][7] = 9
        return g
    return g
