"""Generator for arc_puzzle_bank_twentieth21:E140 — fill 3x3 hollow center.

Rule: a 3x3 block has a uniform-color border (all 8 perimeter cells the same
color) and a 0 center; output fills the center with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_blocks, texture.
Degenerates: no_blocks, mixed_border, no_hollow_center.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3ef9eae12446"
VERSION = "1.1.0"
TASK_ID = "3ef9eae12446"

SUMMARY = "1-2 3x3 blocks each with uniform-color border and 0 center."

INVARIANTS = [
    "background is 0",
    "1-2 disjoint 3x3 hollow blocks; each has uniform-color border and 0 center",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blocks", "mixed_border", "no_hollow_center")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blocks":       {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "= n_blocks", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "scattered_3x3_blocks",
                       "valid": "scattered_3x3_blocks"},
    "n_distinct_colors": {"type": "int", "default": "= n_blocks", "valid": "1..3"},
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
        w = ctx.draw_int("grid_w", 7, 7)
        n = ctx.draw_int("n_blocks", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 12)
        n = ctx.draw_int("n_blocks", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 7, 9)
        n = ctx.draw_int("n_blocks", 1, 2)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
        ok = True
        for color in colors:
            placed = False
            for _ in range(80):
                r0 = rng.randint(0, h - 3); c0 = rng.randint(0, w - 3)
                if not _free(g, r0, c0, r0 + 2, c0 + 2): continue
                for dr in range(3):
                    for dc in range(3):
                        if (dr, dc) != (1, 1):
                            g[r0 + dr][c0 + dc] = color
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize E140 layout")


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_blocks":
        # Empty grid — rule has no 3x3 hollow blocks to fill.
        return g
    if name == "mixed_border":
        # 3x3 border has multiple colors — rule's "uniform border"
        # precondition fails; fill color is undefined.
        block = [(0, 0, 4), (0, 1, 4), (0, 2, 6), (1, 0, 4), (1, 2, 6),
                 (2, 0, 4), (2, 1, 6), (2, 2, 6)]
        for dr, dc, c in block:
            g[2 + dr][3 + dc] = c
        return g
    if name == "no_hollow_center":
        # 3x3 already fully solid — rule's "0 center" precondition
        # fails.
        for dr in range(3):
            for dc in range(3):
                g[2 + dr][3 + dc] = 4
        return g
    return g
