"""Generator for arc_puzzle_bank_twelfth21:E83.

One-cell horizontal or vertical gaps between equal colors are repaired.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_gaps,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_gaps, length_2_gap, midpoint_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d7cf07bea34b"
VERSION = "1.1.0"
TASK_ID = "d7cf07bea34b"

SUMMARY = "One-cell horizontal or vertical gaps between equal colors are repaired."

INVARIANTS = [
    "background is 0",
    "each target is an x 0 x horizontal or vertical pattern",
    "target colors are nonzero",
    "gap patterns are separated from each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_gaps", "length_2_gap", "midpoint_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "4..18"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "4..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_gaps":         {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "x_0_x_patterns",
                       "valid": "x_0_x_patterns"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, cells):
    h, w = len(g), len(g[0])
    for r, c in cells:
        for rr in range(max(0, r - 1), min(h, r + 2)):
            for cc in range(max(0, c - 1), min(w, c + 2)):
                if g[rr][cc] != 0:
                    return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("gaps", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("gaps", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("gaps", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(140):
        if placed >= target:
            break
        vertical = rng.choice([False, True])
        if vertical:
            r, c = rng.randint(0, h - 3), rng.randrange(w)
            cells = [(r, c), (r + 2, c)]
        else:
            r, c = rng.randrange(h), rng.randint(0, w - 3)
            cells = [(r, c), (r, c + 2)]
        if _free(g, cells):
            color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
            for rr, cc in cells:
                g[rr][cc] = color
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_gaps":
        # blank → no x_0_x patterns to repair
        return g
    if name == "length_2_gap":
        # 2-cell gap (x 0 0 x) → not a 1-cell gap, rule won't fire
        g[3][1] = 4; g[3][4] = 4
        return g
    if name == "midpoint_filled":
        # midpoint already filled (x x x) → rule is identity
        for c in range(2, 5): g[3][c] = 4
        return g
    return g
