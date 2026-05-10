"""Generator for arc_puzzle_bank_21_set9_s:S9_M3 — anchor-vector copy.

Rule: 3 = src anchor, 4 = dst anchor, 2 = template. Output: empty grid
+ template translated by (dst-src) painted in 8 + dst itself painted 4.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchors, no_template, src_equals_dst.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "327c3478236b"
VERSION = "1.1.0"
TASK_ID = "327c3478236b"
SUMMARY = "3-anchor src + 4-anchor dst + 2-blob template; translated copy lands in-bounds."

INVARIANTS = [
    "background is 0",
    "exactly one 3-cell, exactly one 4-cell, ≥2 2-cells in a connected blob",
    "translated cells are in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchors", "no_template", "src_equals_dst")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "src_dst_with_template",
                       "valid": "src_dst_with_template"},
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
    src = (rng.randint(0, h // 3), rng.randint(0, w // 2))
    dst = (rng.randint(h // 3, 2 * h // 3), rng.randint(w // 2, w - 1))
    g[src[0]][src[1]] = 3
    g[dst[0]][dst[1]] = 4
    used.add(src); used.add(dst)
    blob = grow_blob(rng, h, w, used, rng.randint(3, 4), max_attempts=80)
    if blob is None:
        return g
    for r, c in blob:
        g[r][c] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_anchors":
        # template only, no 3 or 4 anchors → no translation vector
        g[3][3] = 2; g[3][4] = 2; g[4][3] = 2
        return g
    if name == "no_template":
        # anchors but no 2-template → nothing to translate
        g[1][1] = 3
        g[5][6] = 4
        return g
    if name == "src_equals_dst":
        # both anchors at the same cell → vector is zero, rule is identity
        g[3][3] = 3
        g[3][3] = 4   # overwrites the 3 → ambiguous anchor
        g[5][5] = 2; g[5][6] = 2; g[6][5] = 2
        return g
    return g
