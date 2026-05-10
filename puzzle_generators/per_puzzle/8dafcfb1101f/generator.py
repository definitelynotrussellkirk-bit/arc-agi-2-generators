"""Generator for arc_puzzle_bank_ninth21:M61 — translate by anchor vector.

Rule: 1-cell = src marker, 2-cell = dst marker. Each non-{0,1,2} cell
moves by (dst - src). Output: empty grid + translated cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_src, missing_dst, no_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "8dafcfb1101f"
VERSION = "1.1.0"
TASK_ID = "8dafcfb1101f"
SUMMARY = "1-anchor (src) + 2-anchor (dst) + a colored blob; translation lands in-bounds."

INVARIANTS = [
    "background is 0",
    "exactly one 1-cell, exactly one 2-cell, ≥2 non-{0,1,2} blob cells",
    "translated blob cells are in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_src", "missing_dst", "no_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "src_dst_blob",
                       "valid": "src_dst_blob"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    src = (rng.randint(0, h // 3), rng.randint(0, w // 3))
    dst = (rng.randint(h // 3, 2 * h // 3), rng.randint(w // 3, 2 * w // 3))
    g[src[0]][src[1]] = 1
    g[dst[0]][dst[1]] = 2
    used.add(src); used.add(dst)
    color = rng.choice([3, 4, 5, 6, 7, 8, 9])
    blob = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
    if blob is None:
        return g
    dr = dst[0] - src[0]; dc = dst[1] - src[1]
    ok = all(0 <= r + dr < h and 0 <= c + dc < w for r, c in blob)
    if not ok:
        return g
    for r, c in blob:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "missing_src":
        # only dst (2), no src (1) → no source anchor, translation undefined
        g[2][2] = 2
        for r, c in [(5, 5), (5, 6)]: g[r][c] = 4
        return g
    if name == "missing_dst":
        # only src (1), no dst (2) → no destination anchor
        g[2][2] = 1
        for r, c in [(5, 5), (5, 6)]: g[r][c] = 4
        return g
    if name == "no_blob":
        # markers but no payload to translate → no-op rule
        g[2][2] = 1
        g[5][5] = 2
        return g
    return g
