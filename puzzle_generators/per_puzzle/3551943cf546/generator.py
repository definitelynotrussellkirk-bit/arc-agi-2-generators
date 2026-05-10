"""Generator for arc_additional_puzzles_21_set21_bundle:E142 — Per-row connect 2-cell pairs of any color.

Rule: in each row, for each color with exactly 2 cells, fill all
cells between them inclusive with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, mismatched_endpoints, span_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3551943cf546"
VERSION = "1.1.0"
TASK_ID = "3551943cf546"
SUMMARY = "2-3 rows have color-pairs with exactly 2 cells of one color separated by 0s."

INVARIANTS = [
    "≥2 rows have a color appearing exactly twice, separated by ≥2 empty cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "mismatched_endpoints", "span_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "row_pairs",
                       "valid": "row_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..8"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used_rows = set()
    palette = [2, 3, 4, 5, 6, 7, 8, 9]
    for _ in range(rng.randint(2, 3)):
        for _ in range(20):
            r = rng.randint(0, h - 1)
            if r in used_rows:
                continue
            color = rng.choice(palette)
            cs = sorted(rng.sample(range(w), 2))
            if cs[1] - cs[0] >= 3:
                g[r][cs[0]] = color; g[r][cs[1]] = color
                used_rows.add(r)
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # singletons only — no color appears exactly twice in any row
        g[1][2] = 4
        g[3][5] = 6
        return g
    if name == "mismatched_endpoints":
        # row has 2 cells but in different colors → not a same-color pair
        g[1][1] = 4; g[1][6] = 6
        g[3][2] = 7; g[3][7] = 8
        return g
    if name == "span_already_filled":
        # both endpoints + everything between already painted → rule is identity
        for c in range(1, 7): g[1][c] = 4
        for c in range(2, 6): g[3][c] = 6
        return g
    return g
