"""Generator for 1c02dbbe.

Rule: 5-region defines bbox. For each non-{0,5} marker outside, project
into 5-region by clamping to bbox; fill from marker corner to bbox
corner with marker color.

Combinatorial axes (8): grid_h/w, rect_h, rect_w, n_markers,
position_bias, marker_color, palette_kind, anchor_corner.
Degenerates: no_markers, marker_inside, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "3a4b67ab16ff"
VERSION = "1.1.0"
TASK_ID = "3a4b67ab16ff"
SUMMARY = "Solid 5-rectangle + 1-3 marker cells outside."

INVARIANTS = [
    "1 solid 5-rectangle >=3x6",
    "1-3 single non-{0,5} marker cells outside the 5-region",
]

POSITION_BIASES = ("centered", "corner", "near_edge", "scattered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "marker_inside", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 13..16", "valid": "10..20"},
    "rect_h":         {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "rect_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "n_markers":      {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
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
        h_lo, h_hi, w_lo, w_hi = 5, 7, 10, 12
        rh_lo, rh_hi, rw_lo, rw_hi = 2, 2, 6, 7
        nm_lo, nm_hi = 1, 1
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 9, 14, 16, 20
        rh_lo, rh_hi, rw_lo, rw_hi = 3, 4, 8, 12
        nm_lo, nm_hi = 2, 4
    else:
        h_lo, h_hi, w_lo, w_hi = 7, 9, 13, 16
        rh_lo, rh_hi, rw_lo, rw_hi = 2, 3, 7, 10
        nm_lo, nm_hi = 1, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    rh = int(overrides.get("rect_h",
                           ctx.draw_int("rect_h", rh_lo, min(rh_hi, h - 4))))
    rw = int(overrides.get("rect_w",
                           ctx.draw_int("rect_w", rw_lo, min(rw_hi, w - 4))))
    rh = max(2, min(rh, h - 4))
    rw = max(5, min(rw, w - 4))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    r0, c0 = _pick_rect_pos(bias, h, w, rh, rw, rng)
    draw_rect(g, r0, c0, rh, rw, 5)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, rng)
    n_markers = int(overrides.get("n_markers",
                                  ctx.draw_int("n_markers", nm_lo, nm_hi)))
    n_markers = max(1, min(4, n_markers))
    color = rng.choice(pal)
    for _ in range(n_markers):
        for _try in range(30):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] == 0 and not (r0 <= r < r0 + rh and c0 <= c < c0 + rw):
                g[r][c] = color
                break
    return g


def _pick_rect_pos(bias, h, w, rh, rw, rng):
    max_r = max(2, h - rh - 2)
    max_c = max(2, w - rw - 2)
    if bias == "centered":
        r0 = max(2, (h - rh) // 2 + rng.randint(-1, 1))
        c0 = max(2, (w - rw) // 2 + rng.randint(-1, 1))
    elif bias == "corner":
        r0 = rng.choice([2, max_r])
        c0 = rng.choice([2, max_c])
    elif bias == "near_edge":
        if rng.random() < 0.5:
            r0 = rng.choice([2, max_r])
            c0 = rng.randint(2, max_c)
        else:
            r0 = rng.randint(2, max_r)
            c0 = rng.choice([2, max_c])
    else:
        r0 = rng.randint(2, max_r)
        c0 = rng.randint(2, max_c)
    r0 = max(2, min(r0, max_r))
    c0 = max(2, min(c0, max_c))
    return r0, c0


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (0, 5)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 7, 14
    g = full_grid(h, w, 0)
    if name == "no_markers":
        draw_rect(g, 2, 2, 3, 9, 5)
        return g
    if name == "marker_inside":
        draw_rect(g, 2, 2, 3, 9, 5)
        g[3][6] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
