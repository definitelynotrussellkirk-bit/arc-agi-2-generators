"""Generator for arc_puzzle_bank_21_set8_s:S8_M5 — tile rectangle from seed row.

Rule: a seed row of small distinct colors (e.g. 2,3,4) in row 0. A
solid rectangle of color 8 elsewhere. Output: replace the rectangle's
cells with the seed row repeated to the rect's width.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seed,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seed, no_rect, monochrome_seed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "331074b4dcbc"
VERSION = "1.1.0"
TASK_ID = "331074b4dcbc"
SUMMARY = "Seed row (left of row 0, 2-3 distinct colors) + a solid 8-rect below."

INVARIANTS = [
    "background is 0",
    "row 0 has a contiguous seed of 2-3 distinct non-8 colors at the leftmost cols",
    "exactly one solid 8-rect of size ≥ 2x4 elsewhere",
    "8-rect's row range doesn't include row 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seed", "no_rect", "monochrome_seed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seed":         {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "seed_row_plus_8_rect",
                       "valid": "seed_row_plus_8_rect"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_seed = rng.randint(2, 3)
    seed_palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], n_seed)
    for i, color in enumerate(seed_palette):
        g[0][i] = color
    rh = rng.randint(2, 3)
    rw = rng.randint(5, 8)
    r1 = rng.randint(2, h - rh - 1)
    c1 = rng.randint(2, w - rw - 1)
    for r in range(r1, r1 + rh):
        for c in range(c1, c1 + rw):
            g[r][c] = 8
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 12
    g = full_grid(h, w, 0)
    if name == "no_seed":
        # 8-rect alone with no row-0 seed → no tile pattern to apply
        for r in range(3, 5):
            for c in range(3, 9):
                g[r][c] = 8
        return g
    if name == "no_rect":
        # seed row alone with no 8-rect → nothing to tile into
        g[0][0] = 2; g[0][1] = 3; g[0][2] = 4
        return g
    if name == "monochrome_seed":
        # seed row is one color repeated → tile result indistinguishable from solid
        g[0][0] = 3; g[0][1] = 3; g[0][2] = 3
        for r in range(3, 5):
            for c in range(3, 9):
                g[r][c] = 8
        return g
    return g
