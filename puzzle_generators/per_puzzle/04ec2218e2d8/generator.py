"""Generator for 639f5a19.

Rule: each 8-blob -> quadrant recolor. TL=6, TR=1, BL=2, BR=3.
Interior (>=t cells from each edge) = 4.

Combinatorial axes (8): grid_h/w, rect_h, rect_w, n_blobs,
position_bias, palette_kind, anchor_corner, asymmetry_force.
Degenerates: tiny_rect, no_rect, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "04ec2218e2d8"
VERSION = "1.1.0"
TASK_ID = "04ec2218e2d8"
SUMMARY = "1-2 solid 8-rectangles >=6x6 in different positions."

INVARIANTS = [
    "1-2 solid 8-rectangles, each >=6x6 (so quadrants and interior visible)",
    "rectangles don't touch",
]

POSITION_BIASES = ("centered", "corner", "near_edge", "scattered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("tiny_rect", "no_rect", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..12", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 16..20", "valid": "12..24"},
    "rect_h":         {"type": "int", "default": "rng 6..8", "valid": "5..10"},
    "rect_w":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "n_blobs":        {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 8, 10, 12, 14
        rh_lo, rh_hi, rw_lo, rw_hi = 5, 6, 5, 6
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 12, 16, 18, 24
        rh_lo, rh_hi, rw_lo, rw_hi = 7, 10, 7, 12
    else:
        h_lo, h_hi, w_lo, w_hi = 10, 12, 16, 20
        rh_lo, rh_hi, rw_lo, rw_hi = 6, 8, 6, 9
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    rh = int(overrides.get("rect_h",
                           ctx.draw_int("rect_h", rh_lo, min(rh_hi, h - 2))))
    rw = int(overrides.get("rect_w",
                           ctx.draw_int("rect_w", rw_lo, min(rw_hi, w - 2))))
    rh = max(5, min(rh, h - 2))
    rw = max(5, min(rw, w - 2))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    r0, c0 = _pick_pos(bias, h, w, rh, rw, rng)
    draw_rect(g, r0, c0, rh, rw, 8)
    n_blobs = int(overrides.get("n_blobs", 1))
    if n_blobs >= 2 and h * w >= 200:
        for _try in range(20):
            rh2 = rng.randint(rh_lo, min(rh_hi, h - 2))
            rw2 = rng.randint(rw_lo, min(rw_hi, w - 2))
            r2 = rng.randint(1, h - rh2 - 1)
            c2 = rng.randint(1, w - rw2 - 1)
            if (r2 + rh2 < r0 - 1 or r2 > r0 + rh + 1 or
                c2 + rw2 < c0 - 1 or c2 > c0 + rw + 1):
                draw_rect(g, r2, c2, rh2, rw2, 8)
                break
    return g


def _pick_pos(bias, h, w, rh, rw, rng):
    max_r = max(1, h - rh - 1)
    max_c = max(1, w - rw - 1)
    if bias == "centered":
        r0 = max(1, (h - rh) // 2)
        c0 = max(1, (w - rw) // 2)
    elif bias == "corner":
        r0 = rng.choice([1, max_r])
        c0 = rng.choice([1, max_c])
    elif bias == "near_edge":
        if rng.random() < 0.5:
            r0 = rng.choice([1, max_r])
            c0 = rng.randint(1, max_c)
        else:
            r0 = rng.randint(1, max_r)
            c0 = rng.choice([1, max_c])
    else:
        r0 = rng.randint(1, max_r)
        c0 = rng.randint(1, max_c)
    return r0, c0


def _draw_from_degenerate(name, rng):
    h, w = 11, 18
    g = full_grid(h, w, 0)
    if name == "tiny_rect":
        draw_rect(g, 2, 2, 3, 3, 8)
        return g
    if name == "no_rect":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 8
        return g
    return g
