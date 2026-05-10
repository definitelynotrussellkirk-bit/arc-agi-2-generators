"""Generator for 15b:m100 — select keyed object, upscale 2x.

Rule: at(some position, often outside main content) = key. Find blob
of that color, upscale by 2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, no_matching_blob, multiple_keys.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "82b2be9b4f4e"
VERSION = "1.1.0"
TASK_ID = "82b2be9b4f4e"
SUMMARY = "Single key cell at corner + 2-3 distinct-color blobs (one matching key)."

INVARIANTS = [
    "background is 0",
    "exactly one isolated single key cell (separate from blobs)",
    "exactly one blob matches the key color",
    "≥1 distractor blob in another color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "no_matching_blob", "multiple_keys")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "2..3"},
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
    g[h - 1][0] = key
    used = {(h - 1, 0)}
    for color in palette:
        cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
        if cells:
            for r, c in cells: g[r][c] = color
            used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_key":
        # blobs but no isolated key cell → no selector for which blob to scale
        g[1][1] = 4; g[1][2] = 4; g[2][1] = 4
        g[5][6] = 6; g[5][7] = 6
        return g
    if name == "no_matching_blob":
        # key color 7 but no blob is color 7 → matching blob not found
        g[h - 1][0] = 7
        g[1][1] = 4; g[1][2] = 4; g[2][1] = 4
        g[5][6] = 6; g[5][7] = 6
        return g
    if name == "multiple_keys":
        # two singleton keys in different colors → ambiguous selector
        g[h - 1][0] = 4
        g[0][w - 1] = 6
        g[3][3] = 4; g[3][4] = 4
        g[5][6] = 6; g[5][7] = 6
        return g
    return g
