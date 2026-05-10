"""Generator for 2b01abd0.

Rule: 1-line cross divider; shape in one quadrant uses 2 colors. Other
quadrants get reflected shape with 2 colors swapped.

Combinatorial axes (8): grid_h/w, sep_position, n_cells, quadrant,
palette_kind, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_cross, multiple_quadrants, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c6a422753abe"
VERSION = "1.1.0"
TASK_ID = "c6a422753abe"
SUMMARY = "Cross-divider + shape in one quadrant; rule reflects with color swap."

INVARIANTS = [
    "exactly one 1-row and one 1-col forming a cross",
    "shape in exactly one quadrant: 4-7 cells of 2 distinct non-1 colors",
    "other quadrants are empty",
]

QUADRANTS = ("nw", "ne", "sw", "se")
SEP_POSITIONS = ("center", "off_center", "near_corner")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_cross", "multiple_quadrants", "full_grid")
HELPFUL_TEXTURES = SEP_POSITIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "sep_position":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SEP_POSITIONS)},
    "n_cells":        {"type": "int", "default": "rng 4..7", "valid": "3..10"},
    "quadrant":       {"type": "str", "default": "rng",
                       "valid": "|".join(QUADRANTS)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for sep_position",
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
        h_lo, h_hi, w_lo, w_hi = 7, 9, 8, 10
        nc_lo, nc_hi = 3, 4
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 12, 16, 13, 16
        nc_lo, nc_hi = 5, 9
    else:
        h_lo, h_hi, w_lo, w_hi = 9, 12, 10, 13
        nc_lo, nc_hi = 4, 7
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    sep_pos = (overrides.get("texture") or
               overrides.get("sep_position")
               or ctx.draw_choice("sep_position", list(SEP_POSITIONS)))
    if sep_pos == "center":
        sep_row = h // 2
        sep_col = w // 2
    elif sep_pos == "off_center":
        sep_row = max(2, h // 2 + rng.randint(-1, 1))
        sep_col = max(2, w // 2 + rng.randint(-1, 1))
    else:
        sep_row = rng.randint(2, h - 3)
        sep_col = rng.randint(2, w - 3)
    sep_row = max(2, min(sep_row, h - 3))
    sep_col = max(2, min(sep_col, w - 3))
    for c in range(w):
        g[sep_row][c] = 1
    for r in range(h):
        g[r][sep_col] = 1
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, 2, rng)
    quadrant = overrides.get("quadrant",
                             ctx.draw_choice("quadrant", list(QUADRANTS)))
    is_top = quadrant in ("nw", "ne")
    is_left = quadrant in ("nw", "sw")
    if is_top:
        rrange = (1, sep_row - 1)
    else:
        rrange = (sep_row + 1, h - 2)
    if is_left:
        crange = (1, sep_col - 1)
    else:
        crange = (sep_col + 1, w - 2)
    n_cells = int(overrides.get("n_cells",
                                ctx.draw_int("n_cells", nc_lo, nc_hi)))
    n_cells = max(3, min(10, n_cells))
    placed = 0
    for _ in range(60):
        if placed >= n_cells:
            break
        if rrange[0] > rrange[1] or crange[0] > crange[1]:
            break
        r = rng.randint(rrange[0], rrange[1])
        c = rng.randint(crange[0], crange[1])
        if g[r][c] == 0:
            g[r][c] = rng.choice(palette)
            placed += 1
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [5, 7, 8]
    elif kind == "primary":
        pool = [2, 3, 4]
    else:
        pool = [2, 3, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c != 1]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_cross":
        g[3][3] = 2; g[3][4] = 3
        return g
    if name == "multiple_quadrants":
        sr, sc = 5, 5
        for c in range(w):
            g[sr][c] = 1
        for r in range(h):
            g[r][sc] = 1
        g[2][2] = 2; g[2][8] = 3; g[8][2] = 4
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
