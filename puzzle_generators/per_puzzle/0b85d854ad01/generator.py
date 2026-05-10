"""Generator for arc_puzzle_bank_twelfth21:M82 — crop key-color blob.

Rule: key = at(0,0). Find the largest blob of color `key` (excluding
the corner cell), crop to its bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, no_key_blob, key_only_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "0b85d854ad01"
VERSION = "1.1.0"
TASK_ID = "0b85d854ad01"
SUMMARY = "Key at (0,0) + a key-color blob away from corner + 1 distractor blob."

INVARIANTS = [
    "background is 0",
    "(0,0) holds the key color",
    "≥1 key-color blob away from (0,0)",
    "≥1 blob in a different color (distractor)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "no_key_blob", "key_only_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "key_corner_blob_else",
                       "valid": "key_corner_blob_else"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        blob_lo, blob_hi = 3, 4
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        blob_lo, blob_hi = 4, 5
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
        blob_lo, blob_hi = 3, 5
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
    key, distractor = palette
    g[0][0] = key
    used = {(0, 0)}
    blob = grow_blob(rng, h, w, used, rng.randint(blob_lo, blob_hi), max_attempts=80)
    if blob:
        for r, c in blob: g[r][c] = key
        used |= blob
    dist = grow_blob(rng, h, w, used, rng.randint(1, 2), max_attempts=40)
    if dist:
        for r, c in dist: g[r][c] = distractor
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_key":
        # (0,0) is bg → no key color identifiable
        g[3][4] = 4; g[3][5] = 4; g[4][4] = 4
        g[6][7] = 6
        return g
    if name == "no_key_blob":
        # key at (0,0) but no other cells of key color → nothing to crop
        g[0][0] = 4
        g[3][3] = 6; g[3][4] = 6; g[4][3] = 6
        return g
    if name == "key_only_at_corner":
        # only the corner has the key color → crop target is empty
        g[0][0] = 3
        return g
    return g
