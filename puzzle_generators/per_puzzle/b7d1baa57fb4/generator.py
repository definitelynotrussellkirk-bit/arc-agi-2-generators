"""Generator for puzzle 65daed9b.

Rule: find the column containing 8-cells (mirror axis). For 0-cells:
if mirror cell is non-zero, copy it. Axis col becomes all 8.

Combinatorial axes (8): grid_h/w, axis_col, n_marks, side, n_cells,
palette_kind, anchor_corner, asymmetry_force.
Degenerates: no_axis, no_cells, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b7d1baa57fb4"
VERSION = "1.1.0"
TASK_ID = "b7d1baa57fb4"
SUMMARY = "Grid w/ 8-axis column; rule mirrors non-zero cells across it."

INVARIANTS = [
    "background is 0",
    ">=1 cell of color 8 on the axis column",
    "no other 8-cells outside axis",
    ">=1 non-zero cell whose mirror is 0",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
SIDES = ("left", "right", "rng")
DEGENERATE_TEXTURES = ("no_axis", "no_cells", "full_grid")
HELPFUL_TEXTURES = SIDES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "axis_col":       {"type": "int", "default": "rng 3..w-4",
                       "valid": "1..w-2"},
    "n_marks":        {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "side":           {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SIDES)},
    "n_cells":        {"type": "int", "default": "rng 5..10", "valid": "1..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for side",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 9
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 2, h_hi + 4)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    axis_col = int(overrides.get("axis_col",
                                 rng.randint(3, max(3, w - 4))))
    axis_col = max(1, min(w - 2, axis_col))
    n_marks = int(overrides.get("n_marks",
                                ctx.draw_int("n_marks", 1, 3)))
    n_marks = max(1, min(5, min(h, n_marks)))
    side = (overrides.get("texture") or
            overrides.get("side")
            or ctx.draw_choice("side", list(SIDES)))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, rng)
    n_cells = int(overrides.get("n_cells",
                                ctx.draw_int("n_cells", 5, 10)))
    g = full_grid(h, w, 0)
    mark_rows = rng.sample(range(h), n_marks)
    for r in mark_rows:
        g[r][axis_col] = 8
    if side == "left":
        side_dir = -1
    elif side == "right":
        side_dir = 1
    else:
        side_dir = rng.choice([-1, 1])
    for _ in range(n_cells):
        r = rng.randint(0, h - 1)
        if side_dir == -1:
            c = rng.randint(0, max(0, axis_col - 1))
        else:
            c = rng.randint(min(axis_col + 1, w - 1), w - 1)
        if c == axis_col:
            continue
        if g[r][c] == 0:
            g[r][c] = rng.choice(palette)
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 9]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_axis":
        for r in range(2, 5):
            g[r][2] = rng.choice([1, 2, 3, 4])
        return g
    if name == "no_cells":
        axis_col = w // 2
        for r in range(h // 2):
            g[r][axis_col] = 8
        return g
    if name == "full_grid":
        axis_col = w // 2
        for r in range(h):
            for c in range(w):
                if c == axis_col:
                    g[r][c] = 8
                else:
                    g[r][c] = rng.choice([1, 2, 3, 4])
        return g
    return g
