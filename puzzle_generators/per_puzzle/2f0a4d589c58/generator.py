"""Generator for puzzle ba97ae07.

Rule: find rows + cols whose dominant non-zero color spans most cells.
Where a dominant row and col have different colors, swap them at the
intersection.

Combinatorial axes (8): grid_h/w, color_1, color_2, line_row,
line_col, palette_kind, anchor_corner, asymmetry_force.
Degenerates: same_color, no_lines, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2f0a4d589c58"
VERSION = "1.1.0"
TASK_ID = "2f0a4d589c58"
SUMMARY = "Cross of two colored lines; rule swaps colors at intersection."

INVARIANTS = [
    "background is 0",
    "exactly 1 full-height col of c1",
    "exactly 1 full-width row of c2",
    "c1 != c2",
    "no other non-zero cells",
]

LINE_POSITIONS = ("center", "upper_left", "upper_right", "lower_left",
                  "lower_right", "spread")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("same_color", "no_lines", "full_grid")
HELPFUL_TEXTURES = LINE_POSITIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..12", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 6..12", "valid": "5..16"},
    "color_1":        {"type": "color", "default": "rng (≠0,c2)",
                       "valid": "1..9"},
    "color_2":        {"type": "color", "default": "rng (≠0,c1)",
                       "valid": "1..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "line_position":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(LINE_POSITIONS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for line_position",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 7
    elif difficulty == "hard":
        h_lo, h_hi = 12, 16
    else:
        h_lo, h_hi = 6, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, rng)
    c1 = int(overrides.get("color_1", palette[0]))
    c2 = int(overrides.get("color_2",
                           next((c for c in palette if c != c1),
                                2 if c1 != 2 else 3)))
    if c1 == c2:
        c2 = next((c for c in palette if c != c1),
                  2 if c1 != 2 else 3)
    pos = (overrides.get("texture") or
           overrides.get("line_position")
           or ctx.draw_choice("line_position", list(LINE_POSITIONS)))
    g = full_grid(h, w, 0)
    line_col, line_row = _pick_lines(pos, h, w, rng)
    for r in range(h):
        g[r][line_col] = c1
    for c in range(w):
        g[line_row][c] = c2
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(pool)
    return pool


def _pick_lines(pos, h, w, rng):
    if pos == "center":
        return w // 2, h // 2
    if pos == "upper_left":
        return rng.randint(1, w // 2), rng.randint(1, h // 2)
    if pos == "upper_right":
        return rng.randint(w // 2, w - 2), rng.randint(1, h // 2)
    if pos == "lower_left":
        return rng.randint(1, w // 2), rng.randint(h // 2, h - 2)
    if pos == "lower_right":
        return rng.randint(w // 2, w - 2), rng.randint(h // 2, h - 2)
    return rng.randint(1, w - 2), rng.randint(1, h - 2)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "same_color":
        c = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
        line_col = w // 2; line_row = h // 2
        for r in range(h):
            g[r][line_col] = c
        for cc in range(w):
            g[line_row][cc] = c
        return g
    if name == "no_lines":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3 if (r + c) % 2 == 0 else 4
        return g
    return g
