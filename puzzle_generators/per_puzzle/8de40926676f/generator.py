"""Generator for arc_additional_puzzles_21_set11_bundle:M74 — Pairwise size-equality matrix.

Rule: sort objects by (r1, c1). Output n×n grid: cell (r, c) is 8 if
size(obj_r) == size(obj_c), else 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, single_blob, all_distinct_sizes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "8de40926676f"
VERSION = "1.1.0"
TASK_ID = "8de40926676f"
SUMMARY = "Several non-touching blobs with mix of repeated and unique sizes; output is n×n size-equality matrix."

INVARIANTS = [
    "between 3 and 4 non-touching blobs",
    "at least one pair of equal-size blobs (so off-diagonal 8s appear)",
    "blobs use distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "single_blob", "all_distinct_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "non_touching_blobs",
                       "valid": "non_touching_blobs"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..4"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    # Pick 3-4 sizes; ensure at least one duplicate
    n = rng.randint(3, 4)
    if n == 3:
        sizes = [2, 3, 2] if rng.random() < 0.5 else [2, 3, 3]
    else:
        sizes = [2, 3, 2, 4]
    rng.shuffle(sizes)
    colors = list(range(1, 10)); rng.shuffle(colors)
    used = set()
    for i, sz in enumerate(sizes):
        for _ in range(20):
            blob = grow_blob(rng, h, w, used, sz)
            if blob is None or len(blob) != sz: continue
            used |= blob
            for r, c in blob: g[r][c] = colors[i]
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # blank → 0×0 matrix, no comparisons to make
        return g
    if name == "single_blob":
        # 1 blob → 1×1 matrix is trivially [[8]]
        for r, c in [(2, 2), (3, 2)]: g[r][c] = 4
        return g
    if name == "all_distinct_sizes":
        # all sizes unique → matrix is identity, no off-diagonal 8s
        for r, c in [(1, 1)]: g[r][c] = 4  # size 1
        for r, c in [(4, 1), (4, 2)]: g[r][c] = 6  # size 2
        for r, c in [(7, 1), (7, 2), (7, 3)]: g[r][c] = 7  # size 3
        for r, c in [(1, 6), (1, 7), (2, 6), (2, 7)]: g[r][c] = 8  # size 4
        return g
    return g
