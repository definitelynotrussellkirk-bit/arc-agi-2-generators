"""Generator for arc_puzzle_bank_21_set17_s:S17_H7.

Rule: 3 single-cell markers in distinct colors at distinct positions.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: too_few_markers, duplicate_colors, adjacent_markers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "46c405d73c2a"
VERSION = "1.1.0"
TASK_ID = "46c405d73c2a"
SUMMARY = "3 single-cell markers in distinct colors at distinct positions."

INVARIANTS = [
    "background is 0",
    "3 single-cell markers in distinct non-zero colors at distinct positions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("too_few_markers", "duplicate_colors", "adjacent_markers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 10)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    colors = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 3)
    placed = []
    for color in colors:
        for _t in range(80):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] != 0: continue
            if any(abs(r - pr) + abs(c - pc) < 3 for pr, pc in placed): continue
            g[r][c] = color
            placed.append((r, c))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "too_few_markers":
        # only 1-2 markers → 3-marker assumption violated
        g[2][2] = 3
        g[6][7] = 5
        return g
    if name == "duplicate_colors":
        # two markers share a color → "distinct colors" assumption violated
        g[1][1] = 4
        g[4][6] = 4
        g[7][3] = 7
        return g
    if name == "adjacent_markers":
        # markers placed adjacent → distance-3 separation invariant violated
        g[3][3] = 3
        g[3][4] = 5
        g[4][3] = 7
        return g
    return g
