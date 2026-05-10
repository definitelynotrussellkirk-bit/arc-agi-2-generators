"""Generator for arc_additional_puzzle_bank_volume8:H51 — Mark k-th largest 4-frame.

Rule: k = count of color-1 cells. Find the k-th largest (by bbox area)
4-frame component; recolor its cells to 3.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames, k,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: k_too_large, no_ones, tied_areas.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a1105be40960"
VERSION = "1.1.0"
TASK_ID = "a1105be40960"
SUMMARY = "Several nested 4-frames + k color-1 cells; output recolors the k-th largest frame to 3."

INVARIANTS = [
    "between 3 and 6 nested 4-frames with distinct bbox areas",
    "between 1 and n_frames color-1 cells in upper area",
    "k = count of 1s",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("k_too_large", "no_ones", "tied_areas")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "n_frames":       {"type": "int", "default": "rng 3..6", "valid": "3..7"},
    "k":              {"type": "int", "default": "rng 1..n", "valid": "1..n"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "nested_4frames_with_count",
                       "valid": "nested_4frames_with_count"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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
        n_frames = ctx.draw_int("n_frames", 3, 3)
    elif difficulty == "hard":
        n_frames = ctx.draw_int("n_frames", 5, 6)
    else:
        n_frames = ctx.draw_int("n_frames", 3, 6)
    rng = ctx.draw_rng("layout")
    inner = 1
    side = inner + (n_frames - 1) * 4
    h = side + 4
    w = side + 4
    g = full_grid(h, w, 0)
    r1, c1 = 2, 2
    r2, c2 = h - 3, w - 3
    for i in range(n_frames):
        for c in range(c1, c2 + 1):
            g[r1][c] = 4
            g[r2][c] = 4
        for r in range(r1, r2 + 1):
            g[r][c1] = 4
            g[r][c2] = 4
        if r2 - r1 < 3 or c2 - c1 < 3:
            break
        r1 += 2; c1 += 2; r2 -= 2; c2 -= 2
    k = ctx.draw_int("k", 1, n_frames)
    for i in range(k):
        g[0][i] = 1
    return g


def _draw_from_degenerate(name, rng):
    n_frames = 4
    inner = 1
    side = inner + (n_frames - 1) * 4
    h = side + 4
    w = side + 4
    g = full_grid(h, w, 0)
    r1, c1 = 2, 2
    r2, c2 = h - 3, w - 3
    if name == "k_too_large":
        # k=8 > n_frames=4 → no k-th frame exists, rule has no target
        for i in range(n_frames):
            for c in range(c1, c2 + 1):
                g[r1][c] = 4; g[r2][c] = 4
            for r in range(r1, r2 + 1):
                g[r][c1] = 4; g[r][c2] = 4
            if r2 - r1 < 3 or c2 - c1 < 3: break
            r1 += 2; c1 += 2; r2 -= 2; c2 -= 2
        for i in range(8):
            g[0][i] = 1
        return g
    if name == "no_ones":
        # k = 0 → no frame to recolor, rule is identity
        for i in range(n_frames):
            for c in range(c1, c2 + 1):
                g[r1][c] = 4; g[r2][c] = 4
            for r in range(r1, r2 + 1):
                g[r][c1] = 4; g[r][c2] = 4
            if r2 - r1 < 3 or c2 - c1 < 3: break
            r1 += 2; c1 += 2; r2 -= 2; c2 -= 2
        return g
    if name == "tied_areas":
        # two frames with equal bbox area → "k-th largest" tie-break ambiguous
        # left frame
        for c in range(2, 7):
            g[2][c] = 4; g[6][c] = 4
        for r in range(2, 7):
            g[r][2] = 4; g[r][6] = 4
        # right frame, same 5x5 area
        for c in range(9, 14):
            g[2][c] = 4; g[6][c] = 4
        for r in range(2, 7):
            g[r][9] = 4; g[r][13] = 4
        g[0][0] = 1; g[0][1] = 1  # k=2
        return g
    return g
