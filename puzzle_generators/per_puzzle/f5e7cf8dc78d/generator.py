"""Generator for 0f63c0b9.

Rule: each non-zero "dot" defines a horizontal band; in its band, draw
its color on left/right edges + a horizontal line at the dot's row.

Combinatorial axes (8): grid_h/w, n_dots, palette_kind, position_bias,
min_separation, anchor_corner, asymmetry_force, palette_size.
Degenerates: same_row, no_dots, full_grid.
"""
from __future__ import annotations

from itertools import combinations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f5e7cf8dc78d"
VERSION = "1.1.0"
TASK_ID = "f5e7cf8dc78d"
SUMMARY = "Small grid with 2-3 single colored dots at distinct rows."

INVARIANTS = [
    "2-3 non-zero cells, each at a distinct row",
    "each dot has a unique color",
    "dots are spaced at least two rows apart",
]

POSITION_BIASES = ("scattered", "left_lean", "right_lean", "centered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("same_row", "no_dots", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "6..10"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "6..10"},
    "n_dots":         {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "min_separation": {"type": "int", "default": "2", "valid": "1..4"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..4"},
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
        h_lo, h_hi = 6, 7
        nd_lo, nd_hi = 2, 2
    elif difficulty == "hard":
        h_lo, h_hi = 8, 10
        nd_lo, nd_hi = 3, 4
    else:
        h_lo, h_hi = 6, 8
        nd_lo, nd_hi = 2, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    n_dots = int(overrides.get("n_dots",
                               ctx.draw_int("n_dots", nd_lo, nd_hi)))
    n_dots = max(2, min(4, n_dots))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, n_dots, rng)
    sep = int(overrides.get("min_separation", 2))
    row_options = [
        combo for combo in combinations(range(h), n_dots)
        if all(abs(a - b) >= sep for a, b in combinations(combo, 2))
    ]
    if not row_options:
        row_options = [tuple(rng.sample(range(h), n_dots))]
    rows = list(rng.choice(row_options))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    for r, color in zip(rows, palette):
        if bias == "left_lean":
            c = rng.randint(1, max(1, w // 3))
        elif bias == "right_lean":
            c = rng.randint(min(w - 2, 2 * w // 3), w - 2)
        elif bias == "centered":
            c = max(1, w // 2 + rng.randint(-1, 1))
        else:
            c = rng.randint(1, w - 2)
        c = max(1, min(c, w - 2))
        g[r][c] = color
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 7, 7
    g = full_grid(h, w, 0)
    if name == "same_row":
        g[3][1] = 2
        g[3][5] = 3
        return g
    if name == "no_dots":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
