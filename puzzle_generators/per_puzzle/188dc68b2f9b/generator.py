"""Generator for 2dc579da.

Rule: cross-divider splits into 4 quadrants; one has singleton cell;
output that quadrant.

Combinatorial axes (8): grid_h/w, palette_kind, position_bias,
quadrant, anchor_corner, asymmetry_force, palette_size, sep_position.
Degenerates: no_singleton, no_separator, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "188dc68b2f9b"
VERSION = "1.1.0"
TASK_ID = "188dc68b2f9b"
SUMMARY = "Cross-divider on dom-bg; singleton cell in one quadrant."

INVARIANTS = [
    "exactly one full sep-row and one full sep-col of sep_color",
    "rest filled with dom_color (!=sep_color)",
    "exactly one cell of a 3rd singleton color in one quadrant",
]

QUADRANTS = ("nw", "ne", "sw", "se")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_singleton", "no_separator", "full_grid")
HELPFUL_TEXTURES = QUADRANTS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "quadrant":       {"type": "str", "default": "rng helpful",
                       "valid": "|".join(QUADRANTS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "sep_position":   {"type": "str", "default": "centered",
                       "valid": "centered|rng"},
    "texture":        {"type": "str", "default": "alias for quadrant",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 5, 7
    elif difficulty == "hard":
        h_lo, h_hi = 9, 12
    else:
        h_lo, h_hi = 7, 9
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, 3, rng)
    dom_color, sep_color, singleton_color = pal[0], pal[1], pal[2]
    g = [[dom_color] * w for _ in range(h)]
    sep_pos = overrides.get("sep_position",
                            ctx.draw_choice("sep_position",
                                            ["centered", "rng"]))
    if sep_pos == "centered":
        sep_row = h // 2
        sep_col = w // 2
    else:
        sep_row = rng.randint(2, h - 3)
        sep_col = rng.randint(2, w - 3)
    for c in range(w):
        g[sep_row][c] = sep_color
    for r in range(h):
        g[r][sep_col] = sep_color
    quad = (overrides.get("texture") if overrides.get("texture") in QUADRANTS else None) or \
           overrides.get("quadrant") or \
           ctx.draw_choice("quadrant", list(QUADRANTS))
    is_top = quad in ("nw", "ne")
    is_left = quad in ("nw", "sw")
    r_lo = 0 if is_top else sep_row + 1
    r_hi = sep_row - 1 if is_top else h - 1
    c_lo = 0 if is_left else sep_col + 1
    c_hi = sep_col - 1 if is_left else w - 1
    if r_hi < r_lo or c_hi < c_lo:
        return g
    sr = rng.randint(r_lo, r_hi)
    sc = rng.randint(c_lo, c_hi)
    g[sr][sc] = singleton_color
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
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = [[1] * w for _ in range(h)]
    if name == "no_singleton":
        for c in range(w):
            g[4][c] = 2
        for r in range(h):
            g[r][4] = 2
        return g
    if name == "no_separator":
        g[3][3] = 4
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 4
        return g
    return g
