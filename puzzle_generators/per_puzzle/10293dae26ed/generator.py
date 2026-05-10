"""Generator for puzzle 50cb2852.

Rule: for each non-bg, non-cyan(8) blob with bbox h>=3 and w>=3, set
the strict interior of its bbox to cyan(8).

Combinatorial axes (8): grid_h/w, n_rects, rect_h_min, rect_h_max,
rect_w_min, rect_w_max, rect_color_kind, position_bias.
Degenerates: tiny_rect, all_overlap, single_rect.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "10293dae26ed"
VERSION = "1.1.0"
TASK_ID = "10293dae26ed"
SUMMARY = "Solid rectangles >=3x3 in non-cyan colors; rule fills interior with 8."

INVARIANTS = [
    "background is 0",
    ">=1 solid rectangle of color != 8 with h>=3 and w>=3",
    "rectangles don't overlap or touch each other (4-conn)",
    "rectangle colors != 8",
]

POSITION_BIASES = ("spread", "corners", "stacked", "row_aligned")
DEGENERATE_TEXTURES = ("tiny_rect", "all_overlap", "single_rect")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 9..15", "valid": "8..20"},
    "n_rects":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "rect_h_min":     {"type": "int", "default": "3", "valid": "3..6"},
    "rect_h_max":     {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "rect_w_min":     {"type": "int", "default": "3", "valid": "3..6"},
    "rect_w_max":     {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 8
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 1, h_hi + 1)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_rects = int(overrides.get("n_rects",
                                ctx.draw_int("n_rects", 2, 3)))
    n_rects = max(1, min(5, n_rects))
    rh_min = int(overrides.get("rect_h_min", 3))
    rh_max = int(overrides.get("rect_h_max",
                               ctx.draw_int("rect_h_max", 4, 6)))
    rw_min = int(overrides.get("rect_w_min", 3))
    rw_max = int(overrides.get("rect_w_max",
                               ctx.draw_int("rect_w_max", 4, 6)))
    rh_min = max(3, min(rh_min, h - 2))
    rh_max = max(rh_min, min(rh_max, h - 2))
    rw_min = max(3, min(rw_min, w - 2))
    rw_max = max(rw_min, min(rw_max, w - 2))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    g = full_grid(h, w, 0)
    palette = list(range(1, 10))
    palette = [c for c in palette if c != 8]
    rng.shuffle(palette)
    placed = 0
    for attempt in range(n_rects * 8):
        if placed >= n_rects:
            break
        rh = rng.randint(rh_min, rh_max)
        rw = rng.randint(rw_min, rw_max)
        if rh > h - 2 or rw > w - 2:
            continue
        rr, rc = _pick_position(bias, h, w, rh, rw, placed, rng)
        if rr is None:
            continue
        cells = [(rr + dr, rc + dc) for dr in range(rh) for dc in range(rw)]
        # Check no overlap, with 1-cell buffer
        ok = True
        for r, c in cells:
            if not (0 <= r < h and 0 <= c < w):
                ok = False; break
            if g[r][c] != 0:
                ok = False; break
        if ok:
            for dr in range(-1, rh + 1):
                for dc in range(-1, rw + 1):
                    rr2, rc2 = rr + dr, rc + dc
                    if 0 <= rr2 < h and 0 <= rc2 < w and g[rr2][rc2] != 0:
                        ok = False; break
                if not ok:
                    break
        if ok:
            color = palette[placed % len(palette)]
            draw_rect(g, rr, rc, rh, rw, color)
            placed += 1
    if placed == 0:
        draw_rect(g, 1, 1, 3, 3, palette[0])
    return g


def _pick_position(bias, h, w, rh, rw, idx, rng):
    if h - rh < 0 or w - rw < 0:
        return None, None
    if bias == "corners":
        corners = [(0, 0), (0, w - rw), (h - rh, 0), (h - rh, w - rw)]
        return corners[idx % 4]
    if bias == "stacked":
        rr = idx * (rh + 2) + 1
        if rr + rh > h:
            rr = rng.randint(0, h - rh)
        return rr, max(0, (w - rw) // 2)
    if bias == "row_aligned":
        rr = max(0, (h - rh) // 2)
        rc = idx * (rw + 2) + 1
        if rc + rw > w:
            rc = rng.randint(0, w - rw)
        return rr, rc
    return rng.randint(0, h - rh), rng.randint(0, w - rw)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([2, 3, 4, 5, 6, 7, 9])
    if name == "tiny_rect":
        # 2x2 — too small for the rule to fire (need >=3x3)
        draw_rect(g, 1, 1, 2, 2, color)
        return g
    if name == "all_overlap":
        # Rectangles overlap → become a single connected blob
        draw_rect(g, 1, 1, 4, 4, color)
        draw_rect(g, 2, 3, 4, 4, color)
        return g
    if name == "single_rect":
        draw_rect(g, 1, 1, 4, 4, color)
        return g
    return g
