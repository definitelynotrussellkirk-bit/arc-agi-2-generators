"""Generator for 17b866bd.

Rule: repeated 5x5 zero/8 lattice is cleaned, and each anomaly colors
the below-right local clean-zero block.

Combinatorial axes (8): tile_repeats, anomaly_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_anomalies, all_anomalies, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a1ece4864521"
VERSION = "1.1.0"
TASK_ID = "a1ece4864521"
SUMMARY = "5x5 zero/8 lattice with anomalies that color below-right blocks."

INVARIANTS = [
    "the clean pattern is periodic modulo 5 in both axes",
    "regular lattice values are only 0 and 8",
    "a few anomaly cells break the lattice with nonzero non-8 colors",
    "each anomaly has clean-zero cells in the 4x4 area below and to its right",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_anomalies", "all_anomalies", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

_TILE = [
    [0, 8, 8, 8, 8],
    [8, 8, 0, 0, 8],
    [8, 0, 0, 0, 0],
    [8, 0, 0, 0, 0],
    [8, 8, 0, 0, 8],
]

AXES = {
    "tile_repeats":   {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "anomaly_count":  {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clean_value(r, c):
    return _TILE[r % 5][c % 5]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        rep_lo, rep_hi, ac_lo, ac_hi = 3, 3, 1, 1
    elif difficulty == "hard":
        rep_lo, rep_hi, ac_lo, ac_hi = 5, 6, 3, 5
    else:
        rep_lo, rep_hi, ac_lo, ac_hi = 3, 5, 1, 3
    repeats = ctx.draw_int("tile_repeats", rep_lo, rep_hi)
    anomaly_count = ctx.draw_int("anomaly_count", ac_lo, ac_hi)
    colors = ctx.draw_distinct_colors("anomaly_colors", n=anomaly_count, exclude={0, 8})
    h = repeats * 5 + rng.randint(0, 2)
    w = repeats * 5 + rng.randint(0, 3)
    g = full_grid(h, w, 0)
    for r in range(h):
        for c in range(w):
            g[r][c] = _clean_value(r, c)
    candidates = [
        (r, c)
        for r in range(0, max(1, h - 5))
        for c in range(0, max(1, w - 5))
        if any(_clean_value(rr, cc) == 0
               for rr in range(r + 1, min(r + 5, h))
               for cc in range(c + 1, min(c + 5, w)))
    ]
    rng.shuffle(candidates)
    for color, (r, c) in zip(colors, candidates):
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h = w = 15
    g = full_grid(h, w, 0)
    for r in range(h):
        for c in range(w):
            g[r][c] = _clean_value(r, c)
    if name == "no_anomalies":
        return g
    if name == "all_anomalies":
        for r in range(h):
            for c in range(w):
                if g[r][c] == 0:
                    g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 8
        return g
    return g
