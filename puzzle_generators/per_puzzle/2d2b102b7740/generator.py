"""Generator for puzzle 0b17323b.

Rule: 1-cells form a line (≥2, sorted by row, constant step (dr, dc)).
Compute step from first to second 1, extend from the last 1 with that
step until out-of-bounds, painting 2s.

Combinatorial axes (8): grid_h/w, n_blues, step_dr, step_dc,
position_bias, line_orientation, anchor_corner, asymmetry_force.
Degenerates: same_position, two_blues_only, line_at_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2d2b102b7740"
VERSION = "1.1.0"
TASK_ID = "2d2b102b7740"
SUMMARY = "2-4 collinear blue cells with constant step; rule extends with 2s."

INVARIANTS = [
    "background is 0",
    "exactly 2-4 cells of color 1",
    "blue cells collinear with constant step (dr, dc) where dr+|dc| > 0",
    "extension fits in-bounds for >=1 cell",
]

LINE_ORIENTS = ("horizontal", "vertical", "diagonal_dr",
                "diagonal_dl", "knight", "steep_diag")
DEGENERATE_TEXTURES = ("same_position", "two_blues_only", "line_at_edge")
HELPFUL_TEXTURES = LINE_ORIENTS

AXES = {
    "grid_h":          {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":          {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "n_blues":         {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "line_orientation":{"type": "str", "default": "rng helpful",
                        "valid": "|".join(LINE_ORIENTS)},
    "step_dr":         {"type": "int", "default": "from orientation",
                        "valid": "0..3"},
    "step_dc":         {"type": "int", "default": "from orientation",
                        "valid": "-3..3"},
    "position_bias":   {"type": "str", "default": "rng spread|corner|center",
                        "valid": "spread|corner|center"},
    "anchor_corner":   {"type": "bool", "default": "false",
                        "valid": "true|false"},
    "texture":         {"type": "str", "default": "alias for line_orientation",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 9
    elif difficulty == "hard":
        h_lo, h_hi = 13, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 2, h_hi + 2)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_blues = int(overrides.get("n_blues",
                                ctx.draw_int("n_blues", 2, 3)))
    n_blues = max(2, min(5, n_blues))
    orient = (overrides.get("texture") or
              overrides.get("line_orientation")
              or ctx.draw_choice("line_orientation",
                                 list(LINE_ORIENTS)))
    bias = overrides.get("position_bias",
                         ctx.draw_choice("position_bias",
                                         ["spread", "corner", "center"]))
    dr, dc = _orient_to_step(orient, rng)
    if "step_dr" in overrides:
        dr = int(overrides["step_dr"])
    if "step_dc" in overrides:
        dc = int(overrides["step_dc"])
    if dr == 0 and dc == 0:
        dr = 1
    g = full_grid(h, w, 0)
    if dr >= 0 and dc >= 0:
        max_r0 = h - 1 - max(0, (n_blues - 1) * dr)
        max_c0 = w - 1 - max(0, (n_blues - 1) * dc)
        min_r0 = 0
        min_c0 = max(0, -((n_blues - 1) * dc))
    else:
        min_r0 = max(0, -((n_blues - 1) * dr))
        max_r0 = h - 1 - max(0, (n_blues - 1) * dr)
        if dc < 0:
            min_c0 = -((n_blues - 1) * dc)
            max_c0 = w - 1
        else:
            min_c0 = 0
            max_c0 = w - 1 - (n_blues - 1) * dc
    if max_r0 < min_r0 or max_c0 < min_c0:
        dr, dc = 1, 1
        min_r0 = 0; max_r0 = max(0, h - 1 - (n_blues - 1) * dr)
        min_c0 = 0; max_c0 = max(0, w - 1 - (n_blues - 1) * dc)
    if bias == "corner":
        r0 = min_r0
        c0 = min_c0
    elif bias == "center":
        r0 = (min_r0 + max_r0) // 2
        c0 = (min_c0 + max_c0) // 2
    else:
        r0 = rng.randint(min_r0, max_r0) if max_r0 >= min_r0 else min_r0
        c0 = rng.randint(min_c0, max_c0) if max_c0 >= min_c0 else min_c0
    if bool(overrides.get("anchor_corner", False)):
        r0 = 0; c0 = 0 if dc >= 0 else w - 1
    for i in range(n_blues):
        rr = r0 + i * dr; cc = c0 + i * dc
        if 0 <= rr < h and 0 <= cc < w:
            g[rr][cc] = 1
    return g


def _orient_to_step(orient, rng):
    if orient == "horizontal":
        return 0, rng.choice([1, 2])
    if orient == "vertical":
        return rng.choice([1, 2]), 0
    if orient == "diagonal_dr":
        return 1, 1
    if orient == "diagonal_dl":
        return 1, -1
    if orient == "knight":
        return rng.choice([1, 2]), rng.choice([1, 2])
    if orient == "steep_diag":
        return rng.choice([2, 3]), 1
    return 1, 1


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "same_position":
        g[h // 2][w // 2] = 1
        return g
    if name == "two_blues_only":
        g[2][2] = 1
        g[3][3] = 1
        return g
    if name == "line_at_edge":
        for c in range(min(w, 5)):
            g[0][c] = 1
        return g
    return g
