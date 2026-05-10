"""Generator for puzzle 37ce87bb.

Rule: bg=7. Two vertical bars at the bottom: one of color 8, one of 2.
Compute |height_8 - height_2| = h_diff. Place 5-cells in column
(last_bar_col + 2), spanning the bottom h_diff rows.

Combinatorial axes (8): grid_h/w, col_8_position, col_2_position,
bar_h_8, bar_h_2, bg_color, anchor_corner, asymmetry_force.
Degenerates: equal_heights, no_8_bar, single_bar.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b34d330a5426"
VERSION = "1.1.0"
TASK_ID = "b34d330a5426"
SUMMARY = "bg=7 with two vertical bars (8 and 2) at bottom; rule adds 5-bar of |diff|."

INVARIANTS = [
    "bg = 7",
    "exactly one column with bottom-cell = 8 (8-bar)",
    "exactly one column with bottom-cell = 2 (2-bar)",
    "8-bar height != 2-bar height",
    "(2-bar col + 2) is in-bounds",
]

POSITION_BIASES = ("close", "far", "left_first", "right_first", "centered")
DEGENERATE_TEXTURES = ("equal_heights", "no_8_bar", "single_bar")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..12", "valid": "6..16"},
    "col_8":          {"type": "int", "default": "rng 1..3", "valid": "0..w-5"},
    "col_2":          {"type": "int", "default": "rng col_8+2..w-4",
                       "valid": "col_8+2..w-3"},
    "bar_h_8":        {"type": "int", "default": "rng 2..h-1",
                       "valid": "1..h-1"},
    "bar_h_2":        {"type": "int", "default": "rng 2..h-1 (≠bar_h_8)",
                       "valid": "1..h-1"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 7
    elif difficulty == "hard":
        h_lo, h_hi = 10, 14
    else:
        h_lo, h_hi = 6, 10
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 1, h_hi + 2)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    g = full_grid(h, w, 7)
    col_8, col_2 = _pick_positions(bias, w, rng)
    if "col_8" in overrides:
        col_8 = int(overrides["col_8"])
    if "col_2" in overrides:
        col_2 = int(overrides["col_2"])
    col_8 = max(0, min(w - 5, col_8))
    col_2 = max(col_8 + 2, min(w - 3, col_2))
    bar_h_8 = int(overrides.get("bar_h_8",
                                ctx.draw_int("bar_h_8", 2, max(2, h - 1))))
    bar_h_2 = int(overrides.get("bar_h_2",
                                ctx.draw_int("bar_h_2", 2, max(2, h - 1))))
    bar_h_8 = max(1, min(h - 1, bar_h_8))
    bar_h_2 = max(1, min(h - 1, bar_h_2))
    while bar_h_2 == bar_h_8:
        bar_h_2 = max(1, min(h - 1, bar_h_2 + 1 if bar_h_2 < h - 1 else bar_h_2 - 1))
    for r in range(h - bar_h_8, h):
        g[r][col_8] = 8
    for r in range(h - bar_h_2, h):
        g[r][col_2] = 2
    return g


def _pick_positions(bias, w, rng):
    if bias == "close":
        col_8 = rng.randint(1, max(1, w - 6))
        col_2 = col_8 + 2
        return col_8, col_2
    if bias == "far":
        col_8 = 1
        col_2 = w - 4
        return col_8, col_2
    if bias == "left_first":
        col_8 = 1
        col_2 = rng.randint(3, w - 4)
        return col_8, col_2
    if bias == "right_first":
        col_8 = rng.randint(1, max(1, w - 6))
        col_2 = w - 4
        return col_8, col_2
    if bias == "centered":
        mid = w // 2
        return max(1, mid - 2), min(w - 4, mid + 1)
    col_8 = rng.randint(1, max(1, w - 6))
    col_2 = rng.randint(col_8 + 2, max(col_8 + 2, w - 4))
    return col_8, col_2


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 7)
    if name == "equal_heights":
        # Equal heights → no 5-bar in output
        col_8 = 1; col_2 = w - 4
        bar_h = h // 2
        for r in range(h - bar_h, h):
            g[r][col_8] = 8
            g[r][col_2] = 2
        return g
    if name == "no_8_bar":
        # Only the 2-bar → rule has no 8 to compare
        col_2 = 2
        for r in range(h - 3, h):
            g[r][col_2] = 2
        return g
    if name == "single_bar":
        # Only the 8-bar
        col_8 = 1
        for r in range(h - 3, h):
            g[r][col_8] = 8
        return g
    return g
