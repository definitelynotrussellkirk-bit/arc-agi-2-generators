"""Generator for arc_puzzle_bank_eighteenth21:E124.

Fill the one missing arm of each partial plus.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_motifs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_motifs, full_plus, missing_two_arms.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fc999420d3aa"
VERSION = "1.1.0"
TASK_ID = "fc999420d3aa"

SUMMARY = "Fill the one missing arm of each partial plus."

INVARIANTS = [
    "background is 0",
    "each motif has a center and exactly three matching cardinal arms",
    "the missing in-bounds arm cell is initially zero",
    "partial plus motifs are isolated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motifs", "full_plus", "missing_two_arms")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_motifs":       {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "isolated_partial_pluses",
                       "valid": "isolated_partial_pluses"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear(g, r, c):
    h, w = len(g), len(g[0])
    for rr in range(max(0, r - 2), min(h, r + 3)):
        for cc in range(max(0, c - 2), min(w, c + 3)):
            if g[rr][cc] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("motifs", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("motifs", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("motifs", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = 0
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for _ in range(160):
        if placed >= target:
            break
        r = rng.randint(1, h - 2)
        c = rng.randint(1, w - 2)
        if not _clear(g, r, c):
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        missing = rng.choice(deltas)
        g[r][c] = color
        for dr, dc in deltas:
            if (dr, dc) != missing:
                g[r + dr][c + dc] = color
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "no_motifs":
        # blank → no partial pluses to complete
        return g
    if name == "full_plus":
        # complete 5-cell plus → no missing arm to fill, rule is identity
        cr, cc = 3, 4
        g[cr][cc] = 4
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            g[cr + dr][cc + dc] = 4
        return g
    if name == "missing_two_arms":
        # only 2 arms present → "exactly three" precondition fails
        cr, cc = 3, 4
        g[cr][cc] = 4
        g[cr - 1][cc] = 4; g[cr][cc + 1] = 4
        return g
    return g
