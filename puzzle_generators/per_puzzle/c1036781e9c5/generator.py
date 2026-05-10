"""Generator for fcb5c309.

Rule: most-frequent color = frame; pick the largest frame component;
crop to its bbox; replace frame cells with dot color.

Combinatorial axes (8): grid_h/w, frame_h, frame_w, n_outside, n_inside,
position_bias, palette_kind, anchor_corner.
Degenerates: no_frame, single_frame, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "c1036781e9c5"
VERSION = "1.1.0"
TASK_ID = "c1036781e9c5"
SUMMARY = "Sparse dot cells + 1-2 frame rectangles; rule crops larger and recolors."

INVARIANTS = [
    "frame_color appears most overall (in the rectangles)",
    "1-2 rectangles of frame_color, the largest is wider+taller than the smaller",
    "scattered dot-color cells (>=3) outside and >=1 inside the largest frame",
]

POSITION_BIASES = ("right_lean", "centered", "corner", "scattered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "single_frame", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "frame_h":        {"type": "int", "default": "rng 5..8", "valid": "4..10"},
    "frame_w":        {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "n_outside":      {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "n_inside":       {"type": "int", "default": "rng 1..2", "valid": "0..3"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
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
        h_lo, h_hi, w_lo, w_hi = 8, 10, 10, 12
        no_lo, no_hi = 1, 3
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 14, 18, 16, 20
        no_lo, no_hi = 5, 8
    else:
        h_lo, h_hi, w_lo, w_hi = 10, 14, 12, 16
        no_lo, no_hi = 3, 5
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, rng)
    frame_c, dot_c = pal[0], pal[1]
    fh = int(overrides.get("frame_h",
                           rng.randint(5, min(8, h - 2))))
    fw = int(overrides.get("frame_w",
                           rng.randint(6, min(9, w - 2))))
    fh = max(4, min(fh, h - 2))
    fw = max(5, min(fw, w - 2))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    if bias == "right_lean":
        r0 = rng.randint(1, h - fh - 1)
        c0 = max(1, w - fw - 1)
    elif bias == "centered":
        r0 = max(1, (h - fh) // 2)
        c0 = max(1, (w - fw) // 2)
    elif bias == "corner":
        r0 = rng.choice([1, max(1, h - fh - 1)])
        c0 = rng.choice([1, max(1, w - fw - 1)])
    else:
        r0 = rng.randint(1, max(1, h - fh - 1))
        c0 = rng.randint(1, max(1, w - fw - 1))
    draw_rect_outline(g, r0, c0, fh, fw, frame_c)
    sh = rng.randint(3, 4)
    sw = rng.randint(4, 5)
    s_r0 = rng.randint(1, max(1, r0 - sh - 1))
    s_c0 = rng.randint(1, max(1, c0 - sw - 1))
    if s_r0 + sh < h and s_c0 + sw < w:
        draw_rect_outline(g, s_r0, s_c0, sh, sw, frame_c)
    n_outside = int(overrides.get("n_outside",
                                  ctx.draw_int("n_outside", no_lo, no_hi)))
    n_outside = max(1, min(10, n_outside))
    placed = 0
    for _ in range(80):
        if placed >= n_outside:
            break
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] == 0 and not (r0 < r < r0 + fh - 1 and c0 < c < c0 + fw - 1):
            g[r][c] = dot_c
            placed += 1
    n_inside = int(overrides.get("n_inside",
                                 ctx.draw_int("n_inside", 1, 2)))
    n_inside = max(1, min(3, n_inside))
    inside_count = 0
    for _ in range(40):
        if inside_count >= n_inside:
            break
        r = rng.randint(r0 + 1, r0 + fh - 2)
        c = rng.randint(c0 + 1, c0 + fw - 2)
        if g[r][c] == 0:
            g[r][c] = dot_c
            inside_count += 1
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_frame":
        for _ in range(8):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            g[r][c] = 2
        return g
    if name == "single_frame":
        draw_rect_outline(g, 2, 2, 5, 6, 4)
        g[3][4] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 4
        return g
    return g
