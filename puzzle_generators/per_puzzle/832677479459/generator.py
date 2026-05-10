"""Generator for arc_puzzle_bank_twentieth21:E139 — keep most-frequent color.

Rule: only the most-frequent non-zero color is kept; all other non-zeros
become 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_majority, single_color, all_minority.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "832677479459"
VERSION = "1.1.0"
TASK_ID = "832677479459"
SUMMARY = "Several non-zero cells in 2-3 colors; one color is strictly more frequent."

INVARIANTS = [
    "background is 0",
    "2-3 non-zero colors used; one strictly outnumbers the others",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_majority", "single_color", "all_minority")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..5", "valid": "3..8"},
    "grid_w":         {"type": "int", "default": "rng 5..6", "valid": "4..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "scattered_majority",
                       "valid": "scattered_majority"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "density":        {"type": "str", "default": "scattered", "valid": "scattered"},
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
        h = ctx.draw_int("grid_h", 4, 4)
        w = ctx.draw_int("grid_w", 5, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 6, 6)
    else:
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 5, 6)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        n_colors = rng.randint(2, 3)
        colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n_colors)
        major = colors[0]
        n_major = rng.randint(4, 6)
        n_minor = rng.randint(1, 2)
        positions = []
        for _ in range(n_major):
            for _t in range(40):
                r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
                if g[r][c] != 0: continue
                g[r][c] = major
                positions.append((r, c))
                break
        for color in colors[1:]:
            for _ in range(n_minor):
                for _t in range(40):
                    r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
                    if g[r][c] != 0: continue
                    g[r][c] = color
                    break
        from collections import Counter
        cnts = Counter(v for row in g for v in row if v != 0)
        if cnts[major] > max((c for k, c in cnts.items() if k != major), default=0):
            return g
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 6
    g = full_grid(h, w, 0)
    if name == "tied_majority":
        # two colors tied for max → "most-frequent" is ambiguous
        for (r, c) in [(0, 0), (1, 1), (2, 2)]: g[r][c] = 4   # 3 cells
        for (r, c) in [(3, 0), (3, 2), (3, 4)]: g[r][c] = 6   # 3 cells, also max
        return g
    if name == "single_color":
        # only one color → trivially most-frequent, rule is identity
        for (r, c) in [(0, 0), (1, 2), (2, 4), (3, 1)]: g[r][c] = 4
        return g
    if name == "all_minority":
        # all colors equally rare (each has 1 cell) → no strict majority
        g[0][0] = 4; g[1][2] = 6; g[2][4] = 3; g[3][1] = 8
        return g
    return g
