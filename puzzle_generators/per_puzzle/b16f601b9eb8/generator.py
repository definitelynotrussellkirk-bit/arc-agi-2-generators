"""Generator for puzzle 20818e16.

Rule: bg = (0,0)'s color. Find non-bg colors. Output: largest bbox is
canvas, smaller stacked at top-left.

Combinatorial axes (8): grid_h/w, n_rects, rect_h_min, rect_h_max,
rect_w_min, rect_w_max, palette_kind, position_bias.
Degenerates: tied_areas, single_rect, no_rects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect

GENERATOR_ID = "b16f601b9eb8"
VERSION = "1.1.0"
TASK_ID = "b16f601b9eb8"
SUMMARY = "bg=8 + solid rects of distinct sizes; rule stacks them at TL."

INVARIANTS = [
    "bg = 8",
    "2-4 solid rects of distinct non-bg colors",
    "areas are strictly distinct (sort unambiguous)",
    "rects don't overlap",
]

POSITION_BIASES = ("scattered", "stacked", "row_aligned", "diagonal")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("tied_areas", "single_rect", "no_rects")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "grid_w":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "n_rects":        {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "rect_h_min":     {"type": "int", "default": "2", "valid": "2..5"},
    "rect_h_max":     {"type": "int", "default": "rng 5..7", "valid": "3..9"},
    "rect_w_min":     {"type": "int", "default": "2", "valid": "2..5"},
    "rect_w_max":     {"type": "int", "default": "rng 5..7", "valid": "3..9"},
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
        h_lo, h_hi = 10, 13
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
    else:
        h_lo, h_hi = 12, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_rects = int(overrides.get("n_rects",
                                ctx.draw_int("n_rects", 2, 3)))
    n_rects = max(2, min(4, n_rects))
    rh_min = int(overrides.get("rect_h_min", 2))
    rh_max = int(overrides.get("rect_h_max",
                               ctx.draw_int("rect_h_max", 5, 7)))
    rw_min = int(overrides.get("rect_w_min", 2))
    rw_max = int(overrides.get("rect_w_max",
                               ctx.draw_int("rect_w_max", 5, 7)))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    palette = _build_palette(palette_kind, n_rects, rng)
    g = [[8] * w for _ in range(h)]
    sizes = []
    used_areas = set()
    while len(sizes) < n_rects:
        rh = rng.randint(rh_min, rh_max); rw = rng.randint(rw_min, rw_max)
        area = rh * rw
        if area in used_areas:
            continue
        sizes.append((rh, rw))
        used_areas.add(area)
    placed = []
    for idx, (color, (rh, rw)) in enumerate(zip(palette, sizes)):
        for _ in range(60):
            r0, c0 = _pick_position(bias, h, w, rh, rw, idx, rng)
            if r0 is None:
                continue
            if any(abs(r0 - pr) < (rh + 1) and abs(c0 - pc) < (rw + 1)
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
        pool = [1, 5, 7]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _pick_position(bias, h, w, rh, rw, idx, rng):
    if h - rh < 0 or w - rw < 0:
        return None, None
    if bias == "stacked":
        rr = idx * (rh + 2)
        if rr + rh > h:
            rr = rng.randint(0, h - rh)
        return rr, max(0, (w - rw) // 2)
    if bias == "row_aligned":
        rr = max(0, (h - rh) // 2)
        rc = idx * (rw + 2)
        if rc + rw > w:
            rc = rng.randint(0, w - rw)
        return rr, rc
    if bias == "diagonal":
        rr = idx * 4
        rc = idx * 4
        if rr + rh > h or rc + rw > w:
            return rng.randint(0, h - rh), rng.randint(0, w - rw)
        return rr, rc
    return rng.randint(0, h - rh), rng.randint(0, w - rw)


def _draw_from_degenerate(name, h, w, rng):
    g = [[8] * w for _ in range(h)]
    if name == "tied_areas":
        # 2 rects same area but different shapes
        draw_rect(g, 1, 1, 3, 4, 3)
        draw_rect(g, h - 5, w - 5, 4, 3, 4)
        return g
    if name == "single_rect":
        draw_rect(g, 2, 2, 4, 4, 3)
        return g
    if name == "no_rects":
        return g
    return g
