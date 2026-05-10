"""Generator for arc_additional_puzzle_bank_volume3:E16 — Diagonal-2-quad center → 1.

Rule: cell (r,c) with value 0 whose 4 diagonal neighbors are all 2 →
becomes 1. Out-of-bounds neighbors count as not 2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_quads,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_quads, quads_at_edge, partial_quads.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a44e3443619f"
VERSION = "1.1.0"
TASK_ID = "a44e3443619f"
SUMMARY = "2-3 corner-2 quads (2s at corners of 3x3) with 0 in middle."

INVARIANTS = [
    ">=2 'X' patterns: 2 at four diagonal corners of a 3x3, with empty 0 center",
    "patterns don't overlap or touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_quads", "quads_at_edge", "partial_quads")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_quads":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "interior_quads",
                       "valid": "interior_quads"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n = rng.randint(2, 3)
    placed = []
    for _ in range(40):
        if len(placed) >= n:
            break
        r = rng.randint(0, h - 3); c = rng.randint(0, w - 3)
        ok = all(abs(r - pr) > 3 or abs(c - pc) > 3 for pr, pc in placed)
        if ok:
            g[r][c] = 2; g[r][c + 2] = 2
            g[r + 2][c] = 2; g[r + 2][c + 2] = 2
            placed.append((r, c))
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_quads":
        # scattered 2s but no full diagonal-quad pattern → rule has no centers to mark
        for r, c in [(2, 2), (4, 5), (6, 8)]:
            g[r][c] = 2
        return g
    if name == "quads_at_edge":
        # quads positioned so center is on grid edge → out-of-bounds diagonal neighbors break rule
        # quad at (0,0): center (0,0)+(1,1) = (1,1) but corner (0,0) means top-left out of bounds wrap
        g[0][0] = 2; g[0][2] = 2
        g[2][0] = 2; g[2][2] = 2
        return g
    if name == "partial_quads":
        # only 3 of 4 diagonal corners are 2 → rule's "all 4 diagonals" condition never matches
        for top_r, top_c in [(2, 2), (5, 6)]:
            g[top_r][top_c] = 2
            g[top_r][top_c + 2] = 2
            g[top_r + 2][top_c] = 2
            # missing (top_r + 2, top_c + 2)
        return g
    return g
