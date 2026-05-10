"""Generator for arc_puzzle_bank_fourth_21_bundle:easy_25_complete_descending_diagonal_gaps.

Rule: each pair of color-4 cells on a descending diagonal (offset 2) has
their midpoint filled with 4.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_gaps,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, midpoints_already_filled, ascending_diagonal.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7195f447bb20"
VERSION = "1.1.0"
TASK_ID = "7195f447bb20"
SUMMARY = "Pairs of color-4 cells with one missing descending diagonal midpoint."

INVARIANTS = [
    "background is 0",
    "each target motif has 4,0,4 on a descending diagonal",
    "motifs are separated so they do not form longer diagonal runs",
    "at least one diagonal gap is present",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "midpoints_already_filled", "ascending_diagonal")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_gaps":         {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "descending_diag_pairs",
                       "valid": "descending_diag_pairs"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        n_gaps = ctx.draw_int("n_gaps", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
        n_gaps = ctx.draw_int("n_gaps", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 11)
        w = ctx.draw_int("grid_w", 7, 11)
        n_gaps = ctx.draw_int("n_gaps", 2, 4)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    for _ in range(140):
        if len(used) // 2 >= n_gaps:
            break
        r = rng.randint(0, h - 3)
        c = rng.randint(0, w - 3)
        band = {(r + k, c + k) for k in range(-1, 4)
                if 0 <= r + k < h and 0 <= c + k < w}
        if used & band:
            continue
        g[r][c] = 4
        g[r + 2][c + 2] = 4
        used.add((r, c)); used.add((r + 2, c + 2))
    if not used:
        g[0][0] = g[2][2] = 4
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # isolated 4s with no descending-diagonal partner → no midpoints to fill
        g[1][1] = 4
        g[5][2] = 4
        g[3][6] = 4
        return g
    if name == "midpoints_already_filled":
        # full diagonal runs (no gap) → rule already satisfied, output identical
        g[1][1] = 4; g[2][2] = 4; g[3][3] = 4
        g[4][5] = 4; g[5][6] = 4; g[6][7] = 4
        return g
    if name == "ascending_diagonal":
        # ascending pairs (NE diagonal) → wrong axis, rule (descending) ignores
        g[3][1] = 4; g[1][3] = 4   # ascending pair
        g[7][3] = 4; g[5][5] = 4   # ascending pair
        return g
    return g
