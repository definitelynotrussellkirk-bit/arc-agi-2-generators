"""Generator for arc_additional_puzzle_bank_volume4:E23 — Fill 0 between vertical 3-pair with 2.

Rule: cell (r,c) becomes 2 if it's currently 0 and the cells directly
above (r-1,c) and below (r+1,c) are both 3.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, gap_already_filled, horizontal_pairs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1409f5f7af2e"
VERSION = "1.1.0"
TASK_ID = "1409f5f7af2e"
SUMMARY = "Scattered 3s with at least 2 vertical pairs (3 above and below same col, gap of 1)."

INVARIANTS = [
    ">=2 vertical 3-pairs (3 at r-1 and r+1, same c, with 0 between)",
    ">=3 random isolated 3s as decoration",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "gap_already_filled", "horizontal_pairs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "vertical_pair",
                       "valid": "vertical_pair"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    cols = rng.sample(range(w), 3)
    used_rows = set()
    for c in cols:
        for _ in range(20):
            r = rng.randint(1, h - 2)
            if r not in used_rows and r - 1 not in used_rows and r + 1 not in used_rows:
                g[r - 1][c] = 3; g[r + 1][c] = 3
                used_rows.update([r - 1, r, r + 1])
                break
    for _ in range(rng.randint(3, 5)):
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] == 0:
            g[r][c] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # 3s present but no vertical-pair-with-gap → rule has no targets, output identity
        for r, c in [(1, 1), (3, 5), (5, 8), (7, 2), (9, 4)]:
            g[r][c] = 3
        return g
    if name == "gap_already_filled":
        # vertical pairs exist but the gap cells are already non-zero → rule no-op for those
        for c in [3, 6]:
            g[2][c] = 3
            g[3][c] = 5  # gap already filled with non-bg, non-2
            g[4][c] = 3
        return g
    if name == "horizontal_pairs":
        # 3-pairs are horizontal not vertical → rule's vertical-only condition never matches
        for r in [3, 6]:
            g[r][2] = 3
            g[r][4] = 3  # horizontal pair, gap at (r, 3)
        return g
    return g
