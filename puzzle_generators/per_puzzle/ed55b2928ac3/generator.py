"""Generator for arc_puzzle_bank_21_set22_bundle:medium_p07 — corner-key transform crop.

Rule: at(0,0) = key. Crop to content (excluding the corner cell), then
apply transform based on key.

Combinatorial axes (8): grid_h, grid_w, palette_kind, key,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blob, blob_at_corner, blob_is_rectangle.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "ed55b2928ac3"
VERSION = "1.1.0"
TASK_ID = "ed55b2928ac3"
SUMMARY = "Key 1..7 at (0,0) + a clearly-shaped non-symmetric blob away from corner."

INVARIANTS = [
    "background is 0",
    "(0,0) ∈ {1, 2, 3, 4, 5, 6, 7}",
    "exactly one non-corner blob, non-rectangular",
    "blob doesn't touch the (0,0) corner",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blob", "blob_at_corner", "blob_is_rectangle")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "key":            {"type": "int", "default": "rng 1..7", "valid": "1..7"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "key_corner_with_blob",
                       "valid": "key_corner_with_blob"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 7, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    key = rng.randint(1, 7)
    g[0][0] = key
    used = {(0, 0)}
    color = rng.choice([c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c != key])
    for _ in range(40):
        cells = grow_blob(rng, h, w, used, rng.randint(3, 4), max_attempts=20)
        if cells is None:
            continue
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        bb = (max(rs) - min(rs) + 1) * (max(cs) - min(cs) + 1)
        if bb == len(cells):
            continue
        for r, c in cells:
            g[r][c] = color
        break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    g[0][0] = 1   # key=1
    if name == "no_blob":
        # key present but no blob → nothing to crop and transform
        return g
    if name == "blob_at_corner":
        # blob extends into corner cell → key ambiguously part of blob
        for (r, c) in [(0, 0), (0, 1), (1, 0), (1, 1), (2, 1)]: g[r][c] = 4
        return g
    if name == "blob_is_rectangle":
        # blob is a perfect rectangle → transforms produce identical (or aspect-flipped) output
        for r in range(2, 5):
            for c in range(3, 6): g[r][c] = 6
        return g
    return g
