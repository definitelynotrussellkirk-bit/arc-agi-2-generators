"""Generator for ARC task e7dd8335.

Rule: a color-1 shape spans rows. Compute mid = (min_row + max_row)/2.
Cells where v==1 and r > mid become 2.

Combinatorial axes (8): grid_h/w, shape_kind, shape_col,
shape_row_range, n_decorations, decoration_pattern, decoy_density,
shape_thickness.
Degenerates: single_cell, all_one, no_ones.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "92f4d4eb0dbb"
VERSION = "1.1.0"
TASK_ID = "92f4d4eb0dbb"
SUMMARY = "Color-1 shape; rule turns cells below its row-midpoint to 2."

INVARIANTS = [
    "background is 0",
    "color-1 cells form a shape spanning >=5 rows",
    "shape has both rows above and below its row-midpoint",
    "no color-2 in input (rule only writes 2 to output)",
]

SHAPE_KINDS = ("vertical_bar", "tree", "cross", "snake", "stairs", "T_shape")
DEGENERATE_TEXTURES = ("single_cell", "all_one", "no_ones")
HELPFUL_TEXTURES = SHAPE_KINDS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 7..14", "valid": "5..18"},
    "grid_w":             {"type": "int", "default": "rng 7..14", "valid": "3..20"},
    "shape_kind":         {"type": "str", "default": "rng helpful",
                           "valid": "|".join(SHAPE_KINDS)},
    "shape_col":          {"type": "int", "default": "rng 2..w-3", "valid": "1..w-2"},
    "shape_row_range":    {"type": "str", "default": "rng small|medium|full",
                           "valid": "small|medium|full"},
    "shape_thickness":    {"type": "int", "default": "1", "valid": "1..2"},
    "n_decorations":      {"type": "int", "default": "rng 2..4", "valid": "0..6"},
    "decoy_density":      {"type": "float", "default": "0", "valid": "0..0.05"},
    "texture":            {"type": "str", "default": "alias for shape_kind",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 8
    elif difficulty == "hard":
        h_lo, h_hi = 12, 18
    else:
        h_lo, h_hi = 7, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    shape_kind = (overrides.get("texture") or overrides.get("shape_kind")
                  or ctx.draw_choice("shape_kind", list(SHAPE_KINDS)))
    col = int(overrides.get("shape_col",
                            ctx.draw_int("shape_col", 2, max(2, w - 3))))
    col = max(1, min(w - 2, col))
    row_range = overrides.get("shape_row_range",
                              ctx.draw_choice("shape_row_range",
                                              ["small", "medium", "full"]))
    if row_range == "small":
        r_top, r_bot = 1, max(6, h - 4)
    elif row_range == "full":
        r_top, r_bot = 0, h - 1
    else:
        r_top, r_bot = 1, h - 2
    r_top = max(0, r_top)
    r_bot = min(h - 1, r_bot)
    if r_bot - r_top < 4:
        r_top = 0
        r_bot = h - 1
    g = full_grid(h, w, 0)
    _draw_shape(g, shape_kind, col, r_top, r_bot, h, w, rng)
    return g


def _draw_shape(g, kind, col, r_top, r_bot, h, w, rng):
    def _safe_set(r, c, v):
        if 0 <= r < h and 0 <= c < w:
            g[r][c] = v
    if kind == "vertical_bar":
        for r in range(r_top, r_bot + 1):
            _safe_set(r, col, 1)
        for r in range(r_top + 1, r_bot, 2):
            _safe_set(r, col - 1, 1)
            _safe_set(r, col + 1, 1)
    elif kind == "tree":
        for r in range(r_top, r_bot + 1):
            _safe_set(r, col, 1)
        for r in range(r_top, r_bot + 1, 2):
            for d in range(1, 3):
                _safe_set(r, col - d, 1)
                _safe_set(r, col + d, 1)
    elif kind == "cross":
        for r in range(r_top, r_bot + 1):
            _safe_set(r, col, 1)
        mid = (r_top + r_bot) // 2
        for c in range(max(0, col - 2), min(w, col + 3)):
            _safe_set(mid, c, 1)
    elif kind == "snake":
        for r in range(r_top, r_bot + 1):
            offset = (r - r_top) % 3 - 1
            _safe_set(r, col + offset, 1)
    elif kind == "stairs":
        for i, r in enumerate(range(r_top, r_bot + 1)):
            c = col + (i % 3) - 1
            _safe_set(r, c, 1)
    elif kind == "T_shape":
        for r in range(r_top, r_bot + 1):
            _safe_set(r, col, 1)
        for c in range(max(0, col - 2), min(w, col + 3)):
            _safe_set(r_top, c, 1)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "single_cell":
        g[h // 2][w // 2] = 1
        return g
    if name == "all_one":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    if name == "no_ones":
        return g
    return g
