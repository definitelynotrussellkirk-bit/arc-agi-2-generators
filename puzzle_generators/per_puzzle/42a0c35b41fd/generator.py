"""Generator for arc_puzzle_bank_21_set21_bundle:medium_p07 — corner-key transform crop.

Rule: at(0,0) is a key (1..7) selecting a transform. Pick the largest
non-corner blob, transform it (1=identity, 2=cw, 3=180, 4=ccw, 5=flip_lr,
6=flip_ud, else=transpose) and output its cropped grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, key,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, no_blob, square_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "42a0c35b41fd"
VERSION = "1.1.0"
TASK_ID = "42a0c35b41fd"
SUMMARY = "(0,0) holds a 1..7 key + a clearly-largest non-corner blob in another color."

INVARIANTS = [
    "background is 0",
    "(0,0) ∈ {1, 2, 3, 4, 5, 6, 7}",
    "the largest non-corner blob is strictly larger than any other (so target is unique)",
    "the largest blob is not at (0,0)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "no_blob", "square_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "key":            {"type": "int", "default": "rng 1..7", "valid": "1..7"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "key_corner_blob_body",
                       "valid": "key_corner_blob_body"},
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
    key = rng.randint(1, 7)
    g[0][0] = key
    used = {(0, 0)}
    palette = rng.sample([c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c != key], 2)
    big = grow_blob(rng, h, w, used, rng.randint(4, 5), max_attempts=80)
    if big is None:
        return g
    for r, c in big:
        g[r][c] = palette[0]
    used |= big
    small = grow_blob(rng, h, w, used, rng.randint(2, 2), max_attempts=40)
    if small is not None:
        for r, c in small:
            g[r][c] = palette[1]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_key":
        # blob without corner key → no transform dispatch
        for r, c in [(3, 3), (3, 4), (4, 3), (4, 4)]: g[r][c] = 4
        return g
    if name == "no_blob":
        # corner key alone, no blob → nothing to transform
        g[0][0] = 3
        return g
    if name == "square_blob":
        # blob is solid 2x2 square → all rotations/flips identical
        g[0][0] = 2
        for r in range(3, 5):
            for c in range(4, 6):
                g[r][c] = 4
        return g
    return g
