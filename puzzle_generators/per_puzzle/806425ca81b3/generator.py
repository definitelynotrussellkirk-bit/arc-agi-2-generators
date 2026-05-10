"""Generator for 22168020.

Rule: per row, for each 0 cell, fill with the color that has at least
one non-zero cell to the left AND right.

Combinatorial axes (8): grid_h/w, n_rows, n_marks, palette_kind,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_marks, all_adjacent, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "806425ca81b3"
VERSION = "1.1.0"
TASK_ID = "806425ca81b3"
SUMMARY = "2-3 rows containing 2-3 cells of one color each, with gaps."

INVARIANTS = [
    "1-3 rows have >=2 non-zero cells of a single color",
    "the cells are non-adjacent so the bridge fill is non-trivial",
    "rows use distinct colors",
]

POSITION_BIASES = ("scattered", "wide_spread", "tight", "centered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_marks", "all_adjacent", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "n_rows":         {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "n_marks":        {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..5"},
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
        h_lo, h_hi, w_lo, w_hi = 6, 7, 6, 7
        nr_lo, nr_hi = 1, 2
        nm_lo, nm_hi = 2, 2
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 11, 14, 11, 14
        nr_lo, nr_hi = 3, 5
        nm_lo, nm_hi = 3, 5
    else:
        h_lo, h_hi, w_lo, w_hi = 8, 10, 8, 10
        nr_lo, nr_hi = 2, 3
        nm_lo, nm_hi = 2, 4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    n_rows = int(overrides.get("n_rows",
                               ctx.draw_int("n_rows", nr_lo, nr_hi)))
    n_rows = max(1, min(min(h, 5), n_rows))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, n_rows, rng)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    rows = rng.sample(range(h), n_rows)
    for r, color in zip(rows, pal):
        n_marks = int(overrides.get("n_marks",
                                    rng.randint(nm_lo, nm_hi)))
        n_marks = max(2, min(w, n_marks))
        cols = _pick_cols(bias, w, n_marks, rng)
        for c in cols:
            g[r][c] = color
    return g


def _pick_cols(bias, w, n_marks, rng):
    if bias == "wide_spread":
        cols = [rng.randint(0, max(0, w // 4)),
                rng.randint(min(w - 1, 3 * w // 4), w - 1)]
        for _ in range(n_marks - 2):
            for _try in range(20):
                c = rng.randint(0, w - 1)
                if c not in cols:
                    cols.append(c)
                    break
    elif bias == "tight":
        start = rng.randint(0, max(0, w - n_marks - 2))
        cols = sorted(rng.sample(range(start, min(w, start + n_marks + 2)),
                                 n_marks))
    elif bias == "centered":
        center = w // 2
        rad = max(1, w // 3)
        candidates = list(range(max(0, center - rad), min(w, center + rad)))
        if len(candidates) < n_marks:
            candidates = list(range(w))
        cols = sorted(rng.sample(candidates, min(n_marks, len(candidates))))
    else:
        cols = sorted(rng.sample(range(w), n_marks))
    if cols[-1] - cols[0] < 3 and w >= 4:
        cols = [rng.randint(0, w // 3),
                rng.randint(2 * w // 3, w - 1)]
    return cols


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
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_marks":
        return g
    if name == "all_adjacent":
        g[3][2] = 2; g[3][3] = 2
        g[5][4] = 3; g[5][5] = 3
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
