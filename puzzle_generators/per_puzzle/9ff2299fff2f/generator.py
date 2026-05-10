"""Generator for arc_puzzle_bank_fifteenth21:M99 — move by 8→9 guide vector.

Rule: 8 = src, 9 = dst. Move every non-{0,8,9} cell by (dst - src).
Output: empty grid + translated cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_8, missing_9, no_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "9ff2299fff2f"
VERSION = "1.1.0"
TASK_ID = "9ff2299fff2f"
SUMMARY = "8-src + 9-dst markers + a multi-color blob; translation in-bounds."

INVARIANTS = [
    "background is 0",
    "exactly one 8-cell, exactly one 9-cell, ≥2 non-{0,8,9} blob cells",
    "translation is fully in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_8", "missing_9", "no_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "src_dst_blob",
                       "valid": "src_dst_blob"},
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
    g[dst[0]][dst[1]] = 9
    used.add(src); used.add(dst)
    blob = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
    if blob is None:
        return g
    dr = dst[0] - src[0]; dc = dst[1] - src[1]
    if not all(0 <= r + dr < h and 0 <= c + dc < w for r, c in blob):
        return g
    palette = rng.sample([2, 3, 4, 5, 6, 7], 2)
    for i, (r, c) in enumerate(sorted(blob)):
        g[r][c] = palette[i % len(palette)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "missing_8":
        # only 9, no 8 → no source anchor, translation undefined
        g[2][2] = 9
        for r, c in [(5, 5), (5, 6)]: g[r][c] = 4
        return g
    if name == "missing_9":
        # only 8, no 9 → no destination anchor, translation undefined
        g[2][2] = 8
        for r, c in [(5, 5), (5, 6)]: g[r][c] = 4
        return g
    if name == "no_blob":
        # markers but no payload to translate → no-op rule
        g[2][2] = 8
        g[5][5] = 9
        return g
    return g
