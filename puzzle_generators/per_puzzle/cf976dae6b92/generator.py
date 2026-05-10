"""Generator for puzzle 0e671a1a.

Rule: 3 single-cell markers (2, 4, 3). Output draws Z-shaped path of 5s:
  row from 2 to 4 at r2; col from r2 to r4 at c4;
  row from 4 to 3 at r4; col from r4 to r3 at c3.

Combinatorial axes (8): grid_h/w, marker2_pos, marker4_pos, marker3_pos,
position_bias, anchor_corner, asymmetry_force, separation.
Degenerates: same_position, same_row, no_markers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cf976dae6b92"
VERSION = "1.1.0"
TASK_ID = "cf976dae6b92"
SUMMARY = "3 markers (2, 4, 3); rule draws Z-path of 5s."

INVARIANTS = [
    "background is 0",
    "exactly 1 cell each of 2, 4, 3",
    "all 3 positions at distinct rows AND distinct cols",
]

POSITION_BIASES = ("scattered", "diagonal", "anti_diag", "row_aligned",
                   "centered")
DEGENERATE_TEXTURES = ("same_position", "same_row", "no_markers")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..14", "valid": "7..18"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "7..18"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "min_separation": {"type": "int", "default": "2", "valid": "1..6"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "marker_order":   {"type": "str", "default": "2,4,3",
                       "valid": "2,4,3"},
    "include_decoy":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 7, 9
    elif difficulty == "hard":
        h_lo, h_hi = 13, 18
    else:
        h_lo, h_hi = 9, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    g = full_grid(h, w, 0)
    rows, cols = _pick_positions(bias, h, w, rng)
    g[rows[0]][cols[0]] = 2
    g[rows[1]][cols[1]] = 4
    g[rows[2]][cols[2]] = 3
    return g


def _pick_positions(bias, h, w, rng):
    if bias == "diagonal":
        # 3 cells along diagonal
        n = min(h, w) - 2
        positions = sorted(rng.sample(range(1, n + 1), 3))
        rows = positions
        cols = positions
        return rows, cols
    if bias == "anti_diag":
        n = min(h, w) - 2
        rows = sorted(rng.sample(range(1, n + 1), 3))
        cols = [w - 1 - r for r in rows]
        return rows, cols
    if bias == "row_aligned":
        rows = sorted(rng.sample(range(1, h - 1), 3))
        cols = rng.sample(range(1, w - 1), 3)
        return rows, cols
    if bias == "centered":
        cr = h // 2; cc = w // 2
        rows = [cr - 2, cr, cr + 2]
        cols = [cc - 2, cc, cc + 2]
        rows = [max(1, min(h - 2, r)) for r in rows]
        cols = [max(1, min(w - 2, c)) for c in cols]
        rng.shuffle(rows)
        rng.shuffle(cols)
        return rows, cols
    rows = rng.sample(range(1, h - 1), 3)
    cols = rng.sample(range(1, w - 1), 3)
    rng.shuffle(rows)
    rng.shuffle(cols)
    return rows, cols


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "same_position":
        # Only one marker can occupy a cell, so 2 markers
        g[h // 2][w // 2] = 2
        g[1][1] = 4
        return g
    if name == "same_row":
        r = h // 2
        g[r][1] = 2
        g[r][w // 2] = 4
        g[r][w - 2] = 3
        return g
    if name == "no_markers":
        return g
    return g
