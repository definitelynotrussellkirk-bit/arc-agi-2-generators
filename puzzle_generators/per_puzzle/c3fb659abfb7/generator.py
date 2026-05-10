"""Generator for arc_puzzle_bank_21_set22_bundle:medium_p06 — 2 color-9 markers + draw line.

Rule: 2 single-cell color-9 markers; the rule draws a line between them.

Combinatorial axes (8): grid_h, grid_w, palette_kind, marker_distance,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: single_marker, no_markers, markers_collinear.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c3fb659abfb7"
VERSION = "1.1.0"
TASK_ID = "c3fb659abfb7"
SUMMARY = "Exactly 2 color-9 markers placed on a grid."

INVARIANTS = [
    "background is 0",
    "exactly 2 color-9 marker cells at distinct positions",
    "markers are non-collinear (not same row/col) so a non-trivial line is drawn",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_marker", "no_markers", "markers_collinear")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marker_distance": {"type": "int", "default": "rng 2..h+w",
                        "valid": "2..28"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "non_collinear",
                       "valid": "non_collinear"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for _ in range(40):
        r1 = rng.randint(0, h - 1); c1 = rng.randint(0, w - 1)
        r2 = rng.randint(0, h - 1); c2 = rng.randint(0, w - 1)
        if (r1, c1) == (r2, c2): continue
        if abs(r1 - r2) < 2 or abs(c1 - c2) < 2: continue
        g[r1][c1] = 9
        g[r2][c2] = 9
        return g
    raise ValueError("could not place markers")


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "single_marker":
        # one endpoint only → no line to draw
        g[3][4] = 9
        return g
    if name == "no_markers":
        # empty grid → rule has no anchors
        return g
    if name == "markers_collinear":
        # markers share a row → line is trivially horizontal, no slope
        g[4][2] = 9
        g[4][7] = 9
        return g
    return g
