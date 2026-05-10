"""Generator for arc_additional_puzzle_bank_volume7:E46 — Fill 0 between two 6s horizontally with 6.

Rule: cell (r,c)=0 with g[r][c-1]=6 and g[r][c+1]=6 → becomes 6.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_lines,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_gaps, all_solid_lines, vertical_lines.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "26872d42d87a"
VERSION = "1.1.0"
TASK_ID = "26872d42d87a"
SUMMARY = "2-3 horizontal lines of 6s with single-cell gaps."

INVARIANTS = [
    "≥2 rows have a (6, 0, 6) pattern (sometimes longer with multiple gaps)",
    "1 corner-decoration of color 5",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_gaps", "all_solid_lines", "vertical_lines")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_lines":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "row_lines_with_gaps",
                       "valid": "row_lines_with_gaps"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "1..3"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        n_lines = ctx.draw_int("n_lines", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
        n_lines = ctx.draw_int("n_lines", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
        n_lines = ctx.draw_int("n_lines", 2, 3)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used_rows = set()
    for _ in range(n_lines):
        for _ in range(20):
            r = rng.randint(0, h - 1)
            if r in used_rows:
                continue
            length = rng.choice([3, 5, 7])
            if length > w - 2:
                continue
            c = rng.randint(0, w - length)
            for i in range(0, length, 2):
                g[r][c + i] = 6
            used_rows.add(r)
            break
    g[0][0] = 5
    g[h - 1][w - 1] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_gaps":
        # only isolated 6s, never (6,?,6) → rule fires zero times
        g[2][2] = 6; g[4][6] = 6; g[6][1] = 6
        g[0][0] = 5; g[h - 1][w - 1] = 5
        return g
    if name == "all_solid_lines":
        # solid 6-runs (no zero in the middle) → predicate fails: middle isn't 0
        for c in range(2, 6): g[2][c] = 6
        for c in range(3, 7): g[5][c] = 6
        g[0][0] = 5; g[h - 1][w - 1] = 5
        return g
    if name == "vertical_lines":
        # 6-0-6 vertical (above-below, not left-right) → rule only checks horizontal
        g[1][3] = 6; g[3][3] = 6
        g[2][7] = 6; g[4][7] = 6
        g[0][0] = 5; g[h - 1][w - 1] = 5
        return g
    return g
