"""Generator for arc_additional_puzzles_21_set9:M63 — Each object → single dot at bbox center.

Rule: each object replaced by a single cell of its color at the center
of its bbox (integer-quotient mid-point).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_singletons, single_blob, blobs_share_center.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob, bbox_of, bbox_overlaps

GENERATOR_ID = "6e068328f4ce"
VERSION = "1.1.0"
TASK_ID = "6e068328f4ce"
SUMMARY = "Several non-touching multi-cell blobs (size ≥ 2); output is single dot at each bbox center."

INVARIANTS = [
    "between 2 and 4 non-touching blobs",
    "each blob has size > 1 (so collapse to dot is non-trivial)",
    "blob bboxes don't overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_singletons", "single_blob", "blobs_share_center")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "spread_blobs",
                       "valid": "spread_blobs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..9"},
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
        n_blobs = 2
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_blobs = 4
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
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "all_singletons":
        # all blobs are singletons → bbox center is the cell, rule is identity
        g[2][3] = 4; g[5][7] = 6; g[7][2] = 3
        return g
    if name == "single_blob":
        # one blob → output has one center, no comparison
        for (r, c) in [(3, 4), (3, 5), (4, 4), (4, 5), (5, 5)]: g[r][c] = 6
        return g
    if name == "blobs_share_center":
        # two blobs whose bbox centers happen to collide → output drops one
        for (r, c) in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 4   # bbox (1,1)-(2,2), center (1,1)
        for (r, c) in [(5, 5), (5, 6), (6, 5)]: g[r][c] = 6   # bbox (5,5)-(6,6), center (5,5)
        return g
    return g
