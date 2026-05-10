"""Generator for arc_puzzle_bank_sixth_21_bundle:easy_41_stamp_x_at_markers.

Rule: blue markers become orange 3x3 X stencils on a blank grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, marker_at_corner, markers_too_close.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d02691ffb818"
VERSION = "1.1.0"
TASK_ID = "d02691ffb818"
SUMMARY = "Blue markers become orange 3x3 X stencils on a blank grid."

INVARIANTS = [
    "background is 0",
    "marker color is 1",
    "output color is 7",
    "markers are separated so X stencils are visually distinct",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "marker_at_corner", "markers_too_close")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "3..22"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "3..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "markers":        {"type": "int", "default": "rng 3..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "interior_separated",
                       "valid": "interior_separated"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("markers", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 10, 11)
        target = ctx.draw_int("markers", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 11)
        target = ctx.draw_int("markers", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    markers: list[tuple[int, int]] = []
    candidates = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(candidates)
    for r, c in candidates:
        if len(markers) >= target:
            break
        if any(abs(r - rr) <= 2 and abs(c - cc) <= 2 for rr, cc in markers):
            continue
        g[r][c] = 1
        markers.append((r, c))
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # empty grid → no X stencils to stamp
        return g
    if name == "marker_at_corner":
        # marker at (0,0) → 5 of 8 X-cells clip off-grid
        g[0][0] = 1
        return g
    if name == "markers_too_close":
        # markers within 2 cells → X stencils overlap, color collision
        g[3][3] = 1
        g[3][5] = 1
        return g
    return g
