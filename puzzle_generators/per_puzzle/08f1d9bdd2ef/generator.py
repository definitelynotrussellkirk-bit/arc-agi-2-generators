"""Generator for 272f95fa.

Rule: 2 horizontal 8-rows + 2 vertical 8-cols define 9 zones; rule
recolors zones by region.

Combinatorial axes (8): grid_h/w, sep_row1, sep_row2, sep_col1, sep_col2,
n_distractors, palette_kind, anchor_corner.
Degenerates: no_separators, single_row, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "08f1d9bdd2ef"
VERSION = "1.1.0"
TASK_ID = "08f1d9bdd2ef"
SUMMARY = "9-zone grid with 2 horizontal 8-rows and 2 vertical 8-cols."

INVARIANTS = [
    "exactly 2 full-width 8-rows",
    "exactly 2 full-height 8-cols",
    "rest of grid is all 0",
]

POSITION_BIASES = ("centered", "wide_spread", "tight", "rng")
DEGENERATE_TEXTURES = ("no_separators", "single_row", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "sep_row1":       {"type": "int", "default": "rng 2..h/2-1", "valid": "1..h-2"},
    "sep_row2":       {"type": "int", "default": "rng h/2+1..h-3", "valid": "1..h-2"},
    "sep_col1":       {"type": "int", "default": "rng 2..w/2-1", "valid": "1..w-2"},
    "sep_col2":       {"type": "int", "default": "rng w/2+1..w-3", "valid": "1..w-2"},
    "n_distractors":  {"type": "int", "default": "rng 1..2", "valid": "0..3"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "texture":        {"type": "str", "default": "alias for position bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 6, 8, 10, 12
        nd_lo, nd_hi = 0, 1
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 11, 14, 14, 18
        nd_lo, nd_hi = 2, 3
    else:
        h_lo, h_hi, w_lo, w_hi = 8, 10, 12, 14
        nd_lo, nd_hi = 1, 2
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    sr1 = int(overrides.get("sep_row1",
                            rng.randint(2, max(2, h // 2 - 1))))
    sr2 = int(overrides.get("sep_row2",
                            rng.randint(min(h - 3, h // 2 + 1), h - 3)))
    sc1 = int(overrides.get("sep_col1",
                            rng.randint(2, max(2, w // 2 - 1))))
    sc2 = int(overrides.get("sep_col2",
                            rng.randint(min(w - 3, w // 2 + 1), w - 3)))
    sr1 = max(2, min(sr1, h - 3))
    sr2 = max(sr1 + 2, min(sr2, h - 2))
    sc1 = max(2, min(sc1, w - 3))
    sc2 = max(sc1 + 2, min(sc2, w - 2))
    for c in range(w):
        g[sr1][c] = 8; g[sr2][c] = 8
    for r in range(h):
        g[r][sc1] = 8; g[r][sc2] = 8
    nd = int(overrides.get("n_distractors",
                           ctx.draw_int("n_distractors", nd_lo, nd_hi)))
    nd = max(0, min(3, nd))
    for _ in range(nd):
        for _try in range(20):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] == 0:
                g[r][c] = rng.choice([3, 5, 6, 7])
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 13
    g = full_grid(h, w, 0)
    if name == "no_separators":
        return g
    if name == "single_row":
        for c in range(w):
            g[4][c] = 8
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 8
        return g
    return g
