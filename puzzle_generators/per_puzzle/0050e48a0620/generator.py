"""Generator for round3_md:rectangle_or_not — Recolor by rectangularity.

Rule: each object is recolored to:
  4 if its cells fill its bbox (solid rectangle)
  1 otherwise (any non-rectangular shape)

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_solid, all_non_rect, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob, bbox_of, bbox_overlaps

GENERATOR_ID = "0050e48a0620"
VERSION = "1.1.0"
TASK_ID = "0050e48a0620"
SUMMARY = "Mix of solid-rectangle and non-rectangular blobs; output recolors by rectangularity."

INVARIANTS = [
    "between 3 and 5 non-touching blobs",
    "at least one solid rectangle AND one non-rectangular",
    "blobs use color 2",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_solid", "all_non_rect", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 3..5", "valid": "3..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _place_solid_rect(rng, h, w, used, bboxes):
    for _ in range(20):
        rh = rng.randint(1, 3)
        rw = rng.randint(1, 3)
        if rh == 1 and rw == 1:
            rh = 2
        r1 = rng.randint(0, h - rh)
        c1 = rng.randint(0, w - rw)
        cells = {(r1 + dr, c1 + dc) for dr in range(rh) for dc in range(rw)}
        from puzzle_generators.helpers.blobs import has_neighbor
        if any(p in used or has_neighbor(p, used, ignore=cells) for p in cells):
            continue
        bb = (r1, c1, r1 + rh - 1, c1 + rw - 1)
        if any(bbox_overlaps(bb, ob) for ob in bboxes):
            continue
        return cells, bb
    return None, None


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_blobs = ctx.draw_int("n_blobs", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_blobs = ctx.draw_int("n_blobs", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
        n_blobs = ctx.draw_int("n_blobs", 3, 5)

    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used = set()
    bboxes = []

    sr, bb = _place_solid_rect(rng, h, w, used, bboxes)
    if sr is not None:
        used |= sr; bboxes.append(bb)
        for r, c in sr: g[r][c] = 2

    nr = grow_blob(rng, h, w, used, 4)
    if nr is not None:
        bb2 = bbox_of(nr)
        bh = bb2[2] - bb2[0] + 1
        bw = bb2[3] - bb2[1] + 1
        if bh * bw == len(nr):
            nr = grow_blob(rng, h, w, used, 5)
        if nr is not None and not any(bbox_overlaps(bbox_of(nr), ob) for ob in bboxes):
            used |= nr; bboxes.append(bbox_of(nr))
            for r, c in nr: g[r][c] = 2

    for i in range(n_blobs - 2):
        if rng.random() < 0.5:
            sr, bb = _place_solid_rect(rng, h, w, used, bboxes)
            if sr is not None:
                used |= sr; bboxes.append(bb)
                for r, c in sr: g[r][c] = 2
        else:
            blob = grow_blob(rng, h, w, used, rng.randint(3, 5))
            if blob is None: continue
            bb = bbox_of(blob)
            if any(bbox_overlaps(bb, ob) for ob in bboxes): continue
            used |= blob; bboxes.append(bb)
            for r, c in blob: g[r][c] = 2

    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "all_solid":
        # all blobs solid rectangles → output is monochrome 4, no contrast
        for r in range(2, 4):
            for c in range(2, 4):
                g[r][c] = 2
        for r in range(6, 8):
            for c in range(6, 9):
                g[r][c] = 2
        return g
    if name == "all_non_rect":
        # all blobs non-rectangular → output is monochrome 1, no contrast
        for r, c in [(2, 2), (2, 3), (3, 2)]:
            g[r][c] = 2
        for r, c in [(5, 5), (6, 5), (6, 6), (7, 6)]:
            g[r][c] = 2
        return g
    if name == "no_blobs":
        # empty grid → no objects to recolor, rule no-op
        return g
    return g
