"""Generator for puzzle ba9d41b8.

Rule: for each solid rectangle (>=3x3), keep border, replace interior
with checker pattern (every other cell becomes 0).

Combinatorial axes (8): grid_h/w, n_rects, rect_h_min, rect_h_max,
rect_w_min, rect_w_max, palette_kind, position_bias.
Degenerates: tiny_rect, single_rect, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "2bb81826c18d"
VERSION = "1.1.0"
TASK_ID = "2bb81826c18d"
SUMMARY = "Solid rects >=3x3; rule replaces interior with checker."

INVARIANTS = [
    "background is 0",
    "1-3 solid rectangles, each >=4x4",
    "rectangles have distinct non-bg colors",
    "rectangles don't touch (>=1 bg cell apart)",
]

POSITION_BIASES = ("scattered", "stacked", "row_aligned", "diagonal",
                   "corners")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("tiny_rect", "single_rect", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "grid_w":         {"type": "int", "default": "rng 10..16", "valid": "8..22"},
    "n_rects":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "rect_h_min":     {"type": "int", "default": "4", "valid": "3..6"},
    "rect_h_max":     {"type": "int", "default": "rng 5..7", "valid": "4..8"},
    "rect_w_min":     {"type": "int", "default": "4", "valid": "3..6"},
    "rect_w_max":     {"type": "int", "default": "rng 5..8", "valid": "4..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
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
    if difficulty == "easy":
        h_lo, h_hi = 8, 11
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
    else:
        h_lo, h_hi = 10, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_rects = int(overrides.get("n_rects",
                                ctx.draw_int("n_rects", 1, 2)))
    n_rects = max(1, min(3, n_rects))
    rh_min = int(overrides.get("rect_h_min", 4))
    rh_max = int(overrides.get("rect_h_max",
                               ctx.draw_int("rect_h_max", 5, 7)))
    rw_min = int(overrides.get("rect_w_min", 4))
    rw_max = int(overrides.get("rect_w_max",
                               ctx.draw_int("rect_w_max", 5, 8)))
    rh_min = max(3, min(rh_min, h - 2))
    rh_max = max(rh_min, min(rh_max, h - 2))
    rw_min = max(3, min(rw_min, w - 2))
    rw_max = max(rw_min, min(rw_max, w - 2))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    palette = _build_palette(palette_kind, n_rects, rng)
    g = full_grid(h, w, 0)
    placed = []
    for i, color in enumerate(palette):
        for _ in range(40):
            rh = rng.randint(rh_min, rh_max)
            rw = rng.randint(rw_min, rw_max)
            r0, c0 = _pick_position(bias, h, w, rh, rw, i, rng)
            if r0 is None:
                continue
            if any(abs(r0 - pr) < (rh + 2) and abs(c0 - pc) < (rw + 2)
                   for pr, pc in placed):
                continue
            draw_rect(g, r0, c0, rh, rw, color)
            placed.append((r0, c0))
            break
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _pick_position(bias, h, w, rh, rw, idx, rng):
    if h - rh - 2 < 1 or w - rw - 2 < 1:
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
    if name == "tiny_rect":
        # 2x2 — too small for the rule (needs >=3x3)
        draw_rect(g, 2, 2, 2, 2, 3)
        return g
    if name == "single_rect":
        draw_rect(g, 2, 2, 4, 4, 3)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3
        return g
    return g
