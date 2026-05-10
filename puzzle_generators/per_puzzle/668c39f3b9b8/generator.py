"""Generator for 3b:m16 — shift all blobs by direction key.

Rule: a single direction-key cell at a grid corner determines the
shift direction. All non-key blobs shift by 1 cell in that direction.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, no_blobs, blob_blocking_shift.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "668c39f3b9b8"
VERSION = "1.1.0"
TASK_ID = "668c39f3b9b8"
SUMMARY = "Single corner direction-key + 2-3 blobs in interior."

INVARIANTS = [
    "background is 0",
    "exactly one corner key cell (e.g. (h-1, 0))",
    "2-3 distinct-color blobs in interior, none touching the corner",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "no_blobs", "blob_blocking_shift")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "2", "valid": "2..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "corner_key_plus_interior_blobs",
                       "valid": "corner_key_plus_interior_blobs"},
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
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    g[h - 1][0] = palette[0]
    used = {(h - 1, 0), (h - 1, 1), (h - 2, 0)}
    for c in range(w):
        used.add((0, c))
    for color in palette[1:]:
        cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
        if cells:
            for r, c in cells: g[r][c] = color
            used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_key":
        # blobs without corner direction-key → no shift direction
        g[3][3] = 4; g[3][4] = 4; g[4][3] = 4
        g[5][6] = 6; g[5][7] = 6
        return g
    if name == "no_blobs":
        # corner key alone with no blobs → nothing to shift
        g[h - 1][0] = 5
        return g
    if name == "blob_blocking_shift":
        # blob touches the row/col where shift would push another blob → collision
        g[h - 1][0] = 5  # shift up
        g[3][3] = 4; g[3][4] = 4
        g[2][3] = 6  # blocks the upward shift of the 4-blob
        return g
    return g
