"""Generator for arc_puzzle_bank_ninth21:E63.

Same-color diagonal endpoints two steps apart have blank midpoints.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, single_endpoint, midpoint_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f7e325967ea1"
VERSION = "1.1.0"
TASK_ID = "f7e325967ea1"

SUMMARY = "Same-color diagonal endpoints two steps apart have blank midpoints."

INVARIANTS = [
    "background is 0",
    "each active pattern has two same-color diagonal endpoints",
    "the midpoint cell starts as 0",
    "patterns are separated to avoid accidental extra fills",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_endpoint", "midpoint_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "4..16"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "diagonal_step2_pairs",
                       "valid": "diagonal_step2_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..8"},
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
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(300):
        if placed >= target:
            break
        r = rng.randint(0, h - 3)
        c = rng.randint(0, w - 3)
        dc = rng.choice([2, -2])
        c0 = c if dc == 2 else c + 2
        cells = {(r, c0), (r + 1, c0 + dc // 2), (r + 2, c0 + dc)}
        guard = {
            (rr, cc)
            for cr, cc0 in cells
            for rr in range(max(0, cr - 1), min(h, cr + 2))
            for cc in range(max(0, cc0 - 1), min(w, cc0 + 2))
        }
        if guard & reserved:
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        g[r][c0] = color
        g[r + 2][c0 + dc] = color
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # blank → no diagonal endpoint pairs to fill midpoint of
        return g
    if name == "single_endpoint":
        # 1 endpoint per color → can't form pair, no midpoint to fill
        g[2][2] = 4
        g[5][5] = 6
        return g
    if name == "midpoint_filled":
        # midpoint already filled → rule is identity, no change
        g[1][1] = 4; g[2][2] = 4; g[3][3] = 4
        return g
    return g
