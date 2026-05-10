"""Generator for puzzle d8c310e9.

Rule: per row, find rightmost non-zero col R, then smallest period p
such that g[r][cc] == g[r][cc mod p] for cc in [0..R]. Fill row using
that period to the end.

Combinatorial axes (8): grid_h/w, n_active_rows, period_min, period_max,
n_repeats, palette_size, position_bias, anchor_corner.
Degenerates: empty_grid, full_grid, single_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "80271cb9b303"
VERSION = "1.1.0"
TASK_ID = "80271cb9b303"
SUMMARY = "Rows with periodic prefix; rule extends each row using its period."

INVARIANTS = [
    "background is 0",
    ">=1 row with non-zero cells",
    "in each non-zero row, prefix is the period repeated >=2 times",
    "row's prefix length < grid_w (so rule has work to do)",
]

POSITION_BIASES = ("spread", "centered", "top_heavy", "bottom_heavy",
                   "alternating")
DEGENERATE_TEXTURES = ("empty_grid", "full_grid", "single_row")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..10", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "n_active_rows":  {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "period_min":     {"type": "int", "default": "2", "valid": "2..6"},
    "period_max":     {"type": "int", "default": "rng 3..5", "valid": "2..7"},
    "n_repeats":      {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..7"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 4, 6
    elif difficulty == "hard":
        h_lo, h_hi = 10, 14
    else:
        h_lo, h_hi = 5, 10
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 7, h_hi + 8)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_rows = int(overrides.get("n_active_rows",
                               ctx.draw_int("n_active_rows", 1, 3)))
    n_rows = max(1, min(min(h, 5), n_rows))
    p_min = int(overrides.get("period_min", 2))
    p_max = int(overrides.get("period_max",
                              ctx.draw_int("period_max", 3, 5)))
    n_rep = int(overrides.get("n_repeats",
                              ctx.draw_int("n_repeats", 2, 3)))
    palette_size = int(overrides.get("palette_size",
                                     ctx.draw_int("palette_size", 2, 4)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    palette_pool = list(range(1, 10))
    rng.shuffle(palette_pool)
    palette = palette_pool[:max(1, min(7, palette_size))]
    g = full_grid(h, w, 0)
    chosen_rows = _pick_rows(bias, h, n_rows, rng)
    for r in chosen_rows:
        period = rng.randint(max(2, p_min), max(p_min, p_max))
        period = min(period, w // 2)
        while True:
            pattern = [rng.choice([0] + palette[:max(1, len(palette) // 2)])
                       for _ in range(period)]
            if any(v != 0 for v in pattern):
                break
        repeats = max(2, min(n_rep, max(2, w // period - 1)))
        for i in range(repeats * period):
            if i < w:
                g[r][i] = pattern[i % period]
    return g


def _pick_rows(bias, h, n, rng):
    if bias == "centered":
        center = h // 2
        rs = [center - (n - 1) // 2 + i for i in range(n)]
        return [r for r in rs if 0 <= r < h][:n]
    if bias == "top_heavy":
        return list(range(min(n, h)))
    if bias == "bottom_heavy":
        return list(range(max(0, h - n), h))
    if bias == "alternating":
        rs = [i for i in range(h) if i % 2 == 0]
        return rs[:n] if len(rs) >= n else (rs + [i for i in range(h) if i % 2 == 1])[:n]
    return rng.sample(range(h), n)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "empty_grid":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    if name == "single_row":
        # Single non-bg cell — period == 1, fills with one color
        r = h // 2
        g[r][0] = color
        return g
    return g
