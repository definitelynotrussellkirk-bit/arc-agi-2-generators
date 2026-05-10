"""Generator for puzzle e179c5f4.

Rule: single blue(1) cell at bottom row. Rule traces ball-bouncing path
upward, reflecting off side walls. Path cells → 1, others → 8.

Combinatorial axes (8): grid_h/w, blue_col_position, position_bias,
edge_avoidance, asymmetry_force, n_decoy_pixels, anchor_corner,
column_choice_kind.
Degenerates: no_blue, multiple_blues, blue_top_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f51eb638b973"
VERSION = "1.1.0"
TASK_ID = "f51eb638b973"
SUMMARY = "Single blue at bottom row; rule traces ball-bouncing path upward."

INVARIANTS = [
    "background is 0",
    "exactly one blue(1) cell",
    "blue cell is at the bottom row of the grid",
    "no color 8 in input (rule writes 8 for output)",
]

POSITION_BIAS = ("center", "left_edge", "right_edge", "spread")
DEGENERATE_TEXTURES = ("no_blue", "multiple_blues", "blue_top_row")
HELPFUL_TEXTURES = POSITION_BIAS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 6..14", "valid": "4..18"},
    "grid_w":            {"type": "int", "default": "rng 6..14", "valid": "4..18"},
    "blue_col_position": {"type": "int", "default": "rng 0..w-1",
                          "valid": "0..w-1"},
    "position_bias":     {"type": "str", "default": "rng helpful",
                          "valid": "|".join(POSITION_BIAS)},
    "anchor_corner":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "edge_avoidance":    {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "asymmetry_force":   {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "column_choice_kind": {"type": "str", "default": "rng spread|center",
                           "valid": "spread|center"},
    "texture":           {"type": "str", "default": "alias for position_bias",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 4, 7
    elif difficulty == "hard":
        h_lo, h_hi = 12, 18
    else:
        h_lo, h_hi = 6, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    pos_bias = (overrides.get("texture") or
                overrides.get("position_bias")
                or ctx.draw_choice("position_bias", list(POSITION_BIAS)))
    if pos_bias == "center":
        sc = w // 2
    elif pos_bias == "left_edge":
        sc = 0
    elif pos_bias == "right_edge":
        sc = w - 1
    else:
        sc = rng.randint(0, w - 1)
    if "blue_col_position" in overrides:
        sc = max(0, min(w - 1, int(overrides["blue_col_position"])))
    g = full_grid(h, w, 0)
    g[h - 1][sc] = 1
    if bool(overrides.get("anchor_corner", False)):
        g[h - 1][0] = 1
        # Only one blue
        for c in range(1, w):
            if g[h - 1][c] == 1:
                g[h - 1][c] = 0
        g[h - 1][0] = 1
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_blue":
        return g
    if name == "multiple_blues":
        g[h - 1][0] = 1
        g[h - 1][w - 1] = 1
        return g
    if name == "blue_top_row":
        g[0][w // 2] = 1
        return g
    return g
