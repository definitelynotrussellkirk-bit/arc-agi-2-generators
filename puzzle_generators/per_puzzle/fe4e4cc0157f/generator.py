"""Generator for arc_additional_puzzles_21_set16_bundle:M110 — pick the object with the most interior holes.

Rule: count interior holes per object (using bbox padded by 1; holes
are bg components not touching the padded border). Pick the object
with the most holes (tiebreakers: size DESC, then top-row, then
left-col). Output is its bbox crop.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects (no shapes → rule has nothing to pick);
all_solid (every object has 0 holes → primary key collapses, rule
falls through to size/position tiebreakers); single_object (only 1
→ trivial pick, no contrast in selection).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "fe4e4cc0157f"
VERSION = "1.1.0"
TASK_ID = "fe4e4cc0157f"
SUMMARY = "2-3 distinct-color shapes with distinct hole counts; pick most-holes."

INVARIANTS = [
    "background is 0",
    "2-3 4-connected non-bg objects, each a distinct color",
    "each object has a distinct number of interior holes (0/1/2/4 across the catalog)",
    "objects are non-touching",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "all_solid", "single_object")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..14", "valid": "8..18"},
    "grid_w":            {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "n_objs":            {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":     {"type": "str", "default": "objects_with_distinct_holes",
                          "valid": "objects_with_distinct_holes"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES_0 = [
    ([(0, 0), (0, 1), (1, 0)], 0, 2, 2),
    ([(0, 0), (1, 0), (2, 0)], 0, 3, 1),
    ([(0, 0), (0, 1), (0, 2), (1, 1)], 0, 2, 3),
]
_SHAPES_1 = [
    ([(0, 0), (0, 1), (0, 2),
      (1, 0),         (1, 2),
      (2, 0), (2, 1), (2, 2)], 1, 3, 3),
]
_SHAPES_2 = [
    ([(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
      (1, 0),         (1, 2),         (1, 4),
      (2, 0), (2, 1), (2, 2), (2, 3), (2, 4)], 2, 3, 5),
]
_SHAPES_4 = [
    ([(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
      (1, 0),                 (1, 3),                 (1, 6),
      (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
      (3, 0),                 (3, 3),                 (3, 6),
      (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6)], 4, 5, 7),
]

_HOLE_TIERS = [_SHAPES_0, _SHAPES_1, _SHAPES_2, _SHAPES_4]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 14, 15)
        n = ctx.draw_int("n_objs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 16, 18)
        n = ctx.draw_int("n_objs", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 14)
        w = ctx.draw_int("grid_w", 14, 18)
        n = ctx.draw_int("n_objs", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    tier_idxs = list(range(len(_HOLE_TIERS)))
    rng.shuffle(tier_idxs)
    chosen = tier_idxs[:n]
    palette = list(random_palette(rng, n))
    placed: list[tuple[int, int, int, int]] = []
    for color, tier in zip(palette, chosen):
        cells, _holes, sh, sw = rng.choice(_HOLE_TIERS[tier])
        if sh > h or sw > w: continue
        for _ in range(80):
            r0 = rng.randint(0, h - sh)
            c0 = rng.randint(0, w - sw)
            bb_pad = (r0 - 1, c0 - 1, r0 + sh, c0 + sw)
            if any(bbox_overlaps(bb_pad, p) for p in placed): continue
            paint_at(g, r0, c0, cells, color)
            placed.append((r0, c0, r0 + sh - 1, c0 + sw - 1))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 15
    g = full_grid(h, w, 0)
    if name == "no_objects":
        return g
    if name == "all_solid":
        # Every object has 0 holes — primary key collapses.
        for r in range(2):
            for c in range(2):
                g[1 + r][1 + c] = 1
        for r in range(2):
            for c in range(3):
                g[1 + r][6 + c] = 2
        for r in range(3):
            g[5 + r][3] = 3
        return g
    if name == "single_object":
        # Only 1 object — trivial pick.
        cells, _h, sh, sw = _SHAPES_2[0]
        paint_at(g, 2, 4, cells, 4)
        return g
    return g
