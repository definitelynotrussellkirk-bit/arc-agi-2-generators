"""Generator for 8e1813be.

Rule: gray(5) NxN square plus four single-color line segments around
its 4 sides. Output is NxN with line colors arranged in a sorted
positional pattern.

Combinatorial axes (8): grid_h/w, n, square_position, line_distance,
palette_kind, anchor_corner, asymmetry_force.
Degenerates: missing_line, two_grays, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "5b18a320e97b"
VERSION = "1.1.0"
TASK_ID = "5b18a320e97b"
SUMMARY = "Gray NxN square + 4 colored line segments around it; rule produces NxN color grid."

INVARIANTS = [
    "background is 0",
    "exactly one solid gray(5) NxN square (3<=N<=5)",
    "exactly 4 line segments, each a distinct non-gray non-bg color",
    "lines are length-N runs at fixed distance from the square's sides",
    "all 4 lines fit inside the grid",
]

POSITION_BIASES = ("centered", "off_center", "corner_lean", "wide_spread")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("missing_line", "two_grays", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "n":              {"type": "int", "default": "rng 3..5", "valid": "3..5"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "line_distance":  {"type": "str", "default": "rng",
                       "valid": "near|far|mixed"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 10, 12
        n_lo, n_hi = 3, 3
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
        n_lo, n_hi = 4, 5
    else:
        h_lo, h_hi = 12, 16
        n_lo, n_hi = 3, 5
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    n = int(overrides.get("n", ctx.draw_int("n", n_lo, n_hi)))
    n = max(3, min(5, n))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    line_distance = overrides.get("line_distance",
                                  ctx.draw_choice("line_distance",
                                                  ["near", "far", "mixed"]))
    g = full_grid(h, w, 0)
    margin = 3
    cr, cc = _pick_square_pos(bias, h, w, n, margin, rng)
    draw_rect(g, cr, cc, n, n, 5)
    palette = _build_palette(palette_kind, 4, rng)

    def pick_d(side_max):
        if line_distance == "near":
            return rng.randint(1, max(1, min(2, side_max)))
        if line_distance == "far":
            return rng.randint(max(1, side_max - 1), max(1, side_max))
        return rng.randint(1, max(1, side_max))

    d_top = pick_d(cr)
    for c in range(cc, cc + n):
        if 0 <= cr - d_top:
            g[cr - d_top][c] = palette[0]
    d_bot = pick_d(h - (cr + n))
    for c in range(cc, cc + n):
        if cr + n - 1 + d_bot < h:
            g[cr + n - 1 + d_bot][c] = palette[1]
    d_left = pick_d(cc)
    for r in range(cr, cr + n):
        if 0 <= cc - d_left:
            g[r][cc - d_left] = palette[2]
    d_right = pick_d(w - (cc + n))
    for r in range(cr, cr + n):
        if cc + n - 1 + d_right < w:
            g[r][cc + n - 1 + d_right] = palette[3]
    return g


def _pick_square_pos(bias, h, w, n, margin, rng):
    if bias == "centered":
        cr = max(margin + 1, (h - n) // 2 + rng.randint(-1, 1))
        cc = max(margin + 1, (w - n) // 2 + rng.randint(-1, 1))
    elif bias == "corner_lean":
        cr = rng.choice([margin + 1, h - n - margin])
        cc = rng.choice([margin + 1, w - n - margin])
    elif bias == "wide_spread":
        cr = rng.randint(margin + 1, h - n - margin)
        cc = rng.randint(margin + 1, w - n - margin)
    else:
        cr = rng.randint(margin + 1, h - n - margin)
        cc = rng.randint(margin + 1, w - n - margin)
    cr = max(margin + 1, min(h - n - margin, cr))
    cc = max(margin + 1, min(w - n - margin, cc))
    return cr, cc


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    pool = [c for c in pool if c != 5]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 14, 14
    g = full_grid(h, w, 0)
    if name == "missing_line":
        cr, cc, n = 6, 6, 3
        draw_rect(g, cr, cc, n, n, 5)
        for c in range(cc, cc + n):
            g[cr - 2][c] = 2
        return g
    if name == "two_grays":
        draw_rect(g, 3, 3, 3, 3, 5)
        draw_rect(g, 9, 9, 3, 3, 5)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
