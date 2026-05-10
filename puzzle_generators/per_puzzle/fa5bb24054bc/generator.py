"""Generator for arc_additional_puzzles_21_set17_bundle:M116 — N×N relation matrix from panel (area, holes).

Rule: split input by all-zero columns into panels, crop each to
content, compute (area, holes). Output is N×N matrix:
  (i,i) = 5 (diagonal)
  same area + same holes = 6
  same area only = 2
  same holes only = 3
  else = 0

Combinatorial axes (8): h, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_separators, single_panel, all_same_features.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "fa5bb24054bc"
VERSION = "1.1.0"
TASK_ID = "fa5bb24054bc"
SUMMARY = "3 panels separated by blank cols, each a small shape with controlled (area, holes)."

INVARIANTS = [
    "background is 0",
    "input has 3 panels separated by all-zero columns",
    "each panel contains one connected shape (single non-bg color)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separators", "single_panel", "all_same_features")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "h":              {"type": "int", "default": "rng 3..4", "valid": "3..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "three_panels_blankcol_sep",
                       "valid": "three_panels_blankcol_sep"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

# (cells, area, holes, bbox_h, bbox_w)
_SHAPE_CATALOG = [
    # 4 cells, 0 holes
    ([(0, 0), (0, 1), (1, 0), (1, 1)], 4, 0, 2, 2),
    ([(0, 0), (0, 1), (0, 2), (0, 3)], 4, 0, 1, 4),
    # 8 cells, 1 hole (3x3 ring)
    ([(0, 0), (0, 1), (0, 2),
      (1, 0),         (1, 2),
      (2, 0), (2, 1), (2, 2)], 8, 1, 3, 3),
    # 12 cells, 1 hole (4x4 ring)
    ([(0, 0), (0, 1), (0, 2), (0, 3),
      (1, 0),                 (1, 3),
      (2, 0),                 (2, 3),
      (3, 0), (3, 1), (3, 2), (3, 3)], 12, 1, 4, 4),
    # 6 cells, 0 holes (rectangle 2x3)
    ([(0, 0), (0, 1), (0, 2),
      (1, 0), (1, 1), (1, 2)], 6, 0, 2, 3),
    # 5 cells, 0 holes (plus)
    ([(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)], 5, 0, 3, 3),
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h_min = ctx.draw_int("h", 3, 3)
    elif difficulty == "hard":
        h_min = ctx.draw_int("h", 4, 5)
    else:
        h_min = ctx.draw_int("h", 3, 4)
    rng = ctx.draw_rng("layout")
    chosen = rng.sample(_SHAPE_CATALOG, 3)
    palette = list(random_palette(rng, 3))
    h = max(h_min, max(s[3] for s in chosen))
    panel_widths = [s[4] for s in chosen]
    w = sum(panel_widths) + 2 * 2  # 2 blank cols between 3 panels
    g = full_grid(h, w, 0)
    next_c = 0
    for (cells, _a, _holes, sh, sw), color in zip(chosen, palette):
        r0 = rng.randint(0, h - sh)
        paint_at(g, r0, next_c, cells, color)
        next_c += sw + 2
    return g


def _draw_from_degenerate(name, rng):
    if name == "no_separators":
        # Three panels packed without all-zero col separators — split is undefined.
        g = full_grid(3, 6, 0)
        for c in range(2): g[0][c] = 4; g[1][c] = 4
        for c in range(2): g[0][2 + c] = 5; g[1][2 + c] = 5
        for c in range(2): g[0][4 + c] = 6; g[1][4 + c] = 6
        return g
    if name == "single_panel":
        # Only one panel — N=1, output 1x1 matrix, rule is degenerate.
        g = full_grid(3, 4, 0)
        for c in range(2): g[0][c] = 4; g[1][c] = 4
        return g
    if name == "all_same_features":
        # All 3 panels share area+holes — output matrix is all 6 (no diagonal contrast).
        g = full_grid(3, 8, 0)
        for c in range(2): g[0][c] = 4; g[1][c] = 4
        for c in range(2): g[0][3 + c] = 5; g[1][3 + c] = 5
        for c in range(2): g[0][6 + c] = 6; g[1][6 + c] = 6
        return g
    return full_grid(3, 8, 0)
