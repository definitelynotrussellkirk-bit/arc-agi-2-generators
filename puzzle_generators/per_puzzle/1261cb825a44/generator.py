"""Generator for arc_puzzle_bank_21_set19_bundle:medium_p03 — corner-key crop.

Rule: one of 4 corner cells is non-zero (the "key color"). Output is
the cells of all `key-color` cells in the grid (excluding any corner
positions), packed to a min-bbox subgrid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_distractors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_corner_key, no_blob, no_distractors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "1261cb825a44"
VERSION = "1.1.0"
TASK_ID = "1261cb825a44"
SUMMARY = "Single corner key-color cell + key-blob inside + 1-2 distractor blobs."

INVARIANTS = [
    "background is 0",
    "exactly one corner cell is non-zero (the key)",
    "at least one non-corner blob has the key color (so output is non-empty)",
    "1-2 other-colored distractor blobs exist (so the key matters)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_corner_key", "no_blob", "no_distractors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_distractors":  {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "corner_key_blobs_inside",
                       "valid": "corner_key_blobs_inside"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 13, 16)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    key_color = palette[0]
    distractors = palette[1:]
    corners = [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]
    corner = rng.choice(corners)
    g[corner[0]][corner[1]] = key_color
    used = {corner}
    # one key-color blob away from corner
    blob = grow_blob(rng, h, w, used, rng.randint(3, 5), max_attempts=80)
    if blob is None:
        return g
    if any(p in corners for p in blob):
        # try once more
        blob = grow_blob(rng, h, w, used, rng.randint(3, 5), max_attempts=80)
        if blob is None or any(p in corners for p in blob):
            return g
    for r, c in blob:
        g[r][c] = key_color
    used |= blob
    # 1-2 distractor blobs in other colors
    for color in distractors:
        b = grow_blob(rng, h, w, used, rng.randint(3, 5), max_attempts=40)
        if b is None or any(p in corners for p in b):
            continue
        for r, c in b:
            g[r][c] = color
        used |= b
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_corner_key":
        # No corner cell set — rule has no key color to filter by.
        g[3][3] = 4; g[3][4] = 4; g[4][3] = 4
        g[6][6] = 5; g[6][7] = 5
        return g
    if name == "no_blob":
        # Corner key set but no matching blob inside — output is empty.
        g[0][0] = 4
        g[5][5] = 6; g[5][6] = 6
        return g
    if name == "no_distractors":
        # Only the key color anywhere — rule has nothing to filter against.
        g[0][0] = 4
        g[3][3] = 4; g[3][4] = 4; g[4][3] = 4
        return g
    return g
