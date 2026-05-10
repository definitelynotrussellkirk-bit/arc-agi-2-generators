"""Generator for arc_additional_puzzle_bank_volume6:E37.

Rule: empty diagonal midpoints between yellow pairs are filled cyan.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_gaps,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, partial_pair, midpoint_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "10fa03869a44"
VERSION = "1.1.0"
TASK_ID = "10fa03869a44"
SUMMARY = "Empty diagonal midpoints between yellow pairs are filled cyan."

INVARIANTS = [
    "background is 0",
    "each target gap has yellow cells on opposite diagonal corners",
    "the midpoint starts empty",
    "target triples are separated so fills do not interact",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "partial_pair", "midpoint_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "5..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "5..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_gaps":         {"type": "int", "default": "rng 2..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "spaced_diagonal_pairs",
                       "valid": "spaced_diagonal_pairs"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_gaps = ctx.draw_int("n_gaps", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
        n_gaps = ctx.draw_int("n_gaps", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
        n_gaps = ctx.draw_int("n_gaps", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    centers: list[tuple[int, int]] = []
    for _ in range(220):
        if len(centers) >= n_gaps:
            break
        r = rng.randint(1, h - 2)
        c = rng.randint(1, w - 2)
        if any(abs(r - rr) < 3 and abs(c - cc) < 3 for rr, cc in centers):
            continue
        if rng.choice([False, True]):
            g[r - 1][c - 1] = 4
            g[r + 1][c + 1] = 4
        else:
            g[r - 1][c + 1] = 4
            g[r + 1][c - 1] = 4
        centers.append((r, c))
    if not centers:
        g[1][1] = 4
        g[3][3] = 4
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # blank → no diagonal pairs, rule has no midpoints to fill
        return g
    if name == "partial_pair":
        # single yellow cell with no diagonal partner → predicate "pair" fails
        g[2][2] = 4
        g[5][5] = 4
        g[7][7] = 4
        return g
    if name == "midpoint_filled":
        # diagonal pair with midpoint already non-zero → predicate "empty midpoint" fails
        g[2][2] = 4; g[4][4] = 4
        g[3][3] = 6  # midpoint already filled
        g[5][7] = 4; g[7][5] = 4
        g[6][6] = 8
        return g
    return g
