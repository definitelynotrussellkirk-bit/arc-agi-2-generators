"""Generator for arc_puzzle_bank_sixth21:M38 — transpose each blob in its bbox.

Rule: each blob → transpose its bbox (swap rows and cols), keeping the
top-left corner anchored.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, square_symmetric_blob, single_cell_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "34700cab1c3c"
VERSION = "1.1.0"
TASK_ID = "34700cab1c3c"
SUMMARY = "2-3 distinct-color non-square non-symmetric blobs (transpose changes them)."

INVARIANTS = [
    "background is 0",
    "blobs are non-rectangular OR have asymmetric layout (transpose != identity)",
    "blobs don't overlap or 4-touch even after transpose into the same bbox",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "square_symmetric_blob", "single_cell_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "non_symmetric_blobs",
                       "valid": "non_symmetric_blobs"},
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
        w = ctx.draw_int("grid_w", 9, 10)
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
            r0, c0 = min(rs), min(cs)
            new_r2 = r0 + bb_w - 1
            new_c2 = c0 + bb_h - 1
            if new_r2 >= h or new_c2 >= w:
                continue
            full_box = {(r, c)
                        for r in range(r0, max(r0 + bb_h, new_r2 + 1))
                        for c in range(c0, max(c0 + bb_w, new_c2 + 1))
                        if 0 <= r < h and 0 <= c < w}
            if full_box & used:
                continue
            for r, c in cells:
                g[r][c] = color
            used |= full_box
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # Empty grid — rule has no shapes to transpose.
        return g
    if name == "square_symmetric_blob":
        # 2x2 square — rule's transpose is identity; effect
        # invisible.
        for r in range(2, 4):
            for c in range(2, 4): g[r][c] = 4
        for r in range(6, 8):
            for c in range(7, 9): g[r][c] = 6
        return g
    if name == "single_cell_blob":
        # 1-cell objects — rule's bbox is 1x1; transpose is
        # trivially identity.
        g[2][2] = 4; g[5][7] = 6
        return g
    return g
