"""Generator for arc_puzzle_bank_21_set12_bundle:easy_l06 — Plus → X transform.

Rule: find each plus-shape (5 cells of one color in + pattern). Replace
with X-shape: 4 cells at the corners, center off.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_plus,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_plus_shapes, partial_plus, plus_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "072fa5d50e96"
VERSION = "1.1.0"
TASK_ID = "072fa5d50e96"
SUMMARY = "1-3 plus-shapes (5 cells each) of distinct colors, well separated."

INVARIANTS = [
    "1-3 plus-shapes (each is a 3×3 + pattern of one color)",
    "centers are ≥2 cells apart",
    "centers are at interior positions (not on grid border)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_plus_shapes", "partial_plus", "plus_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_plus":         {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "spaced_plus_shapes",
                       "valid": "spaced_plus_shapes"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..8"},
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
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_plus = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_plus)
    centers = []
    for color in palette:
        for _ in range(40):
            r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
            if any(abs(r - pr) + abs(c - pc) < 4 for pr, pc in centers):
                continue
            for dr, dc in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
                g[r + dr][c + dc] = color
            centers.append((r, c))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_plus_shapes":
        # blank → no plus to transform
        return g
    if name == "partial_plus":
        # missing arms → "5-cell plus" precondition fails
        g[3][3] = 4
        g[3][2] = 4; g[3][4] = 4   # missing top/bottom arms
        g[5][6] = 6
        g[4][6] = 6; g[6][6] = 6   # missing left/right arms
        return g
    if name == "plus_at_corner":
        # plus center at edge → 1 of 4 cardinal arms out of bounds
        g[0][2] = 4
        g[0][1] = 4; g[0][3] = 4
        g[1][2] = 4   # missing the up arm (out of bounds)
        return g
    return g
