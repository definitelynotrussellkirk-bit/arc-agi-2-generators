"""Generator for v1_e_m_h_keys:M1 — recolor 1×N (or N×1) line objects to 8.

Rule: each connected non-bg object is examined: if it's a single-row
or single-column line (h=1 or w=1 with size ≥2), recolor to 8.
Other shapes (multi-row multi-col blobs) stay.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_lines, no_blobs, all_lines.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "40f42915c6c4"
VERSION = "1.1.0"
TASK_ID = "40f42915c6c4"
SUMMARY = "1 line object (1xN or Nx1) + 1-2 multi-row blob objects, distinct colors."

INVARIANTS = [
    "background is 0",
    "exactly one line object (1×N or N×1, N ≥ 2) of one non-bg, non-8 color",
    "1-2 multi-row blobs (h ≥ 2 and w ≥ 2) of distinct non-bg, non-8 colors",
    "objects don't touch each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_lines", "no_blobs", "all_lines")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "line_plus_blobs",
                       "valid": "line_plus_blobs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_LINES = [
    [(0, 0), (0, 1)],
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (1, 0)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (1, 0), (2, 0), (3, 0)],
]
_BLOBS = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        n_blobs = ctx.draw_int("n_blobs", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        n_blobs = ctx.draw_int("n_blobs", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 8, 10)
        n_blobs = ctx.draw_int("n_blobs", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = list(random_palette(rng, 1 + n_blobs, exclude={8}))
    line_shape = rng.choice(_LINES)
    sh = max(c[0] for c in line_shape) + 1
    sw = max(c[1] for c in line_shape) + 1
    placed: list[tuple[int, int, int, int]] = []
    for _ in range(80):
        r0 = rng.randint(0, h - sh)
        c0 = rng.randint(0, w - sw)
        bb_pad = (r0 - 1, c0 - 1, r0 + sh, c0 + sw)
        if any(bbox_overlaps(bb_pad, p) for p in placed): continue
        paint_at(g, r0, c0, line_shape, palette[0])
        placed.append((r0, c0, r0 + sh - 1, c0 + sw - 1))
        break
    for color in palette[1:]:
        blob = rng.choice(_BLOBS)
        bh = max(c[0] for c in blob) + 1
        bw = max(c[1] for c in blob) + 1
        for _ in range(80):
            r0 = rng.randint(0, h - bh)
            c0 = rng.randint(0, w - bw)
            bb_pad = (r0 - 1, c0 - 1, r0 + bh, c0 + bw)
            if any(bbox_overlaps(bb_pad, p) for p in placed): continue
            paint_at(g, r0, c0, blob, color)
            placed.append((r0, c0, r0 + bh - 1, c0 + bw - 1))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_lines":
        # only multi-cell blobs, no lines → rule fires zero times
        for (r, c) in [(1, 1), (1, 2), (2, 1), (2, 2)]: g[r][c] = 4
        for (r, c) in [(4, 5), (4, 6), (5, 5), (5, 6)]: g[r][c] = 6
        return g
    if name == "no_blobs":
        # only lines, no multi-row blobs → all objects recolored to 8 (uniform)
        for c in range(1, 5): g[1][c] = 4
        for r in range(3, 6): g[r][7] = 6
        return g
    if name == "all_lines":
        # every object is a line → all recolored, output uniform color
        for c in range(1, 4): g[1][c] = 4
        for c in range(2, 6): g[3][c] = 6
        for r in range(2, 5): g[r][8] = 3
        return g
    return g
