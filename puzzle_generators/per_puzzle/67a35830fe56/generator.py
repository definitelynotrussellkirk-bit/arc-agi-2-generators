"""Generator for puzzle 25ff71a9.

Rule: shift the input down by one row (top row becomes 0).

Combinatorial axes: grid_h/w, fg_color, fg_density, fg_layout, row_bias.
Degenerates: only_bottom_row (rule erases all), only_top_row, all_bg.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "67a35830fe56"
VERSION = "1.1.0"
TASK_ID = "67a35830fe56"
SUMMARY = "Sparse non-bg cells; rule shifts each down by one row."

INVARIANTS = [
    "bg = 0",
    "≥1 non-bg cell with at least one not in the bottom row",
]

FG_LAYOUTS = ("random", "cluster", "row", "column", "diagonal", "scattered", "blob")
ROW_BIASES = ("top", "bottom", "mid", "spread")
DEGENERATE_TEXTURES = ("only_bottom_row", "only_top_row", "all_bg")
HELPFUL_TEXTURES = FG_LAYOUTS

AXES = {
    "grid_h":     {"type": "int", "default": "rng 3..18", "valid": "3..25"},
    "grid_w":     {"type": "int", "default": "rng 3..18", "valid": "3..25"},
    "fg_color":   {"type": "color", "default": "rng (≠0)", "valid": "1..9"},
    "fg_density": {"type": "float", "default": "rng 0.1..0.4", "valid": "0..0.7"},
    "fg_layout":  {"type": "str", "default": "rng helpful",
                   "valid": "|".join(FG_LAYOUTS)},
    "row_bias":   {"type": "str", "default": "rng top|bottom|mid|spread",
                   "valid": "|".join(ROW_BIASES)},
    "texture":    {"type": "str", "default": "alias for fg_layout",
                   "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 3, 7
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 3, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    fg = int(overrides.get("fg_color", ctx.draw_color("fg_color", exclude={0})))
    density = float(overrides.get("fg_density",
                                  ctx.draw_rng("fg_density").uniform(0.1, 0.4)))
    layout = (overrides.get("texture")
              or overrides.get("fg_layout")
              or ctx.draw_choice("fg_layout", list(FG_LAYOUTS)))
    row_bias = overrides.get("row_bias",
                             ctx.draw_choice("row_bias", list(ROW_BIASES)))
    g = full_grid(h, w, 0)
    candidates = _candidates_for_bias(row_bias, h, w)
    cells = _layout_cells(layout, candidates, density, rng)
    for r, c in cells:
        if 0 <= r < h - 1 and 0 <= c < w:
            g[r][c] = fg
    if not any(g[r][c] != 0 for r in range(h - 1) for c in range(w)):
        g[0][0] = fg
    return g


def _candidates_for_bias(bias, h, w):
    if bias == "top":
        return [(r, c) for r in range(0, max(1, h // 2)) for c in range(w)]
    if bias == "bottom":
        return [(r, c) for r in range(max(0, h // 2), h - 1) for c in range(w)]
    if bias == "mid":
        m = h // 2
        return [(r, c) for r in range(max(0, m - 1), min(h - 1, m + 2)) for c in range(w)]
    return [(r, c) for r in range(h - 1) for c in range(w)]


def _layout_cells(layout, candidates, density, rng):
    if not candidates:
        return []
    n = max(1, int(len(candidates) * density))
    if layout == "cluster":
        cr, cc = rng.choice(candidates)
        candidates = sorted(candidates, key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return candidates[:n]
    if layout == "row":
        rs = sorted({r for r, _ in candidates})
        if not rs: return []
        r = rng.choice(rs)
        cells = [(r, c) for (rr, c) in candidates if rr == r]
        rng.shuffle(cells)
        return cells[:n]
    if layout == "column":
        cs = sorted({c for _, c in candidates})
        if not cs: return []
        c = rng.choice(cs)
        cells = [(r, cc) for (r, cc) in candidates if cc == c]
        rng.shuffle(cells)
        return cells[:n]
    if layout == "diagonal":
        cand_set = set(candidates)
        diag = [(k, k) for k in range(25) if (k, k) in cand_set]
        return diag[:n]
    if layout == "scattered":
        scat = [(r, c) for (r, c) in candidates if (r + c) % 2 == 0]
        rng.shuffle(scat)
        return scat[:n]
    if layout == "blob":
        cr, cc = rng.choice(candidates)
        candidates = sorted(candidates, key=lambda rc: max(abs(rc[0] - cr), abs(rc[1] - cc)))
        return candidates[:n]
    rng.shuffle(candidates)
    return candidates[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    fg = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "only_bottom_row":
        for c in range(w):
            if rng.random() < 0.5:
                g[h - 1][c] = fg
        g[h - 1][0] = fg
        return g
    if name == "only_top_row":
        for c in range(w):
            if rng.random() < 0.5:
                g[0][c] = fg
        g[0][0] = fg
        return g
    if name == "all_bg":
        return g
    return g
