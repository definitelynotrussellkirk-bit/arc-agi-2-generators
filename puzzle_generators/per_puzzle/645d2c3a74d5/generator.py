"""Generator for arc_additional_puzzles_21_set3:E16.

Rule: cell (r,c)=0 with all 4 diagonal neighbors = 1 → set to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_patterns,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_patterns, partial_x, center_already_8.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "645d2c3a74d5"
VERSION = "1.1.0"
TASK_ID = "645d2c3a74d5"
SUMMARY = "2-3 X-patterns of 1s scattered."

INVARIANTS = [
    "≥2 X-patterns: 4 diagonal cells of value 1 around a 0 center",
    "patterns don't overlap",
]

PALETTE_KINDS = ("default", "sparse", "dense", "varied")
DEGENERATE_TEXTURES = ("no_patterns", "partial_x", "center_already_8")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_patterns":     {"type": "int", "default": "2", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "density":        {"type": "str", "default": "mixed", "valid": "mixed"},
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
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    placed = []
    for _ in range(40):
        if len(placed) >= 2:
            break
        r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
        if all(abs(r - pr) > 2 or abs(c - pc) > 2 for pr, pc in placed):
            g[r - 1][c - 1] = 1; g[r - 1][c + 1] = 1
            g[r + 1][c - 1] = 1; g[r + 1][c + 1] = 1
            placed.append((r, c))
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_patterns":
        # empty grid — no X-patterns to detect
        return g
    if name == "partial_x":
        # only 3 diagonal cells of an X → predicate "all 4 diagonals = 1" fails
        g[1][1] = 1; g[1][3] = 1; g[3][1] = 1
        return g
    if name == "center_already_8":
        # complete X but center is already 8 → rule's effect is invisible
        g[1][1] = 1; g[1][3] = 1; g[3][1] = 1; g[3][3] = 1
        g[2][2] = 8
        return g
    return g
