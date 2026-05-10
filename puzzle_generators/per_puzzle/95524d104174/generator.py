"""Generator for 67a423a3.

Rule: full row + full col cross at one cell; rule outputs 4-frame around
the intersection.

Combinatorial axes (8): grid_h/w, palette_kind, position_bias,
anchor_corner, asymmetry_force, palette_size, color1, color2.
Degenerates: no_lines, parallel_lines, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "95524d104174"
VERSION = "1.1.0"
TASK_ID = "95524d104174"
SUMMARY = "One full vertical column + one full horizontal row crossing at interior."

INVARIANTS = [
    "exactly one full-height column of color C1",
    "exactly one full-width row of color C2",
    "C1 != C2",
    "intersection at interior position (>=1 cell from each edge)",
]

POSITION_BIASES = ("centered", "off_center", "near_corner", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_lines", "parallel_lines", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for position_bias",
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
        h_lo, h_hi = 10, 14
    else:
        h_lo, h_hi = 7, 10
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, 2, rng)
    c1, c2 = pal[0], pal[1]
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    if bias == "centered":
        line_col = w // 2
        line_row = h // 2
    elif bias == "off_center":
        line_col = max(2, w // 2 - 1)
        line_row = max(2, h // 2 - 1)
    elif bias == "near_corner":
        line_col = rng.choice([2, w - 3])
        line_row = rng.choice([2, h - 3])
    else:
        line_col = rng.randint(2, w - 3)
        line_row = rng.randint(2, h - 3)
    line_col = max(2, min(line_col, w - 3))
    line_row = max(2, min(line_row, h - 3))
    for r in range(h):
        g[r][line_col] = c1
    for c in range(w):
        g[line_row][c] = c2
    g[line_row][line_col] = c1
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 5, 6, 7, 8, 9]
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
    g = full_grid(h, w, 0)
    if name == "no_lines":
        g[3][3] = 2
        return g
    if name == "parallel_lines":
        for r in range(h):
            g[r][3] = 1
            g[r][5] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
