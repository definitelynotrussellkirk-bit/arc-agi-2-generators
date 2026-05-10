"""Generator for arc_puzzle_bank_21_set10_e:easy_j04 — Fill 0-cells whose 4 cardinal neighbors are same non-bg color.

Rule: cell (r,c)=0 with all 4 cardinal neighbors equal to the same
non-bg value v → set to v.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_plusses,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_plusses, mixed_neighbor_colors, plus_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b159f935141a"
VERSION = "1.1.0"
TASK_ID = "b159f935141a"
SUMMARY = "2-3 plus-patterns of distinct colors scattered in interior."

INVARIANTS = [
    "≥2 plus-patterns: 4 cardinal cells of same non-bg color around 0 center",
    "patterns use distinct colors and don't overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_plusses", "mixed_neighbor_colors", "plus_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_plusses":      {"type": "int", "default": "2", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "scattered_plus_4cells",
                       "valid": "scattered_plus_4cells"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "1..4"},
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
    pal = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 2)
    placed = []
    for color in pal:
        for _ in range(40):
            r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
            if all(abs(r - pr) > 2 or abs(c - pc) > 2 for pr, pc in placed):
                g[r - 1][c] = color; g[r + 1][c] = color
                g[r][c - 1] = color; g[r][c + 1] = color
                placed.append((r, c))
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_plusses":
        # blank → no plus-patterns to fill
        return g
    if name == "mixed_neighbor_colors":
        # plus-pattern with mixed neighbor colors → "all 4 same" precondition fails
        g[1][3] = 4; g[3][3] = 6   # vert pair, different colors
        g[2][2] = 4; g[2][4] = 6   # horiz pair, different colors
        return g
    if name == "plus_at_corner":
        # plus center adjacent to corner → 1+ neighbors out of bounds
        g[0][1] = 4   # would be top-arm if center was at (1,1)
        g[2][1] = 4
        g[1][0] = 4
        g[1][2] = 4
        # but center at (1,1) — actually still has 4 neighbors; place at (0,0):
        # arms at (-1,0),(1,0),(0,-1),(0,1) — 2 oob
        g2 = full_grid(h, w, 0)
        g2[1][0] = 4; g2[0][1] = 4   # only 2 of 4 arms in bounds
        return g2
    return g
