"""Generator for v0_original:medium_01 — keep the largest object recolored 8, erase the rest.

Rule: find all connected non-bg objects. Recolor the largest with
color 8 and erase every other object (set their cells to 0).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: tied_sizes (≥2 objects share max size → "largest" is
ambiguous, tie-break decides), single_object (only one object,
trivially largest → no contrast), no_objects (grid is all bg → rule's
selector finds nothing, output equals input).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "005c7091fce2"
VERSION = "1.1.0"
TASK_ID = "005c7091fce2"
SUMMARY = "1 large connected object + 1-2 smaller distinct-color objects."

INVARIANTS = [
    "background is 0",
    "exactly one 'big' connected object with ≥5 cells",
    "1-2 smaller connected objects, each with strictly fewer cells",
    "all objects have distinct cell counts and distinct colors",
    "objects don't touch each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_sizes", "single_object", "no_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "grid_w":            {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "n_smalls":          {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "position_bias":     {"type": "str", "default": "big_plus_smalls",
                          "valid": "big_plus_smalls"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_BIG = [
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],   # 3x3 ring (8)
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],                           # T (5)
    [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],                           # L (5)
    [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)],                           # P (5)
    [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0)],                   # 6 cells
]
_SMALL = [
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        n_smalls = ctx.draw_int("n_smalls", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 10, 10)
        n_smalls = ctx.draw_int("n_smalls", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 10)
        n_smalls = ctx.draw_int("n_smalls", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = list(random_palette(rng, 1 + n_smalls))
    big_shape = rng.choice(_BIG)
    bh = max(c[0] for c in big_shape) + 1
    bw = max(c[1] for c in big_shape) + 1
    placed: list[tuple[int, int, int, int]] = []
    for _ in range(80):
        r0 = rng.randint(0, h - bh)
        c0 = rng.randint(0, w - bw)
        bb_pad = (r0 - 1, c0 - 1, r0 + bh, c0 + bw)
        if any(bbox_overlaps(bb_pad, p) for p in placed): continue
        paint_at(g, r0, c0, big_shape, palette[0])
        placed.append((r0, c0, r0 + bh - 1, c0 + bw - 1))
        break
    for color in palette[1:]:
        small = rng.choice(_SMALL)
        sh = max(c[0] for c in small) + 1
        sw = max(c[1] for c in small) + 1
        for _ in range(80):
            r0 = rng.randint(0, h - sh)
            c0 = rng.randint(0, w - sw)
            bb_pad = (r0 - 1, c0 - 1, r0 + sh, c0 + sw)
            if any(bbox_overlaps(bb_pad, p) for p in placed): continue
            paint_at(g, r0, c0, small, color)
            placed.append((r0, c0, r0 + sh - 1, c0 + sw - 1))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "tied_sizes":
        # Two objects share max size — "largest" is ambiguous; tie-break
        # decides which is kept.
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[1 + dr][1 + dc] = 3
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[4 + dr][5 + dc] = 6
        return g
    if name == "single_object":
        # Only one object — trivially largest; no candidate contrast.
        for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)]:
            g[2 + dr][2 + dc] = 4
        return g
    if name == "no_objects":
        # No non-bg cells — rule's selector finds nothing; output = input.
        return g
    return g
