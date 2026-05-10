"""Generator for additional_bank:E2.

Rule: blue components touching the top border are recolored to yellow.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_top_touching, all_top_touching, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.blobs import bbox_of, bbox_overlaps, grow_blob
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e99db35d533d"
VERSION = "1.1.0"
TASK_ID = "e99db35d533d"
SUMMARY = "Blue components touching the top border are recolored to yellow."

INVARIANTS = [
    "background is 0",
    "source objects are color 1",
    "at least one blue component touches row 0",
    "at least one blue component does not touch row 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_top_touching", "all_top_touching", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "2", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "top_and_interior",
                       "valid": "top_and_interior"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 7, 11)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    c = rng.randint(1, w - 3)
    top_blob = {(0, c), (1, c), (1, c + 1)}
    for r, cc in top_blob:
        g[r][cc] = 1
    used = set(top_blob)
    bboxes = [bbox_of(top_blob)]
    for _ in range(80):
        blob = grow_blob(rng, h - 2, w, set(), rng.randint(3, 5))
        if not blob:
            continue
        shifted = {(r + 2, cc) for r, cc in blob}
        bb = bbox_of(shifted)
        if any(bbox_overlaps(bb, old) for old in bboxes) or used & shifted:
            continue
        for r, cc in shifted:
            g[r][cc] = 1
        break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_top_touching":
        # all blue components in interior, none on row 0 → rule no-op, no contrast
        for r, c in [(3, 2), (3, 3), (4, 2)]:
            g[r][c] = 1
        for r, c in [(5, 5), (5, 6), (6, 6)]:
            g[r][c] = 1
        return g
    if name == "all_top_touching":
        # all blue components touch row 0 → rule recolors all to yellow, no contrast
        for r, c in [(0, 1), (1, 1), (0, 2)]:
            g[r][c] = 1
        for r, c in [(0, 5), (1, 5), (0, 6), (1, 6)]:
            g[r][c] = 1
        return g
    if name == "no_blobs":
        # empty grid → no objects to recolor, rule no-op
        return g
    return g
