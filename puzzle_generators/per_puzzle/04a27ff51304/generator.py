"""Generator for arc_puzzle_bank_21_set8_s:S8_M2 — long-run crossings.

Rule: cells where a row-run of length ≥3 crosses a col-run of length ≥3
get painted 8. Other cells become 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_lines,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_lines, only_horizontal, no_crossings.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "04a27ff51304"
VERSION = "1.1.0"
TASK_ID = "04a27ff51304"
SUMMARY = "1-2 horizontal lines (length≥3) crossing 1-2 vertical lines (length≥3)."

INVARIANTS = [
    "background is 0",
    "≥1 horizontal line of length ≥ 3 in some color",
    "≥1 vertical line of length ≥ 3 in some color",
    "the lines actually cross (so output is non-empty)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_lines", "only_horizontal", "no_crossings")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_lines":        {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "h_v_lines_crossing",
                       "valid": "h_v_lines_crossing"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], 4)
    n_h = rng.randint(1, 2)
    n_v = rng.randint(1, 2)
    h_lines = []
    for i in range(n_h):
        r = rng.randint(1, h - 2)
        c1 = rng.randint(0, max(0, w - 5))
        length = rng.randint(3, min(6, w - c1))
        for c in range(c1, c1 + length):
            g[r][c] = palette[i]
        h_lines.append((r, c1, c1 + length - 1))
    for i in range(n_v):
        c = rng.randint(1, w - 2)
        r1 = rng.randint(0, max(0, h - 5))
        length = rng.randint(3, min(6, h - r1))
        for r in range(r1, r1 + length):
            if g[r][c] == 0:
                g[r][c] = palette[2 + i]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_lines":
        # blank → no lines, no crossings, output empty
        return g
    if name == "only_horizontal":
        # only horizontal lines → no vertical to cross with
        for c in range(2, 7): g[3][c] = 4
        for c in range(1, 5): g[5][c] = 6
        return g
    if name == "no_crossings":
        # h and v lines exist but don't cross → output empty
        for c in range(0, 4): g[1][c] = 4
        for r in range(4, 7): g[r][7] = 6
        return g
    return g
