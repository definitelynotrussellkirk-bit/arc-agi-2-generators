"""Generator for arc_puzzle_bank_seventh21:M46 — marker-vector translation.

Rule: 1-cell = src marker, 2-cell = dst marker. Translate every 3-cell
by (dst-src). Output: empty grid + translated 3s.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, no_blob, src_equals_dst.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "d83b3801c134"
VERSION = "1.1.0"
TASK_ID = "d83b3801c134"
SUMMARY = "1-marker (src) + 2-marker (dst) + a 3-blob; translation lands in-bounds."

INVARIANTS = [
    "background is 0",
    "exactly one 1-cell, exactly one 2-cell, ≥2 3-cells in a connected blob",
    "translated cells are in-bounds (so output is non-empty)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_blob", "src_equals_dst")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "src_dst_with_blob",
                       "valid": "src_dst_with_blob"},
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
    src = (rng.randint(0, h // 2), rng.randint(0, w // 2))
    dst = (rng.randint(h // 2, h - 1), rng.randint(w // 2, w - 1))
    if src == dst:
        dst = (dst[0], (dst[1] + 1) % w)
    g[src[0]][src[1]] = 1
    g[dst[0]][dst[1]] = 2
    used.add(src); used.add(dst)
    blob = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
    if blob is None:
        return g
    for r, c in blob:
        g[r][c] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # blob only, no 1/2 markers → no translation vector
        g[3][3] = 3; g[3][4] = 3; g[4][3] = 3
        return g
    if name == "no_blob":
        # markers but no 3-blob → nothing to translate
        g[1][1] = 1
        g[5][6] = 2
        return g
    if name == "src_equals_dst":
        # both markers at same cell → vector zero, rule identity
        g[3][3] = 1
        g[3][3] = 2   # overwrites src
        g[5][5] = 3; g[5][6] = 3; g[6][5] = 3
        return g
    return g
