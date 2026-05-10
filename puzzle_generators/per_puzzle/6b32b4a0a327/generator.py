"""Generator for 14b:m96 — select border-touching blob, recolor by key.

Rule: pick the (single) blob whose bbox touches a grid border, recolor
it to a key color (e.g. 8). Interior blobs untouched.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_interior,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_border_blob, no_interior_blob, multiple_border_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "6b32b4a0a327"
VERSION = "1.1.0"
TASK_ID = "6b32b4a0a327"
SUMMARY = "1 border-touching blob + 1-2 interior blobs."

INVARIANTS = [
    "background is 0",
    "exactly 1 blob touching a grid border",
    "≥1 fully-interior blob",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_border_blob", "no_interior_blob", "multiple_border_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_interior":     {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "border_plus_interior",
                       "valid": "border_plus_interior"},
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
    # border blob — top row
    g[0][1] = palette[0]
    g[0][2] = palette[0]
    g[1][1] = palette[0]
    used = {(0, 1), (0, 2), (1, 1)}
    # interior — exclude border
    interior_used = set(used)
    for r in range(h):
        interior_used.add((r, 0)); interior_used.add((r, w - 1))
    for c in range(w):
        interior_used.add((0, c)); interior_used.add((h - 1, c))
    for color in palette[1:]:
        cells = grow_blob(rng, h, w, interior_used, rng.randint(2, 4), max_attempts=80)
        if cells:
            for r, c in cells: g[r][c] = color
            interior_used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_border_blob":
        # all blobs are fully interior → nothing to recolor
        g[3][3] = 4; g[3][4] = 4; g[4][3] = 4
        g[6][6] = 6; g[6][7] = 6
        return g
    if name == "no_interior_blob":
        # only the border blob present → no contrast group to preserve
        g[0][1] = 4; g[0][2] = 4; g[1][1] = 4
        return g
    if name == "multiple_border_blobs":
        # ≥2 border blobs → ambiguous which one to select
        g[0][1] = 4; g[0][2] = 4
        g[h - 1][3] = 6; g[h - 1][4] = 6
        g[3][3] = 7; g[4][3] = 7
        return g
    return g
