"""Generator for arc_puzzle_bank_21_set10_s:S10_E7 — Most-frequent color → bottom-row bar.

Rule: count cells per color; pick most-frequent (color asc on ties).
Output: empty grid with the bottom row's first N cells in that color
where N is the count.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_max_count, single_color, max_count_exceeds_width.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d1bdd8b75ba4"
VERSION = "1.1.0"
TASK_ID = "d1bdd8b75ba4"
SUMMARY = "2-3 colors with distinct counts; most-frequent is unique."

INVARIANTS = [
    "≥2 distinct non-bg colors with distinct counts",
    "max count ≤ w (so bar fits)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_max_count", "single_color", "max_count_exceeds_width")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "scattered_distinct_freqs",
                       "valid": "scattered_distinct_freqs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..4"},
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
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 7, 9)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_colors = rng.randint(2, 3)
    palette = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], n_colors)
    counts = rng.sample(range(1, min(w, h) + 1), n_colors)
    cells = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(cells)
    idx = 0
    for color, cnt in zip(palette, counts):
        for _ in range(cnt):
            r, c = cells[idx]; idx += 1
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "tied_max_count":
        # 2 colors tied for max → "most frequent" tied; rule uses color-asc tiebreak
        g[0][0] = 4; g[0][1] = 4; g[0][2] = 4
        g[1][0] = 6; g[1][1] = 6; g[1][2] = 6
        g[2][0] = 3
        return g
    if name == "single_color":
        # only 1 color present → trivial: that's the most-frequent (count = total)
        g[0][0] = 4; g[1][2] = 4; g[2][3] = 4; g[3][1] = 4
        return g
    if name == "max_count_exceeds_width":
        # most-frequent count > w → bar can't fit in bottom row
        # (here w=8, count=10 of color 4)
        for i in range(10):
            r, c = divmod(i, w); g[r][c] = 4
        g[3][7] = 6  # other color, smaller count
        return g
    return g
