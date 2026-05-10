"""Generator for 14b:m92 — crop component selected by bottom-row key.

Rule: bottom row holds a single non-zero key cell. Find the blob of
that color in the body (rows above bottom), crop it.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, no_match_blob, multiple_keys.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "30aababfb197"
VERSION = "1.1.0"
TASK_ID = "30aababfb197"
SUMMARY = "Bottom-row key cell + 2-3 distinct-color blobs above (one matches key)."

INVARIANTS = [
    "background is 0",
    "bottom row has exactly one non-zero cell (the key)",
    "exactly one blob in the body has the key color",
    "≥1 distractor blob in another color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "no_match_blob", "multiple_keys")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "key_plus_blobs",
                       "valid": "key_plus_blobs"},
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
    g[h - 1][rng.randint(0, w - 1)] = key
    used = {(h - 1, c) for c in range(w)}
    for color in palette:
        cells = grow_blob(rng, h, w, used, rng.randint(3, 5), max_attempts=80)
        if cells:
            for r, c in cells: g[r][c] = color
            used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_key":
        # blobs only, no bottom-row key → no selection signal
        for r, c in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 4
        for r, c in [(4, 5), (4, 6), (5, 5)]: g[r][c] = 6
        return g
    if name == "no_match_blob":
        # key color not present in body → nothing to crop
        g[h - 1][3] = 4
        for r, c in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 6
        for r, c in [(4, 5), (4, 6), (5, 5)]: g[r][c] = 7
        return g
    if name == "multiple_keys":
        # multiple bottom-row keys → ambiguous selection
        g[h - 1][2] = 4
        g[h - 1][6] = 6
        for r, c in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 4
        for r, c in [(4, 5), (4, 6), (5, 5)]: g[r][c] = 6
        return g
    return g
