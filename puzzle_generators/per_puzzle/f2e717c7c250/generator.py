"""Generator for 6b:m42 — crop union of key-color blobs.

Rule: row 0 has key cells; find all blobs in those colors below; crop
their union bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_keys,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_keys, no_matching_blobs, all_distractors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "f2e717c7c250"
VERSION = "1.1.0"
TASK_ID = "f2e717c7c250"
SUMMARY = "Row-0 has 2 keys + 1 blob per key + 1 distractor in another color."

INVARIANTS = [
    "background is 0",
    "row 0 has 2 distinct key colors at distinct cols",
    "below: 1 blob per key color + 1 distractor blob",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_keys", "no_matching_blobs", "all_distractors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_keys":         {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "row0_keys_with_blobs",
                       "valid": "row0_keys_with_blobs"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..5"},
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
    keys = palette[:2]
    distractor = palette[2]
    cols = rng.sample(range(w), 2)
    for c, color in zip(cols, keys):
        g[0][c] = color
    used = {(0, c) for c in cols}
    for c in range(w):
        used.add((1, c))
    for color in keys + [distractor]:
        cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
        if cells:
            for r, c in cells: g[r][c] = color
            used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_keys":
        # row 0 blank → no keys, rule has no source colors
        for (r, c) in [(3, 2), (3, 3), (4, 2)]: g[r][c] = 4
        for (r, c) in [(5, 7), (5, 8), (6, 7)]: g[r][c] = 6
        return g
    if name == "no_matching_blobs":
        # keys in row 0 but no blobs of those colors below → union bbox is empty
        g[0][2] = 4; g[0][7] = 6   # keys
        for (r, c) in [(3, 4), (3, 5), (4, 4)]: g[r][c] = 8   # only distractors
        for (r, c) in [(6, 1), (6, 2)]: g[r][c] = 3
        return g
    if name == "all_distractors":
        # keys present but ALL below blobs use non-key colors → empty bbox
        g[0][3] = 4; g[0][8] = 6   # keys 4, 6
        for (r, c) in [(3, 2), (3, 3), (4, 2)]: g[r][c] = 8
        for (r, c) in [(6, 6), (6, 7), (7, 7)]: g[r][c] = 3
        return g
    return g
