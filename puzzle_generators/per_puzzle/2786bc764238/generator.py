"""Generator for arc_additional_puzzles_21_set4:M24 — Crop largest non-bg blob.

Rule: pick largest blob (binary mask of non-zero); crop to its bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_largest, single_blob, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "2786bc764238"
VERSION = "1.1.0"
TASK_ID = "2786bc764238"
SUMMARY = "2-3 non-touching distinct-color blobs of distinct sizes."

INVARIANTS = [
    "between 2 and 3 non-touching blobs",
    "all distinct sizes (largest unambiguous)",
    "blobs use distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_largest", "single_blob", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "distinct_size_blobs",
                       "valid": "distinct_size_blobs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..4"},
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
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    sizes = list(range(2, 7)); rng.shuffle(sizes); sizes = sorted(sizes[:3], reverse=True)
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
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "tied_largest":
        # 2 blobs same size → "the largest" ambiguous
        for (r, c) in [(1, 1), (1, 2), (2, 1), (2, 2)]: g[r][c] = 4
        for (r, c) in [(1, 7), (1, 8), (2, 7), (2, 8)]: g[r][c] = 6   # tied
        return g
    if name == "single_blob":
        # only 1 blob → trivially largest
        for (r, c) in [(3, 4), (3, 5), (4, 4), (4, 5)]: g[r][c] = 4
        return g
    if name == "no_blobs":
        # blank → no blobs to crop
        return g
    return g
