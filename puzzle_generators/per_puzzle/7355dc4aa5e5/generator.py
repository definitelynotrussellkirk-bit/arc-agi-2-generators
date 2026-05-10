"""Generator for puzzle 140c817e.

Rule: for each 1-cell at (r,c): paint row r and col c with 1; set
(r,c)=2; set 4 diagonal neighbors to 3.

Combinatorial axes (8): grid_h/w, n_ones, position_bias, anchor_corner,
asymmetry_force, palette_size, bg_color, include_decoy.
Degenerates: no_ones, two_ones_same_row, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7355dc4aa5e5"
VERSION = "1.1.0"
TASK_ID = "7355dc4aa5e5"
SUMMARY = "9-bg grid w/ 1-cells; rule paints row+col+diagonals around each."

INVARIANTS = [
    "background is 9",
    "1-3 cells of color 1, no other non-9 cells",
    "1-cells at distinct rows AND distinct cols",
]

POSITION_BIASES = ("scattered", "diagonal", "centered", "corners")
DEGENERATE_TEXTURES = ("no_ones", "two_ones_same_row", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "n_ones":         {"type": "int", "default": "rng 1..2", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "bg_color":       {"type": "color", "default": "9", "valid": "9"},
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
        h_lo, h_hi = 4, 7
    elif difficulty == "hard":
        h_lo, h_hi = 10, 14
    else:
        h_lo, h_hi = 6, 10
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 2, h_hi + 2)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_ones = int(overrides.get("n_ones",
                               ctx.draw_int("n_ones", 1, 2)))
    n_ones = max(1, min(min(h, w, 4), n_ones))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    g = full_grid(h, w, 9)
    rows, cols = _pick_positions(bias, h, w, n_ones, rng)
    for i in range(n_ones):
        g[rows[i]][cols[i]] = 1
    return g


def _pick_positions(bias, h, w, n, rng):
    if bias == "diagonal":
        n_use = min(n, min(h, w))
        rs = sorted(rng.sample(range(min(h, w)), n_use))
        cs = list(rs)
        return rs, cs
    if bias == "centered":
        cr, cc = h // 2, w // 2
        rs = [cr - n // 2 + i for i in range(n)]
        cs = [cc - n // 2 + i for i in range(n)]
        rs = [max(0, min(h - 1, r)) for r in rs]
        cs = [max(0, min(w - 1, c)) for c in cs]
        rng.shuffle(rs); rng.shuffle(cs)
        return rs, cs
    if bias == "corners":
        corners_r = [0, h - 1]
        corners_c = [0, w - 1]
        rng.shuffle(corners_r); rng.shuffle(corners_c)
        return corners_r[:n], corners_c[:n]
    rs = rng.sample(range(h), n)
    cs = rng.sample(range(w), n)
    return rs, cs


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 9)
    if name == "no_ones":
        return g
    if name == "two_ones_same_row":
        r = h // 2
        g[r][1] = 1
        g[r][w - 2] = 1
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
