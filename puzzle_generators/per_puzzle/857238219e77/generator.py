"""Generator for arc_puzzle_bank_21_set15_bundle:easy_o07.

Isolated vertical trios are replaced by centered horizontal trios.

Combinatorial axes (8): grid_h, grid_w, palette_kind, run_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_runs, length_2_runs, runs_on_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "857238219e77"
VERSION = "1.1.0"
TASK_ID = "857238219e77"
SUMMARY = "Separated vertical runs of exactly three cells away from side edges."

INVARIANTS = [
    "background is 0",
    "all nonzero objects are vertical runs of length exactly three",
    "run middle columns are not on the left or right edge",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_runs", "length_2_runs", "runs_on_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "run_count":      {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "vertical_3_runs",
                       "valid": "vertical_3_runs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear_zone(g, r, c):
    h, w = len(g), len(g[0])
    for rr in range(max(0, r - 1), min(h, r + 4)):
        for cc in range(max(0, c - 2), min(w, c + 3)):
            if g[rr][cc] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        run_count = ctx.draw_int("run_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        run_count = ctx.draw_int("run_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        run_count = ctx.draw_int("run_count", 2, 4)
    colors = ctx.draw_distinct_colors("colors", n=run_count, exclude={0})
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for color in colors:
        for _ in range(300):
            r = rng.randint(0, h - 3)
            c = rng.randint(1, w - 2)
            if _clear_zone(g, r, c):
                for rr in range(r, r + 3):
                    g[rr][c] = color
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_runs":
        # blank → no vertical runs to convert
        return g
    if name == "length_2_runs":
        # length-2 runs → "length exactly three" precondition fails
        for r in [1, 2]: g[r][3] = 4
        for r in [4, 5]: g[r][6] = 6
        return g
    if name == "runs_on_edge":
        # run at col 0 → can't center horizontal trio (out of bounds left)
        for r in range(1, 4): g[r][0] = 4
        return g
    return g
