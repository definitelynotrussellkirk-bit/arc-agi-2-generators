"""Generator for 17b80ad2.

Rule: in each col whose last non-zero mark is 5, fill rows by segments
based on mark order.

Combinatorial axes (8): grid_h/w, n_cols, n_marks_per_col,
palette_size, position_bias, palette_kind, anchor_endpoints,
asymmetry_force.
Degenerates: no_cols, no_5s, all_5s.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "964b23808a3c"
VERSION = "1.1.0"
TASK_ID = "964b23808a3c"
SUMMARY = "Cols with mark sequences ending in 5; rule fills segments by mark order."

INVARIANTS = [
    "background is 0",
    ">=2 columns have >=2 non-zero marks",
    "in each marked column, the bottom-most mark is 5",
    "non-marked columns are all 0",
]

POSITION_BIAS = ("center", "spread", "edge")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("no_cols", "no_5s", "all_5s")
HELPFUL_TEXTURES = POSITION_BIAS

AXES = {
    "grid_h":           {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "grid_w":           {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "n_cols":           {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "n_marks_per_col":  {"type": "int", "default": "rng 3..5", "valid": "2..7"},
    "palette_size":     {"type": "int", "default": "rng 3..5", "valid": "2..7"},
    "palette_kind":     {"type": "str", "default": "rng helpful",
                         "valid": "|".join(PALETTE_KINDS)},
    "position_bias":    {"type": "str", "default": "rng helpful",
                         "valid": "|".join(POSITION_BIAS)},
    "anchor_endpoints": {"type": "bool", "default": "false",
                         "valid": "true|false"},
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
        h_lo, h_hi = 15, 20
    else:
        h_lo, h_hi = 10, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_cols = int(overrides.get("n_cols",
                               ctx.draw_int("n_cols", 2, 4)))
    n_cols = max(1, min(min(6, w - 2), n_cols))
    n_marks = int(overrides.get("n_marks_per_col",
                                ctx.draw_int("n_marks_per_col", 3, 5)))
    n_marks = max(2, min(min(7, h), n_marks))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 7, 8]
    elif palette_kind == "small":
        pool = [1, 2, 3]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(pool)
    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", 3, 5)))
    palette = pool[:max(2, n_palette)]
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIAS)))
    g = full_grid(h, w, 0)
    cols = _pick_cols(bias, w, n_cols, rng)
    for c in cols:
        rows = sorted(rng.sample(range(h), min(n_marks, h)))
        for i, r in enumerate(rows):
            if i == len(rows) - 1:
                g[r][c] = 5
            else:
                g[r][c] = rng.choice(palette)
    return g


def _pick_cols(bias, w, n, rng):
    avail = list(range(1, w - 1))
    if not avail:
        return [w // 2]
    if bias == "center":
        center = w // 2
        avail.sort(key=lambda c: abs(c - center))
        return avail[:n]
    if bias == "edge":
        avail.sort(key=lambda c: -min(c, w - 1 - c))
        return avail[:n]
    return rng.sample(avail, min(n, len(avail)))


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_cols":
        return g
    if name == "no_5s":
        for c in [w // 3, 2 * w // 3]:
            for r in [1, h - 2]:
                if 0 <= r < h and 0 <= c < w:
                    g[r][c] = rng.choice([1, 2, 3])
        return g
    if name == "all_5s":
        for c in range(0, w, 2):
            for r in range(0, h, 2):
                g[r][c] = 5
        return g
    return g
