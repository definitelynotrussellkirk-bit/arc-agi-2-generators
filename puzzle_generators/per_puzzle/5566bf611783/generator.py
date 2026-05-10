"""Generator for arc_additional_puzzle_bank_volume20:H140 — Fill 5-walled regions by majority {2,3} color.

Rule: 5-walls divide grid. For each non-5 region, count 2s and 3s; fill
empty cells with majority (8 if equal).

Combinatorial axes (8): grid_h, grid_w, palette_kind, count_range,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, blank_quads, all_tied.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5566bf611783"
VERSION = "1.1.0"
TASK_ID = "5566bf611783"
SUMMARY = "5-walls form 4 compartments; each has different counts of 2s and 3s."

INVARIANTS = [
    "5-walls form 2x2 compartments",
    "each has at least one of {2, 3} (with varying counts)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "blank_quads", "all_tied")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9..9"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13..13"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "count_range":    {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "five_walls_with_counts",
                       "valid": "five_walls_with_counts"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
    rng = ctx.draw_rng("layout")
    h, w = 9, 13
    g = full_grid(h, w, 0)
    div_r = h // 2
    div_c = w // 2
    for c in range(w):
        g[div_r][c] = 5
    for r in range(h):
        g[r][div_c] = 5
    quads = [(1, div_r - 1, 1, div_c - 1),
             (1, div_r - 1, div_c + 1, w - 2),
             (div_r + 1, h - 2, 1, div_c - 1),
             (div_r + 1, h - 2, div_c + 1, w - 2)]
    if difficulty == "easy":
        cmin, cmax = 1, 2
    elif difficulty == "hard":
        cmin, cmax = 2, 3
    else:
        cmin, cmax = 1, 3
    for r0, r1, c0, c1 in quads:
        n2 = rng.randint(cmin, cmax); n3 = rng.randint(cmin, cmax)
        used = set()
        for color, cnt in ((2, n2), (3, n3)):
            placed = 0
            for _ in range(20):
                if placed >= cnt: break
                r = rng.randint(r0, r1); c = rng.randint(c0, c1)
                if (r, c) not in used and g[r][c] == 0:
                    g[r][c] = color; used.add((r, c)); placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 13
    g = full_grid(h, w, 0)
    div_r, div_c = h // 2, w // 2
    if name == "no_walls":
        # 2s and 3s scattered without 5-walls → no compartments to count within
        g[1][2] = 2; g[1][6] = 2
        g[3][9] = 3; g[5][3] = 3
        return g
    if name == "blank_quads":
        # walls present but quadrants empty → no 2s/3s to count, no fill happens
        for c in range(w):
            g[div_r][c] = 5
        for r in range(h):
            g[r][div_c] = 5
        return g
    if name == "all_tied":
        # every quadrant has equal 2s and 3s → rule's tie-break (8) fires everywhere
        for c in range(w):
            g[div_r][c] = 5
        for r in range(h):
            g[r][div_c] = 5
        g[1][1] = 2; g[1][2] = 3
        g[1][7] = 2; g[1][8] = 3
        g[5][1] = 2; g[5][2] = 3
        g[5][7] = 2; g[5][8] = 3
        return g
    return g
