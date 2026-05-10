"""Generator for arc_puzzle_bank_sixth21:M42 — anti-diagonal reflect each blob.

Rule: each blob → reflect cells across the anti-diagonal of its bbox.
For a square bbox: (r, c) → (h-1-c, w-1-r) within bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, non_square_bbox, anti_diag_symmetric.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "538503abef57"
VERSION = "1.1.0"
TASK_ID = "538503abef57"
SUMMARY = "2-3 blobs in square bboxes (≥2x2) where anti-diagonal reflection produces a different shape."

INVARIANTS = [
    "background is 0",
    "blobs have square bboxes (h == w) so anti-diagonal reflection is well-defined",
    "blobs aren't anti-diagonal symmetric (so output != input)",
    "blobs don't 4-touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "non_square_bbox", "anti_diag_symmetric")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "scattered_square_blobs",
                       "valid": "scattered_square_blobs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 9, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    used: set[tuple[int, int]] = set()
    for color in palette:
        for _ in range(40):
            cells = grow_blob(rng, h, w, used, rng.randint(3, 5), max_attempts=20)
            if cells is None:
                continue
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            bb_h = max(rs) - min(rs) + 1
            bb_w = max(cs) - min(cs) + 1
            if bb_h != bb_w:
                continue
            r0, c0 = min(rs), min(cs)
            norm = {(r - r0, c - c0) for r, c in cells}
            n_size = bb_h
            ad = {(n_size - 1 - c, n_size - 1 - r) for r, c in norm}
            if norm == ad:
                continue
            for r, c in cells:
                g[r][c] = color
            used |= cells
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # Empty grid — rule has no blobs to reflect.
        return g
    if name == "non_square_bbox":
        # Blob with non-square bbox — rule's anti-diagonal mapping
        # (h-1-c, w-1-r) requires h == w; for h != w the formula
        # places cells outside the bbox.
        for r, c in [(2, 2), (2, 3), (2, 4), (2, 5)]: g[r][c] = 4
        for r, c in [(6, 6), (6, 7), (7, 6), (8, 6), (8, 7)]: g[r][c] = 6
        return g
    if name == "anti_diag_symmetric":
        # Blob already symmetric across its anti-diagonal — rule's
        # reflection is identity, output equals input.
        for r, c in [(2, 2), (2, 3), (3, 2)]: g[r][c] = 4
        for r, c in [(6, 6), (6, 7), (7, 6)]: g[r][c] = 6
        return g
    return g
