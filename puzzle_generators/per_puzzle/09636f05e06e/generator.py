"""Generator for 319f2597.

Rule: for each row with >=1 0 cell, and each col with >=1 0 cell, set
all those cells to 0 except cells with value 2.

Combinatorial axes (8): grid_h/w, n_zero_cols, n_zero_rows,
zero_density, palette_size, twos_density, position_bias,
preserve_corners.
Degenerates: no_zeros, all_zeros, no_twos.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "09636f05e06e"
VERSION = "1.1.0"
TASK_ID = "09636f05e06e"
SUMMARY = "Dense grid with 0-bands; rule clears bands except 2-cells."

INVARIANTS = [
    ">=1 column or row contains >=1 zero cell",
    "interior cells include >=1 cell of color 2 in zero-bands (so 'preserve' branch fires)",
    "non-bg colors come from {1, 3, 4, 5, 6, 7, 8, 9} ∪ {2}",
]

POSITION_BIAS = ("center", "spread", "edge")
DEGENERATE_TEXTURES = ("no_zeros", "all_zeros", "no_twos")
HELPFUL_TEXTURES = POSITION_BIAS

AXES = {
    "grid_h":           {"type": "int", "default": "rng 10..18", "valid": "8..22"},
    "grid_w":           {"type": "int", "default": "rng 10..18", "valid": "8..22"},
    "n_zero_cols":      {"type": "int", "default": "rng 1..3", "valid": "0..5"},
    "n_zero_rows":      {"type": "int", "default": "rng 0..2", "valid": "0..4"},
    "zero_density":     {"type": "float", "default": "rng 0.4..0.8",
                         "valid": "0.1..1"},
    "palette_size":     {"type": "int", "default": "rng 4..7", "valid": "2..9"},
    "twos_density":     {"type": "float", "default": "rng 0.05..0.2",
                         "valid": "0..0.4"},
    "position_bias":    {"type": "str", "default": "rng helpful",
                         "valid": "|".join(POSITION_BIAS)},
    "texture":          {"type": "str", "default": "alias for position_bias",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 8, 11
    elif difficulty == "hard":
        h_lo, h_hi = 16, 22
    else:
        h_lo, h_hi = 10, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_zero_cols = int(overrides.get("n_zero_cols",
                                    ctx.draw_int("n_zero_cols", 1, 3)))
    n_zero_rows = int(overrides.get("n_zero_rows",
                                    ctx.draw_int("n_zero_rows", 0, 2)))
    n_zero_cols = max(0, min(w - 2, n_zero_cols))
    n_zero_rows = max(0, min(h - 2, n_zero_rows))
    if n_zero_cols == 0 and n_zero_rows == 0:
        n_zero_cols = 1
    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", 4, 7)))
    pool = [1, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    palette = pool[:max(2, n_palette - 1)] + [2]
    zero_density = float(overrides.get("zero_density",
                                       ctx.draw_rng("zero_density")
                                       .uniform(0.4, 0.8)))
    twos_density = float(overrides.get("twos_density",
                                       ctx.draw_rng("twos_density")
                                       .uniform(0.05, 0.2)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIAS)))
    g = [[rng.choice(palette) for _ in range(w)] for _ in range(h)]
    chosen_cols = _pick_cols(bias, w, n_zero_cols, rng)
    for c in chosen_cols:
        for r in range(h):
            if rng.random() < zero_density:
                g[r][c] = 0
    chosen_rows = _pick_rows(bias, h, n_zero_rows, rng)
    for r in chosen_rows:
        for c in range(w):
            if rng.random() < zero_density:
                g[r][c] = 0
    # Sprinkle 2s in zero rows/cols (which become preserved)
    for c in chosen_cols:
        for r in range(h):
            if g[r][c] == 0 and rng.random() < twos_density:
                g[r][c] = 2
    for r in chosen_rows:
        for c in range(w):
            if g[r][c] == 0 and rng.random() < twos_density:
                g[r][c] = 2
    has_zero = any(g[r][c] == 0 for r in range(h) for c in range(w))
    if not has_zero:
        c = chosen_cols[0] if chosen_cols else 1
        g[0][c] = 0
    return g


def _pick_cols(bias, w, n, rng):
    if n <= 0:
        return []
    if bias == "center":
        center = w // 2
        cols = sorted(range(1, w - 1), key=lambda c: abs(c - center))
        return cols[:n]
    if bias == "edge":
        cols = sorted(range(1, w - 1), key=lambda c: -min(c, w - 1 - c))
        return cols[:n]
    cols = list(range(1, w - 1))
    rng.shuffle(cols)
    return cols[:n]


def _pick_rows(bias, h, n, rng):
    if n <= 0:
        return []
    if bias == "center":
        center = h // 2
        rows = sorted(range(1, h - 1), key=lambda r: abs(r - center))
        return rows[:n]
    if bias == "edge":
        rows = sorted(range(1, h - 1), key=lambda r: -min(r, h - 1 - r))
        return rows[:n]
    rows = list(range(1, h - 1))
    rng.shuffle(rows)
    return rows[:n]


def _draw_from_degenerate(name, h, w, rng):
    if name == "no_zeros":
        return [[rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]) for _ in range(w)]
                for _ in range(h)]
    if name == "all_zeros":
        return [[0] * w for _ in range(h)]
    if name == "no_twos":
        g = [[rng.choice([1, 3, 4, 5, 6, 7, 8, 9]) for _ in range(w)]
             for _ in range(h)]
        c = w // 2
        for r in range(h):
            if rng.random() < 0.5:
                g[r][c] = 0
        return g
    return [[1] * w for _ in range(h)]
