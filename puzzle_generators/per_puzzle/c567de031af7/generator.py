"""Generator for puzzle e57337a4.

Rule: input is 15 × 15 divided into 3 × 3 of 5 × 5 sub-grids. bg = g[0][0].
Output is 3 × 3: each cell is 0 if its sub-grid has any 0; else bg color.

Combinatorial axes: bg_color, n_sub_with_zero, zero_positions_per_sub
(scattered/cluster/border), n_zeros_per_sub.
Degenerates: all_subs_have_zero (output all 0), no_subs_have_zero
(output all bg), single_zero_per_sub.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c567de031af7"
VERSION = "1.1.0"
TASK_ID = "c567de031af7"
SUMMARY = "15 × 15 divided into 9 sub-grids; rule outputs 3 × 3 with 0 where sub-grid has any 0."

INVARIANTS = [
    "input is exactly 15 × 15",
    "bg = g[0][0] is non-zero",
    "≥1 sub-grid contains a 0",
    "≥1 sub-grid has no 0 (output has both 0 and bg)",
]

ZERO_POSITIONS = ("scattered", "cluster", "border", "diagonal", "single")
DEGENERATE_TEXTURES = ("all_subs_have_zero", "no_subs_have_zero", "single_zero_per_sub")
HELPFUL_TEXTURES = ZERO_POSITIONS

AXES = {
    "bg_color":            {"type": "color", "default": "rng (≠0)", "valid": "1..9"},
    "n_sub_with_zero":     {"type": "int", "default": "rng 2..7", "valid": "1..8"},
    "zero_positions_kind": {"type": "str", "default": "rng helpful",
                            "valid": "|".join(ZERO_POSITIONS)},
    "n_zeros_per_sub":     {"type": "int", "default": "rng 1..4", "valid": "1..10"},
    "texture":             {"type": "str", "default": "alias for zero_positions_kind",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        n_lo, n_hi = 1, 3
    elif difficulty == "hard":
        n_lo, n_hi = 5, 7
    else:
        n_lo, n_hi = 2, 7
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    bg = int(overrides.get("bg_color", ctx.draw_color("bg_color", exclude={0})))
    n_zero_subs = int(overrides.get("n_sub_with_zero",
                                    ctx.draw_int("n_sub_with_zero", n_lo, n_hi)))
    n_zero_subs = max(1, min(8, n_zero_subs))
    kind = (overrides.get("texture") or overrides.get("zero_positions_kind")
            or ctx.draw_choice("zero_positions_kind", list(ZERO_POSITIONS)))
    n_per_sub = int(overrides.get("n_zeros_per_sub",
                                  ctx.draw_int("n_zeros_per_sub", 1, 4)))
    g = full_grid(15, 15, bg)
    sub_indices = list(range(9))
    rng.shuffle(sub_indices)
    chosen = sub_indices[:n_zero_subs]
    for sub_i in chosen:
        sr, sc = divmod(sub_i, 3)
        positions = _zero_positions_for_kind(kind, n_per_sub, rng)
        for (dr, dc) in positions:
            g[sr * 5 + dr][sc * 5 + dc] = 0
    return g


def _zero_positions_for_kind(kind, n, rng):
    if kind == "cluster":
        cr, cc = rng.randint(0, 4), rng.randint(0, 4)
        cells = [(r, c) for r in range(5) for c in range(5)]
        cells.sort(key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return cells[:n]
    if kind == "border":
        cells = [(0, c) for c in range(5)] + [(4, c) for c in range(5)]
        cells += [(r, 0) for r in range(1, 4)] + [(r, 4) for r in range(1, 4)]
        rng.shuffle(cells)
        return cells[:n]
    if kind == "diagonal":
        return [(k, k) for k in range(min(n, 5))]
    if kind == "single":
        return [(rng.randint(0, 4), rng.randint(0, 4))]
    cells = [(r, c) for r in range(5) for c in range(5)]
    rng.shuffle(cells)
    return cells[:n]


def _draw_from_degenerate(name, rng):
    bg = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    g = full_grid(15, 15, bg)
    if name == "all_subs_have_zero":
        for sr in range(3):
            for sc in range(3):
                g[sr * 5][sc * 5] = 0
        return g
    if name == "no_subs_have_zero":
        return g
    if name == "single_zero_per_sub":
        for sr in range(3):
            for sc in range(3):
                if rng.random() < 0.5:
                    g[sr * 5 + rng.randint(0, 4)][sc * 5 + rng.randint(0, 4)] = 0
        return g
    return g
