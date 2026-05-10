"""Generator for 7e0986d6.

Rule: rectangle + scattered dots; rule absorbs adjacent dots into rect
color, removes isolated dots.

Combinatorial axes (8): grid_h/w, rect_h, rect_w, n_adjacent, n_isolated,
palette_kind, position_bias, anchor_corner.
Degenerates: no_dots, no_rect, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "5bb29951ab1a"
VERSION = "1.1.0"
TASK_ID = "5bb29951ab1a"
SUMMARY = "Rectangle + scattered dots; rule absorbs adjacent dots, removes isolated ones."

INVARIANTS = [
    "background is 0",
    "exactly one solid rectangle of color rect_color (4-connected, >=4 cells)",
    "scattered dots of color dot_color (smaller count than rect_color)",
    ">=1 dot has >=2 adjacent rect cells (absorbed)",
    ">=1 dot is fully isolated from the rect (removed)",
]

POSITION_BIASES = ("centered", "corner", "near_edge", "scattered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_dots", "no_rect", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "rect_h":         {"type": "int", "default": "rng 3..h/3", "valid": "3..7"},
    "rect_w":         {"type": "int", "default": "rng 3..w/3", "valid": "3..7"},
    "n_adjacent":     {"type": "int", "default": "1", "valid": "1..3"},
    "n_isolated":     {"type": "int", "default": "1", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 8, 10
        na_lo, na_hi = 1, 1
        ni_lo, ni_hi = 1, 1
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
        na_lo, na_hi = 2, 3
        ni_lo, ni_hi = 2, 3
    else:
        h_lo, h_hi = 10, 14
        na_lo, na_hi = 1, 2
        ni_lo, ni_hi = 1, 2
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, rng)
    rect_color = pal[0]
    dot_color = pal[1] if len(pal) > 1 else 6
    g = full_grid(h, w, 0)
    rh = int(overrides.get("rect_h",
                           rng.randint(3, max(3, h // 3))))
    rw = int(overrides.get("rect_w",
                           rng.randint(3, max(3, w // 3))))
    rh = max(3, min(rh, h - 3))
    rw = max(3, min(rw, w - 3))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    rr, rc = _pick_pos(bias, h, w, rh, rw, rng)
    draw_rect(g, rr, rc, rh, rw, rect_color)
    n_adj = int(overrides.get("n_adjacent",
                              ctx.draw_int("n_adjacent", na_lo, na_hi)))
    n_iso = int(overrides.get("n_isolated",
                              ctx.draw_int("n_isolated", ni_lo, ni_hi)))
    for _ in range(n_adj):
        for _try in range(15):
            side = rng.choice(["top", "bottom", "left", "right"])
            if side == "top" and rr > 0:
                dr, dc = rr - 1, rng.randint(rc + 1, rc + rw - 2)
            elif side == "bottom" and rr + rh < h:
                dr, dc = rr + rh, rng.randint(rc + 1, rc + rw - 2)
            elif side == "left" and rc > 0:
                dr, dc = rng.randint(rr + 1, rr + rh - 2), rc - 1
            elif side == "right" and rc + rw < w:
                dr, dc = rng.randint(rr + 1, rr + rh - 2), rc + rw
            else:
                continue
            if 0 <= dr < h and 0 <= dc < w and g[dr][dc] == 0:
                g[dr][dc] = dot_color
                break
    for _ in range(n_iso):
        for _try in range(15):
            ir = rng.randint(0, h - 1); ic = rng.randint(0, w - 1)
            if g[ir][ic] != 0:
                continue
            too_close = any(
                abs(ir - (rr + dr)) <= 2 and abs(ic - (rc + dc)) <= 2
                for dr in range(rh) for dc in range(rw)
            )
            if too_close:
                continue
            g[ir][ic] = dot_color
            break
    return g


def _pick_pos(bias, h, w, rh, rw, rng):
    max_r = max(2, h - rh - 2)
    max_c = max(2, w - rw - 2)
    if bias == "centered":
        rr = max(2, (h - rh) // 2)
        rc = max(2, (w - rw) // 2)
    elif bias == "corner":
        rr = rng.choice([2, max_r])
        rc = rng.choice([2, max_c])
    elif bias == "near_edge":
        if rng.random() < 0.5:
            rr = rng.choice([2, max_r])
            rc = rng.randint(2, max_c)
        else:
            rr = rng.randint(2, max_r)
            rc = rng.choice([2, max_c])
    else:
        rr = rng.randint(2, max_r)
        rc = rng.randint(2, max_c)
    return rr, rc


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_dots":
        draw_rect(g, 3, 3, 4, 4, 1)
        return g
    if name == "no_rect":
        g[2][3] = 6; g[8][8] = 6
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
