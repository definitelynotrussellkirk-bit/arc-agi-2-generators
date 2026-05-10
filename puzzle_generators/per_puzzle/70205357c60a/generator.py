"""Generator for bb43febb.

Rule: cell of value 5 with all 4 cardinal neighbors == 5 → 2.

Combinatorial axes (8): grid_h/w, n_rects, rect_size_kind,
position_bias, palette_size, decoy_density, inter_rect_margin,
asymmetry_force.
Degenerates: no_rects, full_grid, single_2x2.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect
from puzzle_generators.helpers.shape import normalize, rect_cells
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "70205357c60a"
VERSION = "1.1.0"
TASK_ID = "70205357c60a"
SUMMARY = "Solid 5-rectangles ≥3×3; rule fills interior with 2."

INVARIANTS = [
    "background is 0",
    ">=1 solid 5-rectangle of side >=3 (so interior cells exist)",
    "rectangles don't touch (4-conn separation by margin >=1)",
    "no color 2 in input (rule writes 2 for output)",
]

RECT_SIZE_KINDS = ("small", "medium", "large", "wide", "tall")
DEGENERATE_TEXTURES = ("no_rects", "full_grid", "single_2x2")
HELPFUL_TEXTURES = RECT_SIZE_KINDS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 7..14", "valid": "5..18"},
    "grid_w":             {"type": "int", "default": "rng 8..16", "valid": "6..20"},
    "n_rects":            {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "rect_size_kind":     {"type": "str", "default": "rng helpful",
                           "valid": "|".join(RECT_SIZE_KINDS)},
    "position_bias":      {"type": "str", "default": "rng spread|center|edge",
                           "valid": "spread|center|edge"},
    "palette_size":       {"type": "int", "default": "1", "valid": "1..1"},
    "inter_rect_margin":  {"type": "int", "default": "1", "valid": "1..3"},
    "asymmetry_force":    {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "texture":            {"type": "str", "default": "alias for rect_size_kind",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 5, 8, 6, 9
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 12, 18, 14, 20
    else:
        h_lo, h_hi, w_lo, w_hi = 7, 14, 8, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_rects = int(overrides.get("n_rects",
                                ctx.draw_int("n_rects", 1, 3)))
    n_rects = max(1, min(4, n_rects))
    size_kind = (overrides.get("texture") or
                 overrides.get("rect_size_kind")
                 or ctx.draw_choice("rect_size_kind",
                                    list(RECT_SIZE_KINDS)))
    margin = int(overrides.get("inter_rect_margin", 1))
    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(n_rects * 4):
        if placed >= n_rects:
            break
        rh, rw = _rect_dims(size_kind, h, w, rng)
        cells = normalize(rect_cells(rh, rw))
        if place_no_overlap(rng, g, cells, 5, bg=0,
                            margin=margin, max_tries=40):
            placed += 1
    if placed < 1:
        rh = min(3, h - 2); rw = min(3, w - 2)
        if rh >= 3 and rw >= 3:
            draw_rect(g, 1, 1, rh, rw, 5)
    return g


def _rect_dims(kind, h, w, rng):
    max_h = max(3, h - 2)
    max_w = max(3, w - 2)
    if kind == "small":
        return 3, 3
    if kind == "medium":
        return rng.randint(3, 4), rng.randint(3, 4)
    if kind == "large":
        return rng.randint(4, min(6, max_h)), rng.randint(4, min(6, max_w))
    if kind == "wide":
        return 3, rng.randint(4, min(7, max_w))
    if kind == "tall":
        return rng.randint(4, min(7, max_h)), 3
    return rng.randint(3, max_h), rng.randint(3, max_w)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_rects":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    if name == "single_2x2":
        if h >= 3 and w >= 3:
            draw_rect(g, 1, 1, 2, 2, 5)
        return g
    return g
