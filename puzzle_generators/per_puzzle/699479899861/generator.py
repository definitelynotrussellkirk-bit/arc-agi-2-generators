"""Generator for arc_additional_puzzle_bank_volume7:M47 — Fill row×col cross of 2-blobs.

Rule: for each color-2 object, paint cells (r, c) for every distinct r
and every distinct c among its cells, with color 3.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, all_solid_rects, single_cell_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "699479899861"
VERSION = "1.1.0"
TASK_ID = "699479899861"
SUMMARY = "Several non-touching L/T-shaped 2-blobs + one decorative non-2 cell; output paints row×col cross with 3."

INVARIANTS = [
    "between 2 and 3 non-touching 2-blobs with size 3-5",
    "blobs are L or T shaped (not solid rectangles, so cross-product is non-trivial)",
    "one stray non-2 colored cell elsewhere as decoration",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "all_solid_rects", "single_cell_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "spaced_nonrect_blobs",
                       "valid": "spaced_nonrect_blobs"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        n_blobs = ctx.draw_int("n_blobs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
        n_blobs = ctx.draw_int("n_blobs", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 13)
        n_blobs = ctx.draw_int("n_blobs", 2, 3)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used = set()
    for _ in range(n_blobs * 5):
        if n_blobs <= 0: break
        size = rng.randint(3, 5)
        blob = grow_blob(rng, h, w, used, size)
        if blob is None: continue
        rs = {r for r, _ in blob}
        cs = {c for _, c in blob}
        if len(rs) * len(cs) <= len(blob):
            continue
        used |= blob
        for r, c in blob: g[r][c] = 2
        n_blobs -= 1
    for _ in range(20):
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if (r, c) in used: continue
        g[r][c] = 5
        break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # only stray cell, no 2-blobs → rule has no objects to process
        g[5][5] = 5
        return g
    if name == "all_solid_rects":
        # solid 2-rectangles → row×col cross equals the rectangle, rule is identity
        for r in range(2):
            for c in range(2): g[1 + r][1 + c] = 2
        for r in range(2):
            for c in range(3): g[5 + r][5 + c] = 2
        return g
    if name == "single_cell_blobs":
        # 1x1 2-blobs → row×col cross is just the cell, rule is trivial
        g[1][1] = 2
        g[5][7] = 2
        g[8][3] = 2
        return g
    return g
