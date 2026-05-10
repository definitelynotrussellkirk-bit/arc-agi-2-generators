"""Generator for arc_puzzle_bank_thirteenth21:E89.

Combinatorial axes (8): grid_h, grid_w, palette_kind, pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, axis_aligned, midpoint_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "04f965847543"
VERSION = "1.1.0"
TASK_ID = "04f965847543"

SUMMARY = "Equal diagonal endpoints two cells apart fill their diagonal midpoint."

INVARIANTS = [
    "background is 0",
    "each target pair is diagonal with one zero midpoint",
    "pairs may use either diagonal orientation",
    "pairs are separated to avoid accidental diagonal midpoint matches",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "axis_aligned", "midpoint_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "4..18"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "4..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "pairs":          {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "diagonal_2step_pairs",
                       "valid": "diagonal_2step_pairs"},
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
        target = ctx.draw_int("pairs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("pairs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("pairs", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(9, target))
    placed = 0
    for _ in range(140):
        if placed >= target:
            break
        dr = rng.choice([-2, 2])
        dc = rng.choice([-2, 2])
        r = rng.randint(max(0, -dr), min(h - 1, h - 1 - dr))
        c = rng.randint(max(0, -dc), min(w - 1, w - 1 - dc))
        cells = [(r, c), (r + dr, c + dc)]
        if _free(g, cells):
            color = colors[placed % len(colors)]
            for rr, cc in cells:
                g[rr][cc] = color
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # single cells per color → no diagonal pair, no midpoint to fill
        g[2][2] = 4; g[5][6] = 6
        return g
    if name == "axis_aligned":
        # pairs are 2 apart in row or column (not diagonal) → midpoint isn't on diagonal
        g[3][1] = 4; g[3][3] = 4
        g[1][6] = 6; g[3][6] = 6
        return g
    if name == "midpoint_filled":
        # midpoint is already non-zero → rule is identity at that pair
        g[2][2] = 4; g[3][3] = 7; g[4][4] = 4
        return g
    return g
