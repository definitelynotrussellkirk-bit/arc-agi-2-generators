"""Generator for arc_puzzle_bank_fourteenth21:M97 — extract guide-colored blob.

Rule: at(0,0) = key. Find the (single non-corner) blob of color `key`,
crop to its bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_corner_key, no_key_blob, multiple_key_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "c8d52f645999"
VERSION = "1.1.0"
TASK_ID = "c8d52f645999"
SUMMARY = "Key at (0,0) + a key-color blob away from corner + 1 distractor."

INVARIANTS = [
    "background is 0",
    "(0,0) holds the key color",
    "≥1 key-color blob away from (0,0)",
    "≥1 distractor blob in another color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_corner_key", "no_key_blob", "multiple_key_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "key_at_origin_with_blob",
                       "valid": "key_at_origin_with_blob"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
    key, distractor = palette
    g[0][0] = key
    used = {(0, 0)}
    blob = grow_blob(rng, h, w, used, rng.randint(3, 5), max_attempts=80)
    if blob:
        for r, c in blob: g[r][c] = key
        used |= blob
    dist = grow_blob(rng, h, w, used, rng.randint(2, 3), max_attempts=40)
    if dist:
        for r, c in dist: g[r][c] = distractor
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_corner_key":
        # (0,0) is bg → no key, rule has no anchor
        for (r, c) in [(2, 3), (2, 4), (3, 3)]: g[r][c] = 4
        for (r, c) in [(5, 5), (5, 6), (6, 6)]: g[r][c] = 6
        return g
    if name == "no_key_blob":
        # key at (0,0) but no other key-color blob → rule has nothing to crop
        g[0][0] = 4
        for (r, c) in [(2, 3), (2, 4), (3, 3)]: g[r][c] = 6
        return g
    if name == "multiple_key_blobs":
        # two blobs of key color → ambiguous which to crop
        g[0][0] = 4
        for (r, c) in [(2, 3), (2, 4), (3, 3)]: g[r][c] = 4
        for (r, c) in [(5, 5), (5, 6), (6, 5)]: g[r][c] = 4
        return g
    return g
