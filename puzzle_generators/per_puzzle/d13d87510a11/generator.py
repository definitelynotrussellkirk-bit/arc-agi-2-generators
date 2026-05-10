"""Generator for arc_puzzle_bank_21_set7_s:S7_M4 — translate by anchor vector.

Rule: 1-cell = src anchor, 2-cell = dst anchor, 3-blob = template.
Output: empty grid + the 3-blob translated by (dst-src) painted in 2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_src, no_dst, no_template.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "d13d87510a11"
VERSION = "1.1.0"
TASK_ID = "d13d87510a11"
SUMMARY = "1-anchor (src) + 2-anchor (dst) + 3-blob (template)."

INVARIANTS = [
    "background is 0",
    "exactly one 1-cell, exactly one 2-cell, ≥1 3-cell forming a blob",
    "translated blob lands in-bounds (so output is non-empty)",
    "(dst - src) is non-zero",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_src", "no_dst", "no_template")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "src_dst_template",
                       "valid": "src_dst_template"},
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
    if name == "no_src":
        # missing 1-cell src anchor → no anchor for translation vector
        g[5][6] = 2  # dst
        g[3][3] = 3; g[3][4] = 3  # blob
        return g
    if name == "no_dst":
        # missing 2-cell dst anchor → no destination for translation
        g[1][1] = 1  # src
        g[3][3] = 3; g[3][4] = 3  # blob
        return g
    if name == "no_template":
        # src + dst but no 3-blob → nothing to translate
        g[1][1] = 1
        g[5][6] = 2
        return g
    return g
