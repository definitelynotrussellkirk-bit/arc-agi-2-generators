"""Generator for puzzle 310f3251.

Rule: first build tile = cellmap that replaces each 0 cell with 2 if
(r+1 mod h, c+1 mod w) is non-zero. Then output is 3h × 3w of tile.

Combinatorial axes (8): grid_h/w, fg_color, n_markers, marker_layout,
fg_density, marker_position_bias, single_or_multi_color, decoy_density.
Degenerates: all_zero, all_filled, single_marker.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "04b981f78957"
VERSION = "1.1.0"
TASK_ID = "04b981f78957"
SUMMARY = "Small marker grid; rule applies diag-shadow then 3 × 3 tile."

INVARIANTS = [
    "h, w in 3..7 (so 3× output ≤ 21)",
    "≥1 non-zero marker cell (rule's diag-shadow needs anchors)",
]

MARKER_LAYOUTS = ("random", "cluster", "diagonal", "scattered", "blob",
                  "row", "column", "corners")
DEGENERATE_TEXTURES = ("all_zero", "all_filled", "single_marker")
HELPFUL_TEXTURES = MARKER_LAYOUTS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 3..7", "valid": "3..10"},
    "grid_w":             {"type": "int", "default": "rng 3..7", "valid": "3..10"},
    "fg_color":           {"type": "color", "default": "rng (≠0,2)", "valid": "1..9 (≠2)"},
    "n_markers":          {"type": "int", "default": "rng 2..6", "valid": "1..15"},
    "marker_layout":      {"type": "str", "default": "rng helpful",
                           "valid": "|".join(MARKER_LAYOUTS)},
    "marker_position_bias": {"type": "str", "default": "rng top|bottom|center|spread",
                             "valid": "top|bottom|center|spread"},
    "single_or_multi_color": {"type": "str", "default": "rng helpful",
                              "valid": "single|multi"},
    "fg_density":         {"type": "float", "default": "rng 0.2..0.5", "valid": "0..1"},
    "texture":            {"type": "str", "default": "alias for marker_layout",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 3, 4
    elif difficulty == "hard":
        h_lo, h_hi = 6, 7
    else:
        h_lo, h_hi = 3, 7
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    fg = int(overrides.get("fg_color", ctx.draw_color("fg_color", exclude={0, 2})))
    n_markers = int(overrides.get("n_markers",
                                  ctx.draw_int("n_markers", 2, max(2, h * w // 3))))
    layout = (overrides.get("texture") or overrides.get("marker_layout")
              or ctx.draw_choice("marker_layout", list(MARKER_LAYOUTS)))
    bias = overrides.get("marker_position_bias",
                         ctx.draw_choice("marker_position_bias",
                                         ["top", "bottom", "center", "spread"]))
    multi = overrides.get("single_or_multi_color",
                          ctx.draw_choice("single_or_multi_color",
                                          ["single", "multi"]))
    palette = [fg]
    if multi == "multi":
        extras = list(ctx.draw_distinct_colors("extras", n=2, exclude={0, 2, fg}))
        palette = [fg] + extras
    g = full_grid(h, w, 0)
    candidates = _candidates_for_bias(bias, h, w)
    cells = _layout_cells(layout, candidates, n_markers, rng)
    for i, (r, c) in enumerate(cells):
        g[r][c] = palette[i % len(palette)]
    if not any(g[r][c] != 0 for r in range(h) for c in range(w)):
        g[0][0] = fg
    return g


def _candidates_for_bias(bias, h, w):
    if bias == "top":
        return [(r, c) for r in range(0, max(1, h // 2)) for c in range(w)]
    if bias == "bottom":
        return [(r, c) for r in range(max(0, h // 2), h) for c in range(w)]
    if bias == "center":
        return [(r, c) for r in range(h // 4, max(h // 4 + 1, 3 * h // 4))
                for c in range(w // 4, max(w // 4 + 1, 3 * w // 4))]
    return [(r, c) for r in range(h) for c in range(w)]


def _layout_cells(layout, candidates, n, rng):
    if not candidates: return []
    n = min(n, len(candidates))
    if layout == "cluster":
        cr, cc = rng.choice(candidates)
        candidates = sorted(candidates, key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return candidates[:n]
    if layout == "diagonal":
        cset = set(candidates)
        return [(k, k) for k in range(20) if (k, k) in cset][:n]
    if layout == "scattered":
        scat = [(r, c) for (r, c) in candidates if (r + c) % 2 == 0]
        rng.shuffle(scat)
        return scat[:n]
    if layout == "blob":
        cr, cc = rng.choice(candidates)
        candidates = sorted(candidates, key=lambda rc: max(abs(rc[0] - cr), abs(rc[1] - cc)))
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
        cells = [(r, c) for (r, cc) in candidates if cc == c]
        rng.shuffle(cells)
        return cells[:n]
    if layout == "corners":
        h = max(r for r, _ in candidates) + 1
        w = max(c for _, c in candidates) + 1
        return [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)][:n]
    rng.shuffle(candidates)
    return candidates[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    fg = rng.choice([1, 3, 4, 5, 6, 7, 8, 9])
    if name == "all_zero":
        g[0][0] = fg
        return g
    if name == "all_filled":
        for r in range(h):
            for c in range(w):
                g[r][c] = fg
        return g
    if name == "single_marker":
        g[h // 2][w // 2] = fg
        return g
    return g
