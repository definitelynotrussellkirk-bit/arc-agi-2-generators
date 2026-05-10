"""Generator for a65b410d.

Rule: row with 2-cells, bar length L. Above: triangles of 3s expanding
up. Below: triangles of 1s shrinking down.

Combinatorial axes (8): grid_h/w, bar_length, bar_row_position,
position_bias, anchor_corner, asymmetry_force, edge_avoidance,
n_decoy_pixels.
Degenerates: no_bar, full_row_bar, multiple_bars.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e0fc08522773"
VERSION = "1.1.0"
TASK_ID = "e0fc08522773"
SUMMARY = "Single horizontal 2-bar at left edge; rule expands triangles above/below."

INVARIANTS = [
    "background is 0",
    "exactly one horizontal 2-bar starting at col 0",
    "bar_len in [2, 4]",
    "bar_row in [2, h-3] (room above/below)",
    "bar_len + bar_row <= w (top triangle fits)",
    "no colors 1, 3 in input (rule writes them for output)",
]

POSITION_BIAS = ("center", "spread", "top", "bottom")
DEGENERATE_TEXTURES = ("no_bar", "full_row_bar", "multiple_bars")
HELPFUL_TEXTURES = POSITION_BIAS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 7..14", "valid": "5..18"},
    "grid_w":            {"type": "int", "default": "rng 8..16", "valid": "6..20"},
    "bar_length":        {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "bar_row_position":  {"type": "str", "default": "rng helpful",
                          "valid": "|".join(POSITION_BIAS)},
    "anchor_corner":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "asymmetry_force":   {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "edge_avoidance":    {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "anchor_left":       {"type": "bool", "default": "true",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for bar_row_position",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 5, 8, 6, 9
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 12, 18, 14, 20
    else:
        h_lo, h_hi, w_lo, w_hi = 7, 14, 8, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    bar_len = int(overrides.get("bar_length",
                                ctx.draw_int("bar_length", 2, min(4, w - 2))))
    bar_len = max(2, min(min(6, w - 2), bar_len))
    pos_kind = (overrides.get("texture") or
                overrides.get("bar_row_position")
                or ctx.draw_choice("bar_row_position",
                                   list(POSITION_BIAS)))
    max_row = min(h - 3, w - bar_len)
    if max_row < 2:
        max_row = max(2, max_row)
    if pos_kind == "center":
        bar_row = (h // 2)
    elif pos_kind == "top":
        bar_row = 2
    elif pos_kind == "bottom":
        bar_row = h - 3
    else:
        bar_row = rng.randint(2, max(2, max_row))
    bar_row = max(2, min(min(h - 3, w - bar_len), bar_row))
    g = full_grid(h, w, 0)
    for c in range(bar_len):
        g[bar_row][c] = 2
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_bar":
        return g
    if name == "full_row_bar":
        for c in range(w):
            g[h // 2][c] = 2
        return g
    if name == "multiple_bars":
        for c in range(2):
            g[2][c] = 2
            g[h - 3][c] = 2
        return g
    return g
