"""Generator for puzzle a61f2674.

Rule: gray(5) vertical bars (anchored at bottom). Output keeps only
tallest (→blue 1) and shortest (→red 2); removes the rest.

Combinatorial axes (8): grid_h/w, n_bars, height_min, height_max,
column_layout, anchor_corner, asymmetry_force, palette_size.
Degenerates: tied_heights, single_bar, no_bars.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ec7d4f02ef89"
VERSION = "1.1.0"
TASK_ID = "ec7d4f02ef89"
SUMMARY = "Gray bars of distinct heights; rule keeps tallest blue + shortest red."

INVARIANTS = [
    "background is 0",
    "all non-bg cells are gray(5)",
    ">=3 distinct gray vertical bars (bottom-anchored)",
    "heights are pairwise distinct",
]

COLUMN_LAYOUTS = ("scattered", "left_to_right", "right_to_left",
                  "evenly_spaced", "clustered")
DEGENERATE_TEXTURES = ("tied_heights", "single_bar", "no_bars")
HELPFUL_TEXTURES = COLUMN_LAYOUTS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "n_bars":         {"type": "int", "default": "rng 3..5", "valid": "3..7"},
    "height_min":     {"type": "int", "default": "1", "valid": "1..h-1"},
    "height_max":     {"type": "int", "default": "h-1", "valid": "2..h-1"},
    "column_layout":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(COLUMN_LAYOUTS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for column_layout",
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
                               ctx.draw_int("n_bars", 3, 5)))
    n_bars = max(3, min(min(w, 7), n_bars))
    h_min = int(overrides.get("height_min", 1))
    h_max = int(overrides.get("height_max", h - 1))
    h_min = max(1, min(h - 1, h_min))
    h_max = max(h_min + n_bars - 1, min(h - 1, h_max))
    layout = (overrides.get("texture") or
              overrides.get("column_layout")
              or ctx.draw_choice("column_layout",
                                 list(COLUMN_LAYOUTS)))
    heights = rng.sample(range(h_min, h_max + 1),
                          min(n_bars, h_max - h_min + 1))
    while len(heights) < n_bars:
        heights.append(h_min + len(heights))
    cols = _pick_columns(layout, w, n_bars, rng)
    g = full_grid(h, w, 0)
    for col, ht in zip(cols, heights):
        for r in range(h - ht, h):
            g[r][col] = 5
    return g


def _pick_columns(layout, w, n, rng):
    if layout == "left_to_right":
        return list(range(min(n, w)))
    if layout == "right_to_left":
        return list(range(max(0, w - n), w))
    if layout == "evenly_spaced":
        step = max(1, w // (n + 1))
        return [step * (i + 1) for i in range(n) if step * (i + 1) < w][:n]
    if layout == "clustered":
        start = rng.randint(0, max(0, w - n))
        return list(range(start, start + n))
    return rng.sample(range(w), n)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "tied_heights":
        # Multiple bars all same height
        for c in [1, 4, 7]:
            if c < w:
                for r in range(h - 3, h):
                    g[r][c] = 5
        return g
    if name == "single_bar":
        c = w // 2
        for r in range(h - 4, h):
            g[r][c] = 5
        return g
    if name == "no_bars":
        return g
    return g
