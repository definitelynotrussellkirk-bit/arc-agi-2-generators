"""Generator for ddf7fa4f.

Rule: top row markers + 5-rectangles below. Each 5-rect recolored to
nearest top-row marker's color.

Combinatorial axes (8): grid_h/w, n_markers, n_rects, marker_layout,
rect_size_kind, palette_kind, position_bias, anchor_corner.
Degenerates: no_markers, no_rects, single_marker.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "424c822d69f3"
VERSION = "1.1.0"
TASK_ID = "424c822d69f3"
SUMMARY = "Top markers + 5-rects below; rule recolors rects to nearest marker."

INVARIANTS = [
    "background is 0",
    ">=2 marker cells in row 0 with distinct non-bg colors",
    ">=1 solid 5-rectangle below row 1, non-overlapping with markers",
    "no color 5 in markers (rule treats 5 as the rect-marker)",
]

MARKER_LAYOUTS = ("evenly_spaced", "left_biased", "right_biased",
                  "scattered", "edges")
RECT_SIZE_KINDS = ("small", "medium", "large", "varied")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("no_markers", "no_rects", "single_marker")
HELPFUL_TEXTURES = MARKER_LAYOUTS

AXES = {
    "grid_h":          {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":          {"type": "int", "default": "rng 9..16", "valid": "8..20"},
    "n_markers":       {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "n_rects":         {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "marker_layout":   {"type": "str", "default": "rng helpful",
                        "valid": "|".join(MARKER_LAYOUTS)},
    "rect_size_kind":  {"type": "str", "default": "rng helpful",
                        "valid": "|".join(RECT_SIZE_KINDS)},
    "palette_kind":    {"type": "str", "default": "rng helpful",
                        "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":   {"type": "bool", "default": "false",
                        "valid": "true|false"},
    "texture":         {"type": "str", "default": "alias for marker_layout",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 6, 9, 8, 11
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 13, 18, 15, 20
    else:
        h_lo, h_hi, w_lo, w_hi = 8, 14, 9, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_markers = int(overrides.get("n_markers",
                                  ctx.draw_int("n_markers", 3, 4)))
    n_markers = max(2, min(min(6, w), n_markers))
    n_rects = int(overrides.get("n_rects",
                                ctx.draw_int("n_rects", 2, 3)))
    n_rects = max(1, min(5, n_rects))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 7, 8]
    elif palette_kind == "small":
        pool = [1, 2, 3]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(pool)
    palette = pool[:n_markers]
    while len(palette) < n_markers:
        palette.append(palette[0])
    layout = (overrides.get("texture") or
              overrides.get("marker_layout")
              or ctx.draw_choice("marker_layout",
                                 list(MARKER_LAYOUTS)))
    rect_kind = overrides.get("rect_size_kind",
                              ctx.draw_choice("rect_size_kind",
                                              list(RECT_SIZE_KINDS)))
    g = full_grid(h, w, 0)
    marker_cols = _layout_markers(layout, w, n_markers, rng)
    for c, color in zip(marker_cols, palette):
        if 0 <= c < w:
            g[0][c] = color
    occupied_cols = set()
    for _ in range(n_rects * 5):
        if len(occupied_cols) // 2 >= n_rects:
            break
        rh, rw = _rect_dims(rect_kind, rng)
        for _try in range(40):
            r0 = rng.randint(2, max(2, h - rh - 1))
            c0 = rng.randint(0, w - rw)
            if any(c in occupied_cols for c in range(c0, c0 + rw)):
                continue
            if any(g[rr][cc] != 0
                   for rr in range(max(0, r0 - 1), min(h, r0 + rh + 1))
                   for cc in range(c0, c0 + rw)):
                continue
            draw_rect(g, r0, c0, rh, rw, 5)
            for c in range(c0, c0 + rw):
                occupied_cols.add(c)
            break
    if not any(g[r][c] == 5 for r in range(h) for c in range(w)):
        if h >= 4 and w >= 3:
            draw_rect(g, h // 2, 0, 2, 2, 5)
    return g


def _layout_markers(layout, w, n, rng):
    if layout == "evenly_spaced":
        step = max(1, w // (n + 1))
        return [step * (i + 1) for i in range(n) if step * (i + 1) < w]
    if layout == "left_biased":
        return list(range(n))
    if layout == "right_biased":
        return list(range(w - n, w))
    if layout == "edges":
        return [0, w - 1] + sorted(rng.sample(range(1, w - 1), max(0, n - 2)))
    cols = list(range(w))
    rng.shuffle(cols)
    return sorted(cols[:n])


def _rect_dims(kind, rng):
    if kind == "small":
        return rng.randint(2, 3), rng.randint(2, 3)
    if kind == "medium":
        return rng.randint(3, 4), rng.randint(3, 4)
    if kind == "large":
        return rng.randint(4, 5), rng.randint(4, 5)
    return rng.randint(2, 4), rng.randint(2, 4)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_markers":
        if h >= 3 and w >= 3:
            draw_rect(g, 2, 2, 2, 2, 5)
        return g
    if name == "no_rects":
        for c in range(0, w, 2):
            g[0][c] = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
        return g
    if name == "single_marker":
        g[0][w // 2] = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
        if h >= 3 and w >= 3:
            draw_rect(g, 2, 2, 2, 2, 5)
        return g
    return g
