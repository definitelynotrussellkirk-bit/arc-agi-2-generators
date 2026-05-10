"""Generator for arc_puzzle_bank_thirteenth_21_bundle:easy_88_stamp_hollow_3x3_around_markers.

Rule: each marker stamps an empty-centered 3x3 ring in its color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, multi_cell_blobs, markers_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b1e8f6552b5f"
VERSION = "1.1.0"
TASK_ID = "b1e8f6552b5f"

SUMMARY = "Each marker stamps an empty-centered 3x3 ring in its color."

INVARIANTS = [
    "background is 0",
    "markers are nonzero singleton centers",
    "markers are away from the border",
    "marker neighborhoods do not overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "multi_cell_blobs", "markers_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..18"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_interior_singletons",
                       "valid": "spaced_interior_singletons"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _far(p, points):
    r, c = p
    return all(max(abs(r - rr), abs(c - cc)) >= 3 for rr, cc in points)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("n_markers", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        target = ctx.draw_int("n_markers", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        target = ctx.draw_int("n_markers", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    candidates = [(r, c) for r in range(1, h - 1) for c in range(1, w - 1)]
    rng.shuffle(candidates)
    centers = []
    for r, c in candidates:
        if len(centers) >= target:
            break
        if _far((r, c), centers):
            centers.append((r, c))
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # blank → no rings to stamp
        return g
    if name == "multi_cell_blobs":
        # markers form blobs (not singletons) → "isolated singleton" precondition fails
        g[2][2] = 4; g[2][3] = 4
        g[5][5] = 6; g[6][5] = 6
        return g
    if name == "markers_at_corner":
        # markers at corners → 3x3 ring extends out of bounds
        g[0][0] = 3
        g[h - 1][w - 1] = 7
        return g
    return g
