"""Generator for v1_e_m_h_keys:M7 — replace each 3×3 hollow ring with a single dot at its center.

Rule: each 3×3 hollow ring object becomes a single same-color dot at
its center cell.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rings,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rings, solid_3x3, ring_with_filled_center.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import RING_3X3
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "37aaf7d1e52e"
VERSION = "1.1.0"
TASK_ID = "37aaf7d1e52e"
SUMMARY = "1-2 3×3 hollow rings in distinct colors."

INVARIANTS = [
    "background is 0",
    "1-2 3×3 hollow ring objects (8 cells each) in distinct non-bg colors",
    "rings don't touch each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rings", "solid_3x3", "ring_with_filled_center")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rings":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "isolated_3x3_rings",
                       "valid": "isolated_3x3_rings"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..3"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
        n = ctx.draw_int("n_rings", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        n = ctx.draw_int("n_rings", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 7, 10)
        n = ctx.draw_int("n_rings", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = list(random_palette(rng, n))
    placed: list[tuple[int, int, int, int]] = []
    for color in palette:
        for _ in range(80):
            r0 = rng.randint(0, h - 3)
            c0 = rng.randint(0, w - 3)
            bb_pad = (r0 - 1, c0 - 1, r0 + 3, c0 + 3)
            if any(bbox_overlaps(bb_pad, p) for p in placed): continue
            paint_at(g, r0, c0, RING_3X3, color)
            placed.append((r0, c0, r0 + 2, c0 + 2))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_rings":
        # blank → no rings to compress to dots
        return g
    if name == "solid_3x3":
        # solid 3×3 (no hollow center) → not a ring, rule won't fire
        for r in range(2, 5):
            for c in range(2, 5):
                g[r][c] = 4
        return g
    if name == "ring_with_filled_center":
        # ring shape but center cell is non-zero → not "hollow"
        for r in range(2, 5):
            for c in range(2, 5):
                g[r][c] = 4
        # don't clear center → stays solid; this is the failure mode
        return g
    return g
