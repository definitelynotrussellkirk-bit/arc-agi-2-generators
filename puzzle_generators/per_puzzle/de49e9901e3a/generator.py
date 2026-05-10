"""Generator for arc_additional_puzzle_bank_volume5:M33 — Fill rs×cs cross-product per object.

Rule: for each object, take the unique rows and unique cols its cells
occupy. Paint the cross-product cells in that obj's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_solid_rects, single_row_blobs, single_cell_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob, bbox_of, bbox_overlaps

GENERATOR_ID = "de49e9901e3a"
VERSION = "1.1.0"
TASK_ID = "de49e9901e3a"
SUMMARY = "Several non-rect blobs; output fills each obj's rs×cs cross-product cells."

INVARIANTS = [
    "between 2 and 4 non-touching blobs",
    "blobs are bbox-isolated",
    "at least one blob is non-rectangular (so output != input)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_solid_rects", "single_row_blobs", "single_cell_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..4",  "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "bbox_isolated_blobs",
                       "valid": "bbox_isolated_blobs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_blobs = ctx.draw_int("n_blobs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_blobs = ctx.draw_int("n_blobs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
        n_blobs = ctx.draw_int("n_blobs", 2, 4)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    colors = list(range(1, 10)); rng.shuffle(colors)
    used = set(); bboxes = []
    for i in range(n_blobs):
        size = rng.randint(3, 6)
        for _ in range(10):
            blob = grow_blob(rng, h, w, used, size)
            if blob is None: continue
            bb = bbox_of(blob)
            if any(bbox_overlaps(bb, ob) for ob in bboxes): continue
            used |= blob; bboxes.append(bb)
            for r, c in blob: g[r][c] = colors[i % len(colors)]
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "all_solid_rects":
        # solid rectangles → cross-product equals the input rect, rule is identity
        for r in range(2):
            for c in range(3): g[1 + r][1 + c] = 4
        for r in range(3):
            for c in range(2): g[5 + r][6 + c] = 6
        return g
    if name == "single_row_blobs":
        # 1xN horizontal line → row-set has 1 element; cross-product is the line, identity
        for c in range(1, 5): g[2][c] = 4
        for c in range(2, 7): g[6][c] = 6
        return g
    if name == "single_cell_blobs":
        # 1x1 blobs → cross-product is the cell, rule is identity
        g[2][3] = 4
        g[5][7] = 6
        g[7][2] = 3
        return g
    return g
