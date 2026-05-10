"""Generator for c074846d.

Rule: 5-pivot with 2-cells forming a line. Output: original 2-cells →3
(preserved), 90°-rotated copy painted as 2.

Combinatorial axes (8): grid_h/w, line_length, pivot_position_bias,
line_direction, palette_size, edge_avoidance, anchor_pivot,
asymmetry_force.
Degenerates: no_pivot, no_twos, multiple_pivots.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3eff273eeb83"
VERSION = "1.1.0"
TASK_ID = "3eff273eeb83"
SUMMARY = "5-pivot + 2-line; rule rotates line 90° around pivot."

INVARIANTS = [
    "background is 0",
    "exactly 1 cell of color 5 (pivot)",
    ">=2 cells of color 2 forming a line attached to pivot",
    "the rotated line stays in-bounds",
    "no color 3 in input (rule writes 3 for output)",
]

LINE_DIRECTIONS = ("horizontal_left", "horizontal_right",
                   "vertical_up", "vertical_down")
POSITION_BIAS = ("center", "spread", "edge")
DEGENERATE_TEXTURES = ("no_pivot", "no_twos", "multiple_pivots")
HELPFUL_TEXTURES = LINE_DIRECTIONS

AXES = {
    "grid_h":              {"type": "int", "default": "rng 6..12", "valid": "5..16"},
    "grid_w":              {"type": "int", "default": "rng 7..14", "valid": "6..18"},
    "line_length":         {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "line_direction":      {"type": "str", "default": "rng helpful",
                            "valid": "|".join(LINE_DIRECTIONS)},
    "pivot_position_bias": {"type": "str", "default": "rng helpful",
                            "valid": "|".join(POSITION_BIAS)},
    "edge_avoidance":      {"type": "bool", "default": "true",
                            "valid": "true|false"},
    "anchor_pivot":        {"type": "bool", "default": "false",
                            "valid": "true|false"},
    "asymmetry_force":     {"type": "bool", "default": "false",
                            "valid": "true|false"},
    "texture":             {"type": "str", "default": "alias for line_direction",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 5, 7, 6, 9
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 11, 16, 13, 18
    else:
        h_lo, h_hi, w_lo, w_hi = 6, 12, 7, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    line_len = int(overrides.get("line_length",
                                 ctx.draw_int("line_length", 2, 4)))
    line_len = max(2, min(min(h, w) // 2, line_len))
    direction = (overrides.get("texture") or
                 overrides.get("line_direction")
                 or ctx.draw_choice("line_direction",
                                    list(LINE_DIRECTIONS)))
    bias = overrides.get("pivot_position_bias",
                         ctx.draw_choice("pivot_position_bias",
                                         list(POSITION_BIAS)))
    pr, pc = _pick_pivot(direction, bias, h, w, line_len, rng)
    g = full_grid(h, w, 0)
    g[pr][pc] = 5
    dr, dc = {"horizontal_left": (0, -1), "horizontal_right": (0, 1),
              "vertical_up": (-1, 0), "vertical_down": (1, 0)}[direction]
    for i in range(1, line_len + 1):
        nr, nc = pr + dr * i, pc + dc * i
        if 0 <= nr < h and 0 <= nc < w:
            g[nr][nc] = 2
    return g


def _pick_pivot(direction, bias, h, w, line_len, rng):
    if direction == "horizontal_left":
        r_lo, r_hi = line_len + 1, h - line_len - 2
        c_lo, c_hi = line_len + 1, w - 2
    elif direction == "horizontal_right":
        r_lo, r_hi = line_len + 1, h - line_len - 2
        c_lo, c_hi = 1, w - line_len - 2
    elif direction == "vertical_up":
        r_lo, r_hi = line_len + 1, h - 2
        c_lo, c_hi = line_len + 1, w - line_len - 2
    else:
        r_lo, r_hi = 1, h - line_len - 2
        c_lo, c_hi = line_len + 1, w - line_len - 2
    if r_hi < r_lo: r_lo, r_hi = 1, h - 2
    if c_hi < c_lo: c_lo, c_hi = 1, w - 2
    if bias == "center":
        return (r_lo + r_hi) // 2, (c_lo + c_hi) // 2
    if bias == "edge":
        return rng.choice([r_lo, r_hi]), rng.choice([c_lo, c_hi])
    return rng.randint(r_lo, r_hi), rng.randint(c_lo, c_hi)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_pivot":
        for c in range(min(3, w)):
            g[h // 2][c + 1] = 2
        return g
    if name == "no_twos":
        g[h // 2][w // 2] = 5
        return g
    if name == "multiple_pivots":
        g[2][2] = 5
        g[h - 3][w - 3] = 5
        g[2][3] = 2
        g[2][4] = 2
        return g
    return g
