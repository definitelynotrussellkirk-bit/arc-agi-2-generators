"""Generator for arc_puzzle_bank_third_21_bundle:easy_16_fill_x_centers.

Rule: green diagonal X arms mark black centers that become yellow.

Combinatorial axes (8): grid_h, grid_w, palette_kind, centers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_xs, partial_xs, x_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7cda20c438b7"
VERSION = "1.1.0"
TASK_ID = "7cda20c438b7"
SUMMARY = "Green diagonal X arms mark black centers that become yellow."

INVARIANTS = [
    "background is 0",
    "each marked center has green cells on all four diagonal neighbors",
    "marked centers remain black in the input",
    "centers are spaced apart to avoid accidental X overlaps",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_xs", "partial_xs", "x_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "centers":        {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "spaced_x_marks",
                       "valid": "spaced_x_marks"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _far_from_existing(center, existing):
    r, c = center
    return all(max(abs(r - rr), abs(c - cc)) >= 3 for rr, cc in existing)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("centers", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("centers", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("centers", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    centers = []

    candidates = [(r, c) for r in range(1, h - 1) for c in range(1, w - 1)]
    rng.shuffle(candidates)
    for r, c in candidates:
        if len(centers) >= target:
            break
        if not _far_from_existing((r, c), centers):
            continue
        centers.append((r, c))
        for dr, dc in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            g[r + dr][c + dc] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_xs":
        # blank grid → no green diagonal arms, no centers to mark
        return g
    if name == "partial_xs":
        # only 3 of 4 diagonal arms set → predicate fails, no center filled
        # missing top-right
        for (r, c) in [(2, 2), (4, 2), (4, 4)]: g[r][c] = 3
        # missing bottom-left
        for (r, c) in [(5, 5), (5, 7), (7, 7)]: g[r][c] = 3
        return g
    if name == "x_at_corner":
        # X-arm pattern at grid corner → outer diagonal cells out of bounds, predicate fails
        # would-be center at (0,0) — out of bounds
        g[1][1] = 3   # only one in-bounds diagonal arm
        return g
    return g
