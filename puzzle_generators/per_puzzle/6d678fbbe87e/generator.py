"""Generator for arc_puzzle_bank_twentysecond21:E149 — complete 2x2 corner.

Rule: a 2×2 block has 3 cells of the same color and 1 zero cell. Output
fills the missing corner with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blocks,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blocks, full_block, dense_blocks.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6d678fbbe87e"
VERSION = "1.1.0"
TASK_ID = "6d678fbbe87e"

SUMMARY = "1-2 partial 2x2 blocks (3 same-color cells + 1 hole) in distinct colors."

INVARIANTS = [
    "background is 0",
    "1-2 disjoint 2x2 blocks; each has 3 same-color cells and 1 missing (0) cell",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blocks", "full_block", "dense_blocks")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blocks":       {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "scattered_separated",
                       "valid": "scattered_separated"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 5, 5)
        n = ctx.draw_int("n_blocks", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 9)
        n = ctx.draw_int("n_blocks", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 5, 7)
        n = ctx.draw_int("n_blocks", 1, 2)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
        ok = True
        for color in colors:
            placed = False
            for _ in range(80):
                r0 = rng.randint(0, h - 2); c0 = rng.randint(0, w - 2)
                if not _free(g, r0, c0, r0 + 1, c0 + 1): continue
                # 3 cells same color, 1 missing
                missing = rng.choice([(0, 0), (0, 1), (1, 0), (1, 1)])
                for dr in range(2):
                    for dc in range(2):
                        if (dr, dc) != missing:
                            g[r0 + dr][c0 + dc] = color
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize E149 layout")


def _draw_from_degenerate(name, rng):
    h, w = 6, 6
    g = full_grid(h, w, 0)
    if name == "no_blocks":
        # Empty grid — rule has no incomplete blocks to complete.
        return g
    if name == "full_block":
        # 2x2 already complete — nothing to fill, rule is no-op.
        for dr in range(2):
            for dc in range(2): g[1 + dr][1 + dc] = 4
        return g
    if name == "dense_blocks":
        # Two partial 2x2 blocks adjacent — completion fills overlap.
        g[1][1] = 4; g[1][2] = 4; g[2][1] = 4
        g[1][3] = 5; g[1][4] = 5; g[2][4] = 5
        return g
    return g
