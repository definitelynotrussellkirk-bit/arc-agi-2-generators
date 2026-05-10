"""Generator for additional_bank:E7.

Rule: among multiple orange components, output keeps the unique largest.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_largest, single_blob, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.blobs import bbox_of, bbox_overlaps, grow_blob
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4c33979d9cc2"
VERSION = "1.1.0"
TASK_ID = "4c33979d9cc2"
SUMMARY = "Multiple orange components with one unique largest component."

INVARIANTS = [
    "background is 0",
    "orange source components are color 7",
    "one orange component has strictly largest size",
    "components are isolated from one another",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_largest", "single_blob", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 11)
        w = ctx.draw_int("grid_w", 7, 11)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    bboxes = []
    for size in (5, 3, 2):
        for _ in range(100):
            blob = grow_blob(rng, h, w, used, size)
            if not blob:
                continue
            bb = bbox_of(blob)
            if any(bbox_overlaps(bb, old) for old in bboxes):
                continue
            used |= blob
            bboxes.append(bb)
            for r, c in blob:
                g[r][c] = 7
            break
    return g


def _draw_from_degenerate(name, rng):
    import random
    rng = random.Random(0)
    h, w = 9, 9
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    if name == "tied_largest":
        # multiple components share max size → "unique largest" invariant violated, ambiguous
        for size in (4, 4, 2):
            blob = grow_blob(rng, h, w, used, size)
            if blob is None: continue
            used |= blob
            for r, c in blob:
                g[r][c] = 7
        return g
    if name == "single_blob":
        # one component → trivially the largest, rule is identity
        blob = grow_blob(rng, h, w, used, 4)
        if blob:
            for r, c in blob:
                g[r][c] = 7
        return g
    if name == "no_blobs":
        # empty grid → no components, rule output is empty
        return g
    return g
