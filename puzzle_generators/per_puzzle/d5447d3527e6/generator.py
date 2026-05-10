"""Generator for v1_e_m_h_keys:E7.

Combinatorial axes (8): grid_h, grid_w, palette_kind, runs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_runs, all_even, all_short.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d5447d3527e6"
VERSION = "1.1.0"
TASK_ID = "d5447d3527e6"

SUMMARY = "Odd vertical runs of 5 recolor only their center cell to 2."

INVARIANTS = [
    "background is 0",
    "target runs are vertical color-5 runs with odd length at least 3",
    "even and short runs remain as distractors",
    "runs are separated by at least one blank column",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_runs", "all_even", "all_short")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "5..24"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "3..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "runs":           {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "vertical_5_runs",
                       "valid": "vertical_5_runs"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r0, c, length):
    h, w = len(g), len(g[0])
    if r0 < 0 or r0 + length > h:
        return False
    for r in range(max(0, r0 - 1), min(h, r0 + length + 1)):
        for cc in range(max(0, c - 1), min(w, c + 2)):
            if g[r][cc] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("runs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 11, 12)
        target = ctx.draw_int("runs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 8, 12)
        target = ctx.draw_int("runs", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = 0
    for length in [3, 5, 3, 5][:target]:
        for _ in range(80):
            c = rng.randrange(w)
            r0 = rng.randint(0, h - length)
            if _free(g, r0, c, length):
                for r in range(r0, r0 + length):
                    g[r][c] = 5
                placed += 1
                break
    for length in (2, 4):
        for _ in range(60):
            c = rng.randrange(w)
            r0 = rng.randint(0, h - length)
            if _free(g, r0, c, length):
                for r in range(r0, r0 + length):
                    g[r][c] = 5
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 9
    g = full_grid(h, w, 0)
    if name == "no_runs":
        # blank → no runs to recolor
        return g
    if name == "all_even":
        # only even-length runs → no odd targets to recolor center
        for r in range(0, 4): g[r][2] = 5
        for r in range(2, 4): g[r][6] = 5
        return g
    if name == "all_short":
        # only length-1 or length-2 runs → no odd run ≥3, no targets
        g[1][2] = 5
        for r in range(4, 6): g[r][6] = 5
        return g
    return g
