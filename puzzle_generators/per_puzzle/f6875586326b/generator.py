"""Generator for 178fcbfb.

Rule: row with 1 or 3 → fill row with that color; col with 2 → fill
col with 2; row precedence.

Combinatorial axes (8): grid_h/w, n_rows, n_cols, palette_size,
position_bias, color_distribution, anchor_corner, asymmetry_force.
Degenerates: no_rows, no_cols, all_rows.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f6875586326b"
VERSION = "1.1.0"
TASK_ID = "f6875586326b"
SUMMARY = "Cells of 1/3 in rows + 2 in cols; rule fills rows then cols."

INVARIANTS = [
    "background is 0",
    ">=1 cell of color 1 OR 3",
    ">=1 cell of color 2",
    "no row contains both 2 and (1 or 3) (so row vs col precedence is unambiguous)",
]

POSITION_BIAS = ("center", "spread", "edge")
COLOR_DISTRIBUTIONS = ("balanced", "ones_only", "threes_only", "mixed")
DEGENERATE_TEXTURES = ("no_rows", "no_cols", "all_rows")
HELPFUL_TEXTURES = POSITION_BIAS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 5..10", "valid": "4..14"},
    "grid_w":            {"type": "int", "default": "rng 7..14", "valid": "6..18"},
    "n_rows":            {"type": "int", "default": "rng 1..3", "valid": "0..5"},
    "n_cols":            {"type": "int", "default": "rng 1..3", "valid": "0..5"},
    "palette_size":      {"type": "int", "default": "rng 2..3", "valid": "1..3"},
    "color_distribution": {"type": "str", "default": "rng helpful",
                           "valid": "|".join(COLOR_DISTRIBUTIONS)},
    "position_bias":     {"type": "str", "default": "rng helpful",
                          "valid": "|".join(POSITION_BIAS)},
    "anchor_corner":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for position_bias",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 4, 6, 6, 9
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 9, 14, 13, 18
    else:
        h_lo, h_hi, w_lo, w_hi = 5, 10, 7, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_rows = int(overrides.get("n_rows",
                               ctx.draw_int("n_rows", 1, 3)))
    n_cols = int(overrides.get("n_cols",
                               ctx.draw_int("n_cols", 1, 3)))
    n_rows = max(0, min(min(h - 1, 5), n_rows))
    n_cols = max(0, min(min(w - 1, 5), n_cols))
    if n_rows + n_cols == 0:
        n_rows, n_cols = 1, 1
    color_dist = overrides.get("color_distribution",
                               ctx.draw_choice("color_distribution",
                                               list(COLOR_DISTRIBUTIONS)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIAS)))
    g = full_grid(h, w, 0)
    rows_used = _pick_rows(bias, h, n_rows, rng)
    for r in rows_used:
        c = _pick_col(bias, w, rng)
        g[r][c] = _pick_color_13(color_dist, rng)
    avail_rows = [rr for rr in range(h) if rr not in rows_used]
    cols_used = _pick_cols(bias, w, n_cols, rng)
    for c in cols_used:
        if not avail_rows:
            r = rng.randint(0, h - 1)
        else:
            r = rng.choice(avail_rows)
        g[r][c] = 2
    return g


def _pick_rows(bias, h, n, rng):
    if n <= 0:
        return []
    if bias == "center":
        center = h // 2
        rs = sorted(range(h), key=lambda r: abs(r - center))
        return rs[:n]
    if bias == "edge":
        rs = sorted(range(h), key=lambda r: -min(r, h - 1 - r))
        return rs[:n]
    return rng.sample(range(h), n)


def _pick_cols(bias, w, n, rng):
    if n <= 0:
        return []
    if bias == "center":
        center = w // 2
        cs = sorted(range(w), key=lambda c: abs(c - center))
        return cs[:n]
    if bias == "edge":
        cs = sorted(range(w), key=lambda c: -min(c, w - 1 - c))
        return cs[:n]
    return rng.sample(range(w), n)


def _pick_col(bias, w, rng):
    if bias == "center":
        return w // 2
    return rng.randint(0, w - 1)


def _pick_color_13(dist, rng):
    if dist == "ones_only":
        return 1
    if dist == "threes_only":
        return 3
    return rng.choice([1, 3])


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_rows":
        for c in range(0, w, 2):
            g[h // 2][c] = 2
        return g
    if name == "no_cols":
        for r in range(h):
            g[r][w // 2] = rng.choice([1, 3])
        return g
    if name == "all_rows":
        for r in range(h):
            g[r][0] = rng.choice([1, 3])
        return g
    return g
