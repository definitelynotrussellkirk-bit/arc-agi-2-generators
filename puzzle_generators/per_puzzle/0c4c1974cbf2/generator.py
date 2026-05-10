"""Generator for arc_puzzle_bank_21_set8_s:S8_E6 — fold across 8-bar, mark overlaps with 2.

Rule: after folding across a color-8 bar, right-side cells with
nonzero overlap are marked 2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, overlap_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_bar, no_overlap, all_overlap.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0c4c1974cbf2"
VERSION = "1.1.0"
TASK_ID = "0c4c1974cbf2"

SUMMARY = "After folding across a color-8 bar, right-side cells with nonzero overlap are marked 2."

INVARIANTS = [
    "background is 0",
    "there is exactly one full-height color-8 divider",
    "at least one mirrored left/right pair is nonzero on both sides",
    "output marks only overlapped right-side folded positions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_bar", "no_overlap", "all_overlap")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng odd 9..13", "valid": "7..17"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "overlap_count":  {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "bar_with_mirror_pairs",
                       "valid": "bar_with_mirror_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 11)
        count = ctx.draw_int("overlap_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 13)
        count = ctx.draw_int("overlap_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 13)
        count = ctx.draw_int("overlap_count", 2, 4)
    if w % 2 == 0:
        w += 1
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    b = w // 2
    for r in range(h):
        g[r][b] = 8
    pairs = rng.sample([(r, c) for r in range(h) for c in range(b)], count)
    for idx, (r, c) in enumerate(pairs):
        mc = 2 * b - c
        g[r][c] = [3, 4, 6, 7][idx % 4]
        g[r][mc] = [2, 5, 9, 1][idx % 4]
    for r, c in rng.sample([(r, c) for r in range(h) for c in range(b)], min(2, h)):
        if g[r][c] == 0:
            g[r][c] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    b = w // 2
    if name == "no_bar":
        # left/right cells exist but no 8-divider → no fold axis defined
        g[2][1] = 4; g[2][7] = 6
        g[5][2] = 3; g[5][6] = 7
        return g
    if name == "no_overlap":
        # bar exists but no mirrored cells overlap → nothing to mark
        for r in range(h): g[r][b] = 8
        g[1][1] = 4   # left only (no right counterpart)
        g[3][7] = 6   # right only (no left counterpart)
        return g
    if name == "all_overlap":
        # every left cell mirrors a right cell → entire left side gets marked
        for r in range(h): g[r][b] = 8
        for r in range(h):
            for c in range(b):
                g[r][c] = 4
                g[r][2 * b - c] = 6
        return g
    return g
