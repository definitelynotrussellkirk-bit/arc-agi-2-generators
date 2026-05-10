"""Generator for arc_additional_puzzles_21_set12_bundle:M83 — sort objects by interior-hole count.

Rule: count "holes" (non-border-touching bg components) inside each
object's bbox crop. Sort objects ascending by hole count (with
tiebreakers), then stack their crops vertically at column 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects, all_zero_holes, equal_holes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "edb34dd65185"
VERSION = "1.1.0"
TASK_ID = "edb34dd65185"
SUMMARY = "2-3 distinct-color shapes with distinct interior-hole counts (0/1/2)."

INVARIANTS = [
    "background is 0",
    "2-3 4-connected non-bg objects, each a distinct color",
    "each object has a distinct number of interior holes (0, 1, or 2)",
    "objects are non-touching (≥1 bg gap between bboxes)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "all_zero_holes", "equal_holes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "12..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "scattered_distinct_holes",
                       "valid": "scattered_distinct_holes"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES_0 = [
    ([(0, 0), (0, 1), (1, 0)], 0, 2, 2),
    ([(0, 0), (0, 1), (0, 2), (1, 1)], 0, 2, 3),
    ([(0, 0), (1, 0), (2, 0)], 0, 3, 1),
    ([(0, 0), (0, 1), (0, 2), (1, 0)], 0, 2, 3),
]
_SHAPES_1 = [
    ([(0, 0), (0, 1), (0, 2),
      (1, 0),         (1, 2),
      (2, 0), (2, 1), (2, 2)], 1, 3, 3),
    ([(0, 0), (0, 1), (0, 2), (0, 3),
      (1, 0),                 (1, 3),
      (2, 0), (2, 1), (2, 2), (2, 3)], 1, 3, 4),
]
_SHAPES_2 = [
    ([(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
      (1, 0),         (1, 2),         (1, 4),
      (2, 0), (2, 1), (2, 2), (2, 3), (2, 4)], 2, 3, 5),
    ([(0, 0), (0, 1), (0, 2),
      (1, 0),         (1, 2),
      (2, 0), (2, 1), (2, 2),
      (3, 0),         (3, 2),
      (4, 0), (4, 1), (4, 2)], 2, 5, 3),
]

_SHAPE_BUCKETS = [_SHAPES_0, _SHAPES_1, _SHAPES_2]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 14, 15)
        n = ctx.draw_int("n_objects", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 16, 20)
        w = ctx.draw_int("grid_w", 16, 19)
        n = ctx.draw_int("n_objects", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 14, 18)
        w = ctx.draw_int("grid_w", 14, 18)
        n = ctx.draw_int("n_objects", 2, 3)
    rng = ctx.draw_rng("layout")
    colors = list(random_palette(rng, n))
    g = full_grid(h, w, 0)
    bucket_idxs = list(range(3))
    rng.shuffle(bucket_idxs)
    chosen = bucket_idxs[:n]
    placed_bboxes: list[tuple[int, int, int, int]] = []
    for color, b in zip(colors, chosen):
        cells, _holes, sh, sw = rng.choice(_SHAPE_BUCKETS[b])
        for _ in range(60):
            r0 = rng.randint(0, h - sh)
            c0 = rng.randint(0, w - sw)
            bb = (r0 - 1, c0 - 1, r0 + sh, c0 + sw)
            if any(bbox_overlaps(bb, p) for p in placed_bboxes): continue
            paint_at(g, r0, c0, cells, color)
            placed_bboxes.append((r0, c0, r0 + sh - 1, c0 + sw - 1))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 16, 16
    g = full_grid(h, w, 0)
    if name == "no_objects":
        return g
    if name == "all_zero_holes":
        # All solid shapes — sort by hole-count is degenerate (all 0).
        paint_at(g, 1, 1, _SHAPES_0[0][0], 4)
        paint_at(g, 5, 1, _SHAPES_0[1][0], 5)
        paint_at(g, 9, 1, _SHAPES_0[2][0], 6)
        return g
    if name == "equal_holes":
        # All shapes have same hole count — sort tie-break ambiguous.
        paint_at(g, 1, 1, _SHAPES_1[0][0], 4)
        paint_at(g, 5, 1, _SHAPES_1[0][0], 5)
        paint_at(g, 9, 1, _SHAPES_1[0][0], 6)
        return g
    return g
