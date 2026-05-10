"""Generator for puzzle ce9e57f2.

Rule: every red(2) vertical bar gets its bottom floor(h/2) cells
recolored to cyan(8).

Combinatorial axes (8): grid_h/w, n_bars, bar_h_min, bar_h_max,
bar_layout, bar_position, palette_size, asymmetry_force.
Degenerates: no_bars, single_bar, full_grid_bar.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1a92a12bac06"
VERSION = "1.1.0"
TASK_ID = "1a92a12bac06"
SUMMARY = "Red vertical bars; rule paints bottom half of each bar cyan."

INVARIANTS = [
    "background is 0",
    ">=2 red(2) vertical bars",
    "bars are at distinct columns (4-conn separated)",
    "each bar has height >=2 (so floor(h/2) >=1)",
]

BAR_LAYOUTS = ("evenly_spaced", "left_heavy", "right_heavy",
               "clustered", "scattered")
DEGENERATE_TEXTURES = ("no_bars", "single_bar", "full_grid_bar")
HELPFUL_TEXTURES = BAR_LAYOUTS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "n_bars":         {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "bar_h_min":      {"type": "int", "default": "2", "valid": "2..6"},
    "bar_h_max":      {"type": "int", "default": "rng 4..7", "valid": "3..12"},
    "bar_layout":     {"type": "str", "default": "rng helpful",
                       "valid": "|".join(BAR_LAYOUTS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for bar_layout",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 9
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_bars = int(overrides.get("n_bars",
                               ctx.draw_int("n_bars", 2, 4)))
    n_bars = max(2, min(6, min(w, n_bars)))
    bar_h_min = int(overrides.get("bar_h_min", 2))
    bar_h_max = int(overrides.get("bar_h_max",
                                  ctx.draw_int("bar_h_max", 4, 7)))
    bar_h_min = max(2, min(h - 1, bar_h_min))
    bar_h_max = max(bar_h_min, min(h - 1, bar_h_max))
    layout = (overrides.get("texture") or
              overrides.get("bar_layout")
              or ctx.draw_choice("bar_layout", list(BAR_LAYOUTS)))
    g = full_grid(h, w, 0)
    cols = _pick_cols(layout, n_bars, w, rng)
    for c in cols:
        bar_h = rng.randint(bar_h_min, bar_h_max)
        bar_top = rng.randint(0, h - bar_h)
        for r in range(bar_top, bar_top + bar_h):
            g[r][c] = 2
    return g


def _pick_cols(layout, n, w, rng):
    if layout == "evenly_spaced":
        step = max(1, w // (n + 1))
        cols = [step + i * step for i in range(n)]
        return [c for c in cols if 0 <= c < w][:n]
    if layout == "left_heavy":
        return [i for i in range(n) if i < w]
    if layout == "right_heavy":
        return [w - 1 - i for i in range(n) if w - 1 - i >= 0]
    if layout == "clustered":
        start = rng.randint(0, max(0, w - n))
        return list(range(start, start + n))
    cols = list(range(w))
    rng.shuffle(cols)
    return sorted(cols[:n])


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_bars":
        # No 2s — rule has no work
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.1:
                    g[r][c] = rng.choice([1, 3, 4, 5, 6, 7, 8, 9])
        return g
    if name == "single_bar":
        c = w // 2
        for r in range(h):
            g[r][c] = 2
        return g
    if name == "full_grid_bar":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
