"""Generator for arc_additional_puzzle_bank_volume20:E134 — Mark middle of horizontal 1-line of odd length ≥3.

Rule: each 1-blob that is a single row of size ≥3 and odd → set
middle cell to 2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_lines,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: only_even_lengths, only_vertical, no_lines.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5bcc776c32fb"
VERSION = "1.1.0"
TASK_ID = "5bcc776c32fb"
SUMMARY = "2 horizontal 1-lines of odd length (3 or 5) + decoration."

INVARIANTS = [
    "≥2 horizontal 1-lines of odd length ≥3",
    "1 horizontal 1-line of even length (won't qualify)",
    "1 vertical 1-line",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("only_even_lengths", "only_vertical", "no_lines")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_lines":        {"type": "int", "default": "2", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "row_lines_with_distractors",
                       "valid": "row_lines_with_distractors"},
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
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 10, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used_rows = set()
    for _ in range(2):
        for _ in range(20):
            r = rng.randint(0, h - 1)
            length = rng.choice([3, 5])
            if r in used_rows or length > w:
                continue
            c = rng.randint(0, w - length)
            for i in range(length):
                g[r][c + i] = 1
            used_rows.add(r)
            break
    for _ in range(20):
        r = rng.randint(0, h - 1)
        if r not in used_rows:
            length = 4
            c = rng.randint(0, w - length)
            for i in range(length):
                g[r][c + i] = 1
            used_rows.add(r)
            break
    cv = rng.randint(0, w - 1)
    rv = rng.randint(0, h - 4)
    for dr in range(3):
        if g[rv + dr][cv] == 0:
            g[rv + dr][cv] = 1
    g[h - 2][0] = 7; g[h - 1][0] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 11
    g = full_grid(h, w, 0)
    if name == "only_even_lengths":
        # only even-length horizontal 1-lines → no odd-length lines, rule fires zero times
        for c in range(1, 5): g[2][c] = 1   # length 4
        for c in range(3, 7): g[5][c] = 1   # length 4
        return g
    if name == "only_vertical":
        # only vertical 1-lines → predicate "single row" fails, rule fires zero times
        for r in range(1, 5): g[r][2] = 1
        for r in range(3, 7): g[r][7] = 1
        return g
    if name == "no_lines":
        # blank grid → no 1-cells at all, rule fires zero times
        return g
    return g
