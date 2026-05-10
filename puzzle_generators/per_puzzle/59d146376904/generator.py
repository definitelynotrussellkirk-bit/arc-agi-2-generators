"""Generator for 10b:m67 — summarize quadrant majorities.

Rule: split the grid into 2x2 quadrants. For each quadrant, find its
majority non-bg color. Output is a 2x2 grid of those majority colors.

Combinatorial axes (8): grid_h, grid_w, palette_kind, qh,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cells, single_quadrant_filled, tied_majority.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "59d146376904"
VERSION = "1.1.0"
TASK_ID = "59d146376904"
SUMMARY = "Even-sized grid (2*qh x 2*qw); each quadrant has a clear majority color."

INVARIANTS = [
    "background is 0",
    "grid h is 2*qh and w is 2*qw",
    "each of the 4 quadrants has a strict majority of one non-bg color",
    "all 4 quadrants use distinct majority colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cells", "single_quadrant_filled", "tied_majority")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "4..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "qh":             {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "qw":             {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "four_quadrants_majority",
                       "valid": "four_quadrants_majority"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "dense", "valid": "dense"},
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
        qh = ctx.draw_int("qh", 3, 3)
        qw = ctx.draw_int("qw", 3, 3)
    elif difficulty == "hard":
        qh = ctx.draw_int("qh", 4, 4)
        qw = ctx.draw_int("qw", 4, 5)
    else:
        qh = ctx.draw_int("qh", 3, 4)
        qw = ctx.draw_int("qw", 3, 5)
    rng = ctx.draw_rng("layout")
    h = qh * 2; w = qw * 2
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 4)
    quads = [(0, 0), (0, qw), (qh, 0), (qh, qw)]
    for color, (r0, c0) in zip(palette, quads):
        cells = [(r0 + dr, c0 + dc) for dr in range(qh) for dc in range(qw)]
        n = rng.randint(max(3, qh * qw // 2 + 1), max(qh * qw - 1, 3))
        for r, c in rng.sample(cells, min(n, len(cells))):
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    qh, qw = 3, 4
    h, w = qh * 2, qw * 2
    g = full_grid(h, w, 0)
    if name == "no_cells":
        # blank → no majorities to summarize
        return g
    if name == "single_quadrant_filled":
        # only one quadrant has cells → other 3 quadrants have no majority
        for r in range(qh):
            for c in range(qw): g[r][c] = 4
        return g
    if name == "tied_majority":
        # quadrant has two colors with equal count → no strict majority
        g[0][0] = 4; g[0][1] = 6
        g[1][0] = 4; g[1][1] = 6   # tied 2-2 in this quadrant
        for r in range(qh):
            for c in range(qw): g[r][qw + c] = 7
        for r in range(qh):
            for c in range(qw): g[qh + r][c] = 8
        for r in range(qh):
            for c in range(qw): g[qh + r][qw + c] = 9
        return g
    return g
