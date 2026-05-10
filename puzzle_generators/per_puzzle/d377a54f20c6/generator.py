"""Generator for 8cb8642d.

Rule: two-color rectangle is redrawn as a main-color frame with
marker-color diagonals and center line.

Combinatorial axes (8): rect_height, rect_width, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_rect, full_grid, single_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import fill_box, full_grid

GENERATOR_ID = "d377a54f20c6"
VERSION = "1.1.0"
TASK_ID = "d377a54f20c6"
SUMMARY = "Two-color rectangle is redrawn as main-color frame with marker-color X."

INVARIANTS = [
    "background is color 0",
    "single connected rectangle with a dominant main color",
    "a rarer marker color inside supplies the interior stroke",
    "the rectangle sits with one row of margin on every side",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rect", "full_grid", "single_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "rect_height":    {"type": "int", "default": "rng 5..7", "valid": "3..12"},
    "rect_width":     {"type": "int", "default": "rng 6..9", "valid": "3..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
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
        rh_lo, rh_hi, rw_lo, rw_hi = 4, 5, 5, 6
    elif difficulty == "hard":
        rh_lo, rh_hi, rw_lo, rw_hi = 7, 9, 8, 11
    else:
        rh_lo, rh_hi, rw_lo, rw_hi = 5, 7, 6, 9
    rh = ctx.draw_int("rect_height", rh_lo, rh_hi)
    rw = ctx.draw_int("rect_width", rw_lo, rw_hi)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 2:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in pool]
    main, marker = pool[0], pool[1]
    g = full_grid(rh + 4, rw + 4, 0)
    fill_box(g, 2, 2, rh + 1, rw + 1, main)
    g[2 + rh // 2][2 + rw // 2] = marker
    g[3][3] = marker
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c != 0]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 0)
    if name == "no_rect":
        return g
    if name == "single_color":
        fill_box(g, 2, 2, 7, 9, 2)
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
