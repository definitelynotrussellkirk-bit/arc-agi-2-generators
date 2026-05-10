"""Generator for 2601afb7.

Rule: 7-bg with vertical bars at distinct cols; rule rotates colors
right by 1 and heights left by 1.

Combinatorial axes (8): grid_h/w, n_bars, palette_kind, height_skew,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: equal_heights, single_bar, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "44e865b6a43e"
VERSION = "1.1.0"
TASK_ID = "44e865b6a43e"
SUMMARY = "7-bg with 3-5 vertical bars at distinct cols, distinct heights and colors."

INVARIANTS = [
    "bg = 7",
    "3-5 vertical bars at distinct cols",
    "each bar reaches the bottom row",
    "bars have distinct heights and distinct non-7 colors",
]

POSITION_BIASES = ("scattered", "left_lean", "right_lean", "centered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("equal_heights", "single_bar", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "n_bars":         {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "height_skew":    {"type": "str", "default": "rng",
                       "valid": "ascending|descending|mixed"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..6"},
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
        h_lo, h_hi, w_lo, w_hi = 6, 8, 8, 10
        nb_lo, nb_hi = 2, 3
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 11, 12, 12, 14
        nb_lo, nb_hi = 4, 6
    else:
        h_lo, h_hi, w_lo, w_hi = 8, 10, 9, 11
        nb_lo, nb_hi = 3, 5
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = [[7] * w for _ in range(h)]
    n_bars = int(overrides.get("n_bars",
                               ctx.draw_int("n_bars", nb_lo, nb_hi)))
    n_bars = max(2, min(min(w - 2, h - 1, 6), n_bars))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, n_bars, rng)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    if bias == "left_lean":
        cols = sorted(rng.sample(range(1, max(2, w // 2 + 1)), n_bars))
    elif bias == "right_lean":
        cols = sorted(rng.sample(range(max(1, w // 2), w - 1), n_bars))
    elif bias == "centered":
        cr = w // 2
        rad = max(1, w // 3)
        candidates = list(range(max(1, cr - rad), min(w - 1, cr + rad)))
        if len(candidates) < n_bars:
            candidates = list(range(1, w - 1))
        cols = sorted(rng.sample(candidates, n_bars))
    else:
        cols = sorted(rng.sample(range(1, w - 1), n_bars))
    heights = rng.sample(range(1, h), n_bars)
    skew = overrides.get("height_skew",
                         ctx.draw_choice("height_skew",
                                         ["ascending", "descending", "mixed"]))
    if skew == "ascending":
        heights = sorted(heights)
    elif skew == "descending":
        heights = sorted(heights, reverse=True)
    for c, ht, color in zip(cols, heights, palette):
        for r in range(h - ht, h):
            g[r][c] = color
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
    h, w = 9, 10
    g = [[7] * w for _ in range(h)]
    if name == "equal_heights":
        for c in [2, 4, 6]:
            for r in range(h - 3, h):
                g[r][c] = 2
        return g
    if name == "single_bar":
        for r in range(h - 4, h):
            g[r][5] = 3
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 4
        return g
    return g
