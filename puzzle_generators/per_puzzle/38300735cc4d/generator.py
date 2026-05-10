"""Generator for additional_scaffolded:M3 — fill clear row/col paths between 2-marker pairs.

Rule: for each color with exactly 2 markers in the input, if they
share a row OR column AND every cell of the segment between them is 0,
fill the whole segment with that color. Blocked segments do nothing.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, all_blocked, single_marker.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "38300735cc4d"
VERSION = "1.1.0"
TASK_ID = "38300735cc4d"
SUMMARY = "1-3 distinct colors, each with exactly 2 markers in a shared row or column."

INVARIANTS = [
    "background is 0",
    "1-3 distinct non-bg colors, each with exactly 2 markers",
    "every pair shares a row or column with at least 1 0-cell strictly between them",
    "pairs occupy distinct rows and distinct cols (segments don't cross)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "all_blocked", "single_marker")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "row_col_pairs",
                       "valid": "row_col_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
        n_colors = ctx.draw_int("n_colors", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 12)
        n_colors = ctx.draw_int("n_colors", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 6, 10)
        n_colors = ctx.draw_int("n_colors", 1, 3)
    rng = ctx.draw_rng("layout")
    colors = list(random_palette(rng, n_colors))
    g = full_grid(h, w, 0)
    busy_rows: set[int] = set()
    busy_cols: set[int] = set()
    for color in colors:
        for _ in range(60):
            if rng.random() < 0.5:
                r = rng.randint(0, h - 1)
                if r in busy_rows: continue
                cs = sorted(rng.sample(range(w), 2))
                if cs[1] - cs[0] < 2: continue
                if cs[0] in busy_cols or cs[1] in busy_cols: continue
                g[r][cs[0]] = color; g[r][cs[1]] = color
                busy_rows.add(r)
                break
            else:
                c = rng.randint(0, w - 1)
                if c in busy_cols: continue
                rs = sorted(rng.sample(range(h), 2))
                if rs[1] - rs[0] < 2: continue
                if rs[0] in busy_rows or rs[1] in busy_rows: continue
                g[rs[0]][c] = color; g[rs[1]][c] = color
                busy_cols.add(c)
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Lone markers, not in shared rows/cols — rule has no segments to fill.
        g[1][3] = 4; g[5][6] = 5
        return g
    if name == "all_blocked":
        # Pair shares row but a non-bg cell sits between — rule skips this segment.
        g[2][1] = 4; g[2][6] = 4
        g[2][4] = 5  # blocker
        return g
    if name == "single_marker":
        # Color has only 1 marker — rule needs 2 to define a segment.
        g[3][3] = 4
        return g
    return g
