"""Generator for 15b:m102 — frame each blob with key color.

Rule: a single corner key cell defines a key color. Each non-key blob
gets its bbox painted with the key color (filled).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, no_blobs, blob_uses_key_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "d5df53fde4de"
VERSION = "1.1.0"
TASK_ID = "d5df53fde4de"
SUMMARY = "Single key cell at corner + 2 distinct-color non-rectangular blobs."

INVARIANTS = [
    "background is 0",
    "exactly one isolated key cell at a corner",
    "2 distinct-color blobs (none equal to key color)",
    "blobs don't 4-touch the key cell",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "no_blobs", "blob_uses_key_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "2", "valid": "2..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "key_at_corner_with_blobs",
                       "valid": "key_at_corner_with_blobs"},
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
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    key = palette[0]
    g[0][w - 1] = key
    used = {(0, w - 1), (0, w - 2), (1, w - 1)}
    for color in palette[1:]:
        cells = grow_blob(rng, h, w, used, rng.randint(3, 4), max_attempts=80)
        if cells is None:
            continue
        for r, c in cells: g[r][c] = color
        used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_key":
        # blobs but no key cell → no color to frame with
        g[2][2] = 4; g[2][3] = 4; g[3][2] = 4
        g[5][6] = 6; g[5][7] = 6
        return g
    if name == "no_blobs":
        # key only, no blobs → nothing to frame
        g[0][w - 1] = 4
        return g
    if name == "blob_uses_key_color":
        # one of the blobs uses the same color as the key → no contrast
        g[0][w - 1] = 4
        g[2][2] = 4; g[2][3] = 4; g[3][2] = 4   # SAME as key color
        g[5][6] = 6
        return g
    return g
