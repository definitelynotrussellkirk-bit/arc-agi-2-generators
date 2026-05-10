"""Generator for 20_bundle:m140 — select object touching 2 borders, crop.

Rule: pick the (single) blob whose bbox touches exactly 2 grid
borders, crop its bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_interior,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_corner_blob, no_interior_blob, multiple_corner_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "076ce2aa4e8c"
VERSION = "1.1.0"
TASK_ID = "076ce2aa4e8c"
SUMMARY = "Corner blob touching 2 borders + 1-2 interior blobs touching 0 borders."

INVARIANTS = [
    "background is 0",
    "exactly one blob with bbox touching 2 grid borders (corner-anchored)",
    "≥1 interior blob touching 0 borders",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_corner_blob", "no_interior_blob", "multiple_corner_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_interior":     {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "corner_plus_interior",
                       "valid": "corner_plus_interior"},
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
    # corner blob: top-left
    g[0][0] = palette[0]
    g[1][0] = palette[0]
    g[0][1] = palette[0]
    used = {(0, 0), (1, 0), (0, 1)}
    # interior blobs
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
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_corner_blob":
        # all blobs are interior → no 2-border-touching blob to crop
        g[3][3] = 4; g[3][4] = 4
        g[6][7] = 6; g[5][7] = 6
        return g
    if name == "no_interior_blob":
        # only the corner blob → no contrast objects
        g[0][0] = 4; g[1][0] = 4; g[0][1] = 4
        return g
    if name == "multiple_corner_blobs":
        # ≥2 corner-touching blobs → ambiguous which to crop
        g[0][0] = 4; g[1][0] = 4; g[0][1] = 4
        g[h - 1][w - 1] = 6; g[h - 2][w - 1] = 6; g[h - 1][w - 2] = 6
        g[3][3] = 7; g[4][3] = 7
        return g
    return g
