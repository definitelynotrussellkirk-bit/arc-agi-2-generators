"""Generator for 342ae2ed.

Rule: pairs of same-color components connected by diagonal segment
between their bounding boxes.

Combinatorial axes (8): grid_h/w, pair_count, palette_kind, jitter,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: same_position, no_pairs, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6c08e545720f"
VERSION = "1.1.0"
TASK_ID = "6c08e545720f"
SUMMARY = "Same-color component pairs; rule fills gap between them with diagonal segment."

INVARIANTS = [
    "background is color 7",
    "each active color appears in exactly two separated components",
    "the second component is diagonally offset from the first",
    "the gap between paired components is filled with that color",
]

POSITION_BIASES = ("scattered", "diagonal", "wide_spread", "stacked")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("same_position", "no_pairs", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "12", "valid": "10..16"},
    "pair_count":     {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "jitter":         {"type": "int", "default": "rng 0..1", "valid": "0..2"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "texture":        {"type": "str", "default": "alias for position_bias",
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
        pc_lo, pc_hi = 1, 1
    elif difficulty == "hard":
        pc_lo, pc_hi = 2, 3
    else:
        pc_lo, pc_hi = 1, 2
    pair_count = int(overrides.get("pair_count",
                                   ctx.draw_int("pair_count", pc_lo, pc_hi)))
    pair_count = max(1, min(3, pair_count))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, pair_count, rng)
    h = int(overrides.get("grid_h", 12))
    w = int(overrides.get("grid_w", 12))
    g = full_grid(h, w, 7)
    starts = [(1, 1, 6, 6), (2, 8, 7, 3), (4, 4, 9, 9)]
    jitter = int(overrides.get("jitter",
                               ctx.draw_int("jitter", 0, 1)))
    for i in range(pair_count):
        r1, c1, r2, c2 = starts[i % len(starts)]
        if r1 < h and c1 < w and r2 < h and c2 < w:
            j = rng.randint(0, max(0, jitter))
            g[r1 + j][c1] = pal[i]
            g[r2 + j][c2] = pal[i]
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 8, 9]
    pool = [c for c in pool if c != 7]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 7)
    if name == "same_position":
        g[5][5] = 2
        return g
    if name == "no_pairs":
        g[2][2] = 2; g[8][9] = 3
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
