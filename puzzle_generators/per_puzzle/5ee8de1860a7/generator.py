"""Generator for ARC task fc754716.

Rule: find first non-zero color; output is h × w with border = color,
interior = 0.

Combinatorial axes: grid_h/w, fg_color, marker_count, marker_layout.
Degenerates: no_markers (no fg → invalid), all_markers, single_marker.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5ee8de1860a7"
VERSION = "1.1.0"
TASK_ID = "5ee8de1860a7"
SUMMARY = "Mostly blank grid with one fg color; rule draws a full border in that color."

INVARIANTS = [
    "background is 0",
    "exactly one fg color appears",
    "≥1 marker so the rule has a color to read",
]

MARKER_LAYOUTS = ("scattered", "cluster", "row", "column", "diagonal", "blob")
DEGENERATE_TEXTURES = ("single_marker", "many_markers", "interior_full")
HELPFUL_TEXTURES = MARKER_LAYOUTS

AXES = {
    "grid_h":          {"type": "int", "default": "rng 3..14", "valid": "3..18"},
    "grid_w":          {"type": "int", "default": "rng 3..14", "valid": "3..18"},
    "fg_color":        {"type": "color", "default": "rng (≠0)", "valid": "1..9"},
    "marker_count":    {"type": "int", "default": "rng 1..5", "valid": "1..h*w/4"},
    "marker_layout":   {"type": "str", "default": "rng helpful",
                        "valid": "|".join(MARKER_LAYOUTS)},
    "texture":         {"type": "str", "default": "alias for marker_layout",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 3, 5
    elif difficulty == "hard":
        h_lo, h_hi = 11, 14
    else:
        h_lo, h_hi = 3, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("markers")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    fg = int(overrides.get("fg_color", ctx.draw_color("fg_color", exclude={0})))
    n_markers = int(overrides.get("marker_count",
                                  ctx.draw_int("marker_count", 1,
                                               max(1, (h - 2) * (w - 2)))))
    layout = (overrides.get("texture") or overrides.get("marker_layout")
              or ctx.draw_choice("marker_layout", list(MARKER_LAYOUTS)))
    g = full_grid(h, w, 0)
    interior = [(r, c) for r in range(1, h - 1) for c in range(1, w - 1)] or [(0, 0)]
    cells = _layout_cells(layout, interior, n_markers, rng)
    for r, c in cells:
        g[r][c] = fg
    if not any(g[r][c] != 0 for r in range(h) for c in range(w)):
        g[0][0] = fg
    return g


def _layout_cells(layout, interior, n, rng):
    n = min(n, len(interior))
    if layout == "cluster":
        cr, cc = rng.choice(interior)
        cells = sorted(interior, key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return cells[:n]
    if layout == "row":
        rs = sorted({r for r, _ in interior})
        if not rs: return interior[:n]
        r = rng.choice(rs)
        cells = [(r, c) for (rr, c) in interior if rr == r]
        rng.shuffle(cells)
        return cells[:n]
    if layout == "column":
        cs = sorted({c for _, c in interior})
        if not cs: return interior[:n]
        c = rng.choice(cs)
        cells = [(r, c) for (r, cc) in interior if cc == c]
        rng.shuffle(cells)
        return cells[:n]
    if layout == "diagonal":
        cand = set(interior)
        return [(k, k) for k in range(20) if (k, k) in cand][:n]
    if layout == "blob":
        cr, cc = rng.choice(interior)
        cells = sorted(interior, key=lambda rc: max(abs(rc[0] - cr), abs(rc[1] - cc)))
        return cells[:n]
    cells = list(interior)
    rng.shuffle(cells)
    return cells[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    fg = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "single_marker":
        g[h // 2][w // 2] = fg
        return g
    if name == "many_markers":
        for r in range(1, h - 1):
            for c in range(1, w - 1):
                if rng.random() < 0.5:
                    g[r][c] = fg
        return g
    if name == "interior_full":
        for r in range(1, h - 1):
            for c in range(1, w - 1):
                g[r][c] = fg
        return g
    return g
