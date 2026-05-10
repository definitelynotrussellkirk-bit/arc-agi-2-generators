"""Generator for puzzle d4a91cb9.

Rule: one cyan(8) cell + one red(2) cell at distinct rows/cols. Rule
draws an L-path of yellow(4) from cyan to red, with the corner at
(red_row, cyan_col).

Combinatorial axes (8): grid_h/w, distance_kind, cyan_quadrant,
red_quadrant, position_bias, anchor_corner, asymmetry_force,
include_decoy.
Degenerates: same_row, same_col, same_position.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7fdbaba4995e"
VERSION = "1.1.0"
TASK_ID = "7fdbaba4995e"
SUMMARY = "1 cyan + 1 red cell at distinct rows/cols; rule draws L-path of yellow."

INVARIANTS = [
    "background is 0",
    "exactly 1 cyan(8) cell, 1 red(2) cell",
    "cyan and red at different rows AND different columns",
    "no other non-bg cells (rule writes 4 in path)",
]

DISTANCE_KINDS = ("near", "medium", "far", "diagonal", "knight")
QUADRANT_BIASES = ("opposite_corner", "same_corner", "spread", "edge")
DEGENERATE_TEXTURES = ("same_row", "same_col", "same_position")
HELPFUL_TEXTURES = DISTANCE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "5..18"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "5..18"},
    "distance_kind":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DISTANCE_KINDS)},
    "quadrant_bias":  {"type": "str", "default": "rng spread|opposite_corner|same_corner|edge",
                       "valid": "|".join(QUADRANT_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "min_dist":       {"type": "int", "default": "2", "valid": "1..6"},
    "max_dist":       {"type": "int", "default": "min(h,w)-2",
                       "valid": "2..max"},
    "texture":        {"type": "str", "default": "alias for distance_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 8
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    distance = (overrides.get("texture") or
                overrides.get("distance_kind")
                or ctx.draw_choice("distance_kind",
                                   list(DISTANCE_KINDS)))
    quadrant = overrides.get("quadrant_bias",
                             ctx.draw_choice("quadrant_bias",
                                             list(QUADRANT_BIASES)))
    g = full_grid(h, w, 0)
    cy_r, cy_c, re_r, re_c = _pick_endpoints(distance, quadrant, h, w, rng)
    g[cy_r][cy_c] = 8
    g[re_r][re_c] = 2
    return g


def _pick_endpoints(distance, quadrant, h, w, rng):
    if quadrant == "opposite_corner":
        cy_r = rng.randint(0, h // 2 - 1) if h > 2 else 0
        cy_c = rng.randint(0, w // 2 - 1) if w > 2 else 0
        re_r = rng.randint(h // 2, h - 1)
        re_c = rng.randint(w // 2, w - 1)
        return cy_r, cy_c, re_r, re_c
    if quadrant == "same_corner":
        cy_r = rng.randint(0, h // 3) if h > 3 else 0
        cy_c = rng.randint(0, w // 3) if w > 3 else 0
        for _ in range(20):
            re_r = rng.randint(0, h // 2)
            re_c = rng.randint(0, w // 2)
            if re_r != cy_r and re_c != cy_c:
                return cy_r, cy_c, re_r, re_c
    if quadrant == "edge":
        cy_r = rng.choice([0, h - 1])
        cy_c = rng.randint(1, max(1, w - 2))
        for _ in range(20):
            re_r = rng.choice([0, h - 1])
            re_c = rng.randint(1, max(1, w - 2))
            if re_r != cy_r and re_c != cy_c:
                return cy_r, cy_c, re_r, re_c
    # default spread / distance-driven
    target = {"near": 3, "medium": 5, "far": 8,
              "diagonal": min(h, w) - 1, "knight": 2}.get(distance, 4)
    for _ in range(40):
        cy_r = rng.randint(0, h - 1); cy_c = rng.randint(0, w - 1)
        re_r = rng.randint(0, h - 1); re_c = rng.randint(0, w - 1)
        if re_r == cy_r or re_c == cy_c:
            continue
        d = abs(re_r - cy_r) + abs(re_c - cy_c)
        if abs(d - target) <= 2:
            return cy_r, cy_c, re_r, re_c
    cy_r, cy_c = 0, 0
    re_r, re_c = h - 1, w - 1
    return cy_r, cy_c, re_r, re_c


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "same_row":
        r = h // 2
        c1 = rng.randint(0, w // 2 - 1)
        c2 = rng.randint(w // 2, w - 1)
        g[r][c1] = 8
        g[r][c2] = 2
        return g
    if name == "same_col":
        c = w // 2
        r1 = rng.randint(0, h // 2 - 1)
        r2 = rng.randint(h // 2, h - 1)
        g[r1][c] = 8
        g[r2][c] = 2
        return g
    if name == "same_position":
        # Only one cell can hold one color; rule has no red to find
        g[h // 2][w // 2] = 8
        return g
    return g
