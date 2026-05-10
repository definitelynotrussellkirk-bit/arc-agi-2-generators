"""Generator for 11b:m71 — marker selects component to crop.

Rule: a marker cell of one color picks the matching-color blob; crop
that blob to its bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_matching_blob, multiple_marker_colors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "0a444f80387e"
VERSION = "1.1.0"
TASK_ID = "0a444f80387e"
SUMMARY = "1 isolated marker cell + 2-3 distinct-color blobs (one matching marker)."

INVARIANTS = [
    "background is 0",
    "exactly one isolated marker cell",
    "exactly one blob has the marker color",
    "≥1 distractor blob in another color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_matching_blob", "multiple_marker_colors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "marker_with_distinct_blobs",
                       "valid": "marker_with_distinct_blobs"},
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
    marker = palette[0]
    g[h - 1][w - 1] = marker
    used = {(h - 1, w - 1), (h - 1, w - 2), (h - 2, w - 1)}
    for color in palette:
        cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
        if cells:
            for r, c in cells: g[r][c] = color
            used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # only blobs, no isolated marker → no selector for which blob to crop
        g[1][1] = 4; g[1][2] = 4; g[2][1] = 4
        g[5][6] = 6; g[5][7] = 6
        return g
    if name == "no_matching_blob":
        # marker color 7 but no blob is color 7 → matching blob not found
        g[h - 1][w - 1] = 7
        g[1][1] = 4; g[1][2] = 4; g[2][1] = 4
        g[5][6] = 6; g[5][7] = 6
        return g
    if name == "multiple_marker_colors":
        # two singleton markers in different colors → ambiguous selector
        g[h - 1][w - 1] = 4
        g[h - 1][0] = 6
        g[1][1] = 4; g[1][2] = 4
        g[5][6] = 6; g[5][7] = 6
        return g
    return g
