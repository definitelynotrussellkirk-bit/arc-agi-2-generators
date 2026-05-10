"""Generator for arc_additional_puzzles_21_set2:M11 — Crop first marker-color blob (size > 1).

Rule: marker = first non-zero in row 0. Find first blob with that color
and size > 1 (in reading order); crop to bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, marker_color,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_matching_blob, all_singletons.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "5dbe4bcb101c"
VERSION = "1.1.0"
TASK_ID = "5dbe4bcb101c"
SUMMARY = "Marker color in row 0 + multiple blobs of various colors; one is marker-color and size ≥2."

INVARIANTS = [
    "row 0 has 1 non-zero cell (the marker)",
    "exactly one marker-color blob with size ≥ 2",
    "1-2 decoy blobs of other colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_matching_blob", "all_singletons")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marker_color":   {"type": "color", "default": "rng", "valid": "2..7"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "row0_marker_with_color_blobs",
                       "valid": "row0_marker_with_color_blobs"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    marker = rng.choice([2, 3, 4, 5, 6, 7])
    g[0][0] = marker
    # marker-color blob (size 4)
    paint_at(g, 2, 8, [(0, 0), (0, 1), (0, 2), (1, 1)], marker)
    # decoy of other color
    other = rng.choice([c for c in [2, 3, 4, 5, 6, 7, 8, 9] if c != marker])
    paint_at(g, 4, 1, [(0, 0), (0, 1), (1, 0), (1, 1)], other)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # row 0 is empty → no marker color, rule has no target
        paint_at(g, 2, 8, [(0, 0), (0, 1), (1, 1)], 4)
        paint_at(g, 4, 1, [(0, 0), (0, 1), (1, 0), (1, 1)], 6)
        return g
    if name == "no_matching_blob":
        # marker color has no blob of that color → lookup fails
        g[0][0] = 4   # marker is 4
        paint_at(g, 2, 8, [(0, 0), (0, 1), (1, 1)], 6)   # only 6-blob, no 4-blob
        return g
    if name == "all_singletons":
        # marker-color cells are all singletons (size 1) → no blob with size > 1
        g[0][0] = 4
        g[2][3] = 4   # singleton
        g[5][7] = 4   # singleton
        paint_at(g, 4, 1, [(0, 0), (0, 1), (1, 1)], 6)
        return g
    return g
