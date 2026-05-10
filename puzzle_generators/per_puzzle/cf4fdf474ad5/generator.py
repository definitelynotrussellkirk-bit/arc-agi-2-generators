"""Generator for puzzle 2c0b0aff.

Rule: 2-3 8-rectangles with 3-cells overlaid; rule outputs the rect
with the most 3-cells (tie: smaller bbox, then top-left).

Combinatorial axes (8): grid_h/w, n_rects, rect_h_min, rect_h_max,
rect_w_min, rect_w_max, n_3_min, n_3_max.
Degenerates: tied_3_count, single_rect, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "cf4fdf474ad5"
VERSION = "1.1.0"
TASK_ID = "cf4fdf474ad5"
SUMMARY = "8-rects with 3-cells; rule outputs rect with most 3s."

INVARIANTS = [
    "background is 0",
    "2-4 solid 8-rectangles, each with 3-cells overlaid",
    "exactly one rect has the strict-largest 3-count",
    "rectangles don't touch (>=1 bg cell apart)",
    "all rects have h <= 8",
]

POSITION_BIASES = ("scattered", "stacked", "row_aligned", "diagonal",
                   "corners")
DEGENERATE_TEXTURES = ("tied_3_count", "single_rect", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 16..22", "valid": "12..28"},
    "grid_w":         {"type": "int", "default": "rng 16..22", "valid": "12..28"},
    "n_rects":        {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "rect_h_min":     {"type": "int", "default": "5", "valid": "4..8"},
    "rect_h_max":     {"type": "int", "default": "rng 7..8", "valid": "5..8"},
    "rect_w_min":     {"type": "int", "default": "5", "valid": "4..8"},
    "rect_w_max":     {"type": "int", "default": "rng 7..8", "valid": "5..8"},
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
        h_lo, h_hi = 12, 16
    elif difficulty == "hard":
        h_lo, h_hi = 22, 28
    else:
        h_lo, h_hi = 16, 22
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_rects = int(overrides.get("n_rects",
                                ctx.draw_int("n_rects", 2, 3)))
    n_rects = max(2, min(4, n_rects))
    rh_min = int(overrides.get("rect_h_min", 5))
    rh_max = int(overrides.get("rect_h_max",
                               ctx.draw_int("rect_h_max", 7, 8)))
    rw_min = int(overrides.get("rect_w_min", 5))
    rw_max = int(overrides.get("rect_w_max",
                               ctx.draw_int("rect_w_max", 7, 8)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    g = full_grid(h, w, 0)
    counts = rng.sample(range(2, 9), n_rects)
    placed = []
    for n3 in counts:
        for _ in range(40):
            rh = rng.randint(rh_min, rh_max)
            rw = rng.randint(rw_min, rw_max)
            if rh > h - 2 or rw > w - 2:
                continue
            r0, c0 = _pick_position(bias, h, w, rh, rw, len(placed), rng)
            if r0 is None:
                continue
            if any(abs(r0 - pr) < (rh + 2) and abs(c0 - pc) < (rw + 2)
                   for pr, pc in placed):
                continue
            draw_rect(g, r0, c0, rh, rw, 8)
            cells = [(r, c) for r in range(r0, r0 + rh)
                     for c in range(c0, c0 + rw)]
            rng.shuffle(cells)
            for cell in cells[:n3]:
                g[cell[0]][cell[1]] = 3
            placed.append((r0, c0))
            break
    return g


def _pick_position(bias, h, w, rh, rw, idx, rng):
    if h - rh < 2 or w - rw < 2:
        return None, None
    if bias == "stacked":
        rr = 1 + idx * (rh + 2)
        if rr + rh > h - 1:
            rr = rng.randint(1, h - rh - 1)
        return rr, max(1, (w - rw) // 2)
    if bias == "row_aligned":
        rr = max(1, (h - rh) // 2)
        rc = 1 + idx * (rw + 2)
        if rc + rw > w - 1:
            rc = rng.randint(1, w - rw - 1)
        return rr, rc
    if bias == "diagonal":
        rr = 1 + idx * 4
        rc = 1 + idx * 4
        if rr + rh > h - 1 or rc + rw > w - 1:
            return rng.randint(1, h - rh - 1), rng.randint(1, w - rw - 1)
        return rr, rc
    if bias == "corners":
        corners = [(1, 1), (1, w - rw - 1), (h - rh - 1, 1),
                   (h - rh - 1, w - rw - 1)]
        return corners[idx % 4]
    return rng.randint(1, h - rh - 1), rng.randint(1, w - rw - 1)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "tied_3_count":
        # Two rects with same 3-count → ambiguous output
        for r0, c0 in [(2, 2), (h - 7, w - 8)]:
            if r0 + 5 > h or c0 + 6 > w: continue
            draw_rect(g, r0, c0, 5, 6, 8)
            for _ in range(3):
                g[r0 + rng.randint(0, 4)][c0 + rng.randint(0, 5)] = 3
        return g
    if name == "single_rect":
        draw_rect(g, 2, 2, 6, 6, 8)
        for _ in range(3):
            g[2 + rng.randint(0, 5)][2 + rng.randint(0, 5)] = 3
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 8 if (r + c) % 2 == 0 else 3
        return g
    return g
