"""Generator for 23581191.

Rule: for each (r,c,v), all cells in row r and col c get v. Where two
crosses overlap, cell becomes 2.

Combinatorial axes (8): grid_h/w, n_cells, palette_size, palette_kind,
position_bias, cell_layout, separation_kind, anchor_corner.
Degenerates: same_row, same_col, no_cells.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "aa0e6084d394"
VERSION = "1.1.0"
TASK_ID = "aa0e6084d394"
SUMMARY = "Isolated non-bg cells; rule paints crosses + 2s at intersections."

INVARIANTS = [
    "background is 0",
    ">=1 non-bg cell",
    "if >=2 cells: distinct rows AND distinct cols",
    "no color 2 in input (rule writes 2 for output)",
]

CELL_LAYOUTS = ("scattered", "diagonal", "anti_diag", "corners", "spread")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("same_row", "same_col", "no_cells")
HELPFUL_TEXTURES = CELL_LAYOUTS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..14", "valid": "5..18"},
    "grid_w":         {"type": "int", "default": "rng 8..16", "valid": "6..20"},
    "n_cells":        {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "= n_cells",
                       "valid": "1..7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cell_layout":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(CELL_LAYOUTS)},
    "position_bias":  {"type": "str", "default": "rng spread|center|edge",
                       "valid": "spread|center|edge"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for cell_layout",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
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
    n = int(overrides.get("n_cells", ctx.draw_int("n_cells", 1, 3)))
    n = max(1, min(min(h, w), n))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 5, 7, 8]
    elif palette_kind == "small":
        pool = [1, 3]
    else:
        pool = [1, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    palette = pool[:n]
    while len(palette) < n:
        palette.append(palette[0])
    layout = (overrides.get("texture") or overrides.get("cell_layout")
              or ctx.draw_choice("cell_layout", list(CELL_LAYOUTS)))
    rs, cs = _layout_positions(layout, h, w, n, rng)
    g = full_grid(h, w, 0)
    for i in range(n):
        g[rs[i]][cs[i]] = palette[i]
    return g


def _layout_positions(layout, h, w, n, rng):
    if layout == "diagonal":
        rs = list(range(min(n, h)))
        cs = list(range(min(n, w)))
        return rs, cs
    if layout == "anti_diag":
        rs = list(range(min(n, h)))
        cs = [w - 1 - i for i in range(min(n, w))]
        return rs, cs
    if layout == "corners":
        corners_r = [0, 0, h - 1, h - 1]
        corners_c = [0, w - 1, 0, w - 1]
        rs = corners_r[:n]
        cs = corners_c[:n]
        return rs, cs
    if layout == "spread":
        step_r = max(1, h // (n + 1))
        step_c = max(1, w // (n + 1))
        rs = [step_r * (i + 1) for i in range(n) if step_r * (i + 1) < h]
        cs = [step_c * (i + 1) for i in range(n) if step_c * (i + 1) < w]
        while len(rs) < n: rs.append(rs[-1] if rs else 0)
        while len(cs) < n: cs.append(cs[-1] if cs else 0)
        return rs, cs
    rs = rng.sample(range(h), min(n, h))
    cs = rng.sample(range(w), min(n, w))
    while len(rs) < n: rs.append(rs[-1])
    while len(cs) < n: cs.append(cs[-1])
    return rs, cs


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color1 = rng.choice([1, 3, 4, 5, 6, 7, 8, 9])
    color2 = rng.choice([c for c in [1, 3, 4, 5, 6, 7, 8, 9]
                         if c != color1])
    if name == "same_row":
        r = h // 2
        g[r][1] = color1
        g[r][w - 2] = color2
        return g
    if name == "same_col":
        c = w // 2
        g[1][c] = color1
        g[h - 2][c] = color2
        return g
    if name == "no_cells":
        return g
    return g
