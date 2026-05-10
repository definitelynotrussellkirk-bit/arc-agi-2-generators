"""Generator for 3b:m19 — keep corner-touching blobs.

Rule: keep blobs whose bbox touches a grid corner (any of 4); drop
non-corner-touching blobs.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_corner_blob, no_interior_blob, all_corner_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "515cca15a0b7"
VERSION = "1.1.0"
TASK_ID = "515cca15a0b7"
SUMMARY = "≥1 corner-anchored blob + ≥1 interior blob."

INVARIANTS = [
    "background is 0",
    "≥1 blob with a cell at a grid corner",
    "≥1 fully-interior blob (no border cells)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_corner_blob", "no_interior_blob", "all_corner_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "corner_blob_plus_interior",
                       "valid": "corner_blob_plus_interior"},
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
    g[0][0] = palette[0]; g[0][1] = palette[0]; g[1][0] = palette[0]
    used = {(0, 0), (0, 1), (1, 0)}
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
    if name == "no_corner_blob":
        # only interior blobs, no corner-anchored → rule erases everything
        g[3][3] = 4; g[3][4] = 4
        g[5][6] = 6; g[6][6] = 6
        return g
    if name == "no_interior_blob":
        # only corner blob, no interior → rule keeps everything (no contrast)
        g[0][0] = 4; g[0][1] = 4; g[1][0] = 4
        return g
    if name == "all_corner_blobs":
        # all 4 corners have blobs → rule keeps all (no signal for elimination)
        g[0][0] = 4; g[0][1] = 4
        g[0][w - 1] = 6; g[0][w - 2] = 6
        g[h - 1][0] = 7; g[h - 2][0] = 7
        g[h - 1][w - 1] = 8; g[h - 1][w - 2] = 8
        return g
    return g
