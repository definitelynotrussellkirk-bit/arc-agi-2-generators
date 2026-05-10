"""Generator for arc_puzzle_bank_seventeenth21:E114.

Same-color endpoints on down-right diagonals have blank spans.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, length_1_pair, anti_diagonal.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7b351b4ba9a5"
VERSION = "1.1.0"
TASK_ID = "7b351b4ba9a5"

SUMMARY = "Same-color endpoints on down-right diagonals have blank spans."

INVARIANTS = [
    "background is 0",
    "each active color appears exactly twice",
    "the two cells share a down-right diagonal",
    "intervening diagonal cells are initially 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "length_1_pair", "anti_diagonal")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..16"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 1..3", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "down_right_diagonal_pairs",
                       "valid": "down_right_diagonal_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
        target = ctx.draw_int("pairs", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("pairs", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 6, 9)
        target = ctx.draw_int("pairs", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(target, 9))
    placed = 0
    for _ in range(300):
        if placed >= target:
            break
        span = rng.randint(2, min(4, h - 1, w - 1))
        r = rng.randint(0, h - span - 1)
        c = rng.randint(0, w - span - 1)
        cells = {(r + d, c + d) for d in range(span + 1)}
        guard = {
            (rr, cc)
            for cr, cc0 in cells
            for rr in range(max(0, cr - 1), min(h, cr + 2))
            for cc in range(max(0, cc0 - 1), min(w, cc0 + 2))
        }
        if guard & reserved:
            continue
        color = colors[placed % len(colors)]
        g[r][c] = color
        g[r + span][c + span] = color
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 7
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # blank → no diagonal endpoint pairs
        return g
    if name == "length_1_pair":
        # adjacent diagonal cells → no empty span
        g[2][2] = 4; g[3][3] = 4
        return g
    if name == "anti_diagonal":
        # anti-diagonal (slope -1) → not down-right, rule won't fire
        g[2][6] = 4; g[5][3] = 4
        return g
    return g
