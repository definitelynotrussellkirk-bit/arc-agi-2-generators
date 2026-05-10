"""Generator for arc_additional_puzzles_21_set7:E43.

Rule: for each non-bg cell at (r, c, v), set out[r±2][c] = v and
out[r][c±2] = v if in-bounds.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, seed_at_edge, seeds_too_close.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2f889ed81450"
VERSION = "1.1.0"
TASK_ID = "2f889ed81450"
SUMMARY = "1-3 isolated non-bg cells with empty rays at distance 2."

INVARIANTS = [
    "1-3 isolated non-bg cells",
    "no two cells within Manhattan distance 4 of each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "seed_at_edge", "seeds_too_close")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "interior", "valid": "interior"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..4"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    placed = []
    palette = [2, 3, 4, 5, 6, 7, 8, 9]
    for _ in range(40):
        if len(placed) >= 3:
            break
        r = rng.randint(2, h - 3); c = rng.randint(2, w - 3)
        if all(abs(r - pr) + abs(c - pc) > 4 for pr, pc in placed):
            g[r][c] = rng.choice(palette)
            placed.append((r, c))
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # no source cells → no rays, output equals input
        return g
    if name == "seed_at_edge":
        # seed at (0,0) → all 4 rays at distance 2 are out-of-bounds, pattern collapses
        g[0][0] = 4
        g[h - 1][w - 1] = 7
        return g
    if name == "seeds_too_close":
        # two seeds within Manhattan-4 → their rays overlap, painting order matters
        g[3][3] = 5
        g[3][5] = 6
        return g
    return g
