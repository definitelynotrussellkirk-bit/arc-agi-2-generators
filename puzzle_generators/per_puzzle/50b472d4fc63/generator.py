"""Generator for arc_puzzle_bank_fourth21:E26 — highlight endpoints of vertical triples.

Rule: place separated exact vertical triples whose endpoints are
highlighted.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_runs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_runs, length_2_runs, length_4_runs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "50b472d4fc63"
VERSION = "1.1.0"
TASK_ID = "50b472d4fc63"

SUMMARY = "Place separated exact vertical triples whose endpoints are highlighted."

INVARIANTS = [
    "background is 0",
    "each target run is vertical and length exactly 3",
    "target run colors are non-8",
    "runs are separated by background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_runs", "length_2_runs", "length_4_runs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_runs":         {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "spaced_vertical_triples",
                       "valid": "spaced_vertical_triples"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 6, 7)
        target = ctx.draw_int("n_runs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("n_runs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 6, 9)
        target = ctx.draw_int("n_runs", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(300):
        if placed >= target:
            break
        r0 = rng.randint(0, h - 3)
        c = rng.randrange(w)
        guard = {
            (r, cc)
            for r in range(max(0, r0 - 1), min(h, r0 + 4))
            for cc in range(max(0, c - 1), min(w, c + 2))
        }
        if guard & reserved:
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
        for dr in range(3):
            g[r0 + dr][c] = color
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 7
    g = full_grid(h, w, 0)
    if name == "no_runs":
        # blank → no triples to highlight endpoints of
        return g
    if name == "length_2_runs":
        # all runs length 2 → "exactly 3" precondition fails
        g[1][1] = 4; g[2][1] = 4
        g[5][4] = 6; g[6][4] = 6
        return g
    if name == "length_4_runs":
        # all runs length 4 → "exactly 3" precondition fails
        for r in range(1, 5): g[r][1] = 4
        for r in range(2, 6): g[r][5] = 6
        return g
    return g
