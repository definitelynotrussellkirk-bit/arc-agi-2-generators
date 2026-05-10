"""Generator for arc_puzzle_bank_21_set21_bundle:medium_p01 — keyed color crop.

Rule: key = at(0,0). Find the largest connected blob of `key` color
(excluding the (0,0) cell itself). Output = that blob cropped to its
bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, no_blob_in_key, equal_size_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "5d15679fbc44"
VERSION = "1.1.0"
TASK_ID = "5d15679fbc44"
SUMMARY = "(0,0) holds key color; the same key color forms a blob elsewhere; distractor blobs in other colors."

INVARIANTS = [
    "background is 0",
    "(0,0) is non-zero (the key)",
    "key-color blob away from corner exists, strictly larger than any other key-color region",
    "1-2 distractor blobs in different colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "no_blob_in_key", "equal_size_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "key_corner_with_keycolor_blob",
                       "valid": "key_corner_with_keycolor_blob"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    key = palette[0]
    distractors = palette[1:]
    g[0][0] = key
    used = {(0, 0)}
    blob = grow_blob(rng, h, w, used, rng.randint(4, 5), max_attempts=80)
    if blob is None:
        return g
    for r, c in blob:
        g[r][c] = key
    used |= blob
    for color in distractors:
        b = grow_blob(rng, h, w, used, rng.randint(2, 3), max_attempts=40)
        if b is None:
            continue
        for r, c in b:
            g[r][c] = color
        used |= b
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_key":
        # blob present but no corner key → no color filter defined
        for r, c in [(3, 3), (3, 4), (4, 4)]: g[r][c] = 4
        return g
    if name == "no_blob_in_key":
        # corner key but no other key-color blob → nothing to crop
        g[0][0] = 4
        for r, c in [(3, 3), (4, 3)]: g[r][c] = 6
        return g
    if name == "equal_size_blobs":
        # 2 key-color blobs of equal size → "strictly larger" precondition fails
        g[0][0] = 4
        for r, c in [(2, 2), (3, 2), (3, 3)]: g[r][c] = 4  # blob1, size 3
        for r, c in [(6, 6), (6, 7), (7, 7)]: g[r][c] = 4  # blob2, size 3 (tied)
        return g
    return g
