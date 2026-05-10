"""Generator for 7b:m45 — crop union of key-colored blobs.

Rule: row 0 holds 1-2 key-color cells. Find all blobs of those colors,
crop the union (bbox of all key-color cells in the body).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_keys,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_keys, no_distractor, key_color_missing_in_body.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "d486b924dcdf"
VERSION = "1.1.0"
TASK_ID = "d486b924dcdf"
SUMMARY = "Row-0 has 2 distinct key colors + below-row blobs in those + 1 distractor."

INVARIANTS = [
    "background is 0",
    "row 0 has exactly 2 key-color cells (distinct colors) at distinct cols",
    "below row 0: ≥1 blob in each key color + ≥1 distractor blob",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_keys", "no_distractor", "key_color_missing_in_body")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_keys":         {"type": "int", "default": "2", "valid": "2..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "row0_keys_plus_blobs",
                       "valid": "row0_keys_plus_blobs"},
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
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_keys":
        # blobs without row-0 key cells → no key colors selected
        for r, c in [(2, 1), (2, 2)]: g[r][c] = 4
        for r, c in [(4, 5), (4, 6)]: g[r][c] = 6
        for r, c in [(6, 8), (7, 8)]: g[r][c] = 7
        return g
    if name == "no_distractor":
        # keys + matching blobs but no distractor → no contrast for "union" rule
        g[0][2] = 4; g[0][6] = 6
        for r, c in [(2, 1), (2, 2)]: g[r][c] = 4
        for r, c in [(4, 5), (4, 6)]: g[r][c] = 6
        return g
    if name == "key_color_missing_in_body":
        # row-0 key colors don't appear below → empty union
        g[0][2] = 4; g[0][6] = 6
        for r, c in [(4, 5), (4, 6)]: g[r][c] = 7  # only distractor color
        return g
    return g
