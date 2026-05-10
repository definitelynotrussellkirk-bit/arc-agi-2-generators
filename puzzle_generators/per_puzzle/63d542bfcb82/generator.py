"""Generator for arc_puzzle_bank_eleventh21:E73.

Rule: fill a zero center surrounded by four same-color diagonal cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motifs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_xs, mixed_corner_colors, center_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "63d542bfcb82"
VERSION = "1.1.0"
TASK_ID = "63d542bfcb82"
SUMMARY = "Fill a zero center surrounded by four same-color diagonal cells."

INVARIANTS = [
    "background is 0",
    "each active center has four same-color diagonal neighbors",
    "active centers are initially zero",
    "X motifs are isolated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_xs", "mixed_corner_colors", "center_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motifs":         {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_xs",
                       "valid": "spaced_xs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear(g, r, c):
    h, w = len(g), len(g[0])
    for rr in range(max(0, r - 2), min(h, r + 3)):
        for cc in range(max(0, c - 2), min(w, c + 3)):
            if g[rr][cc] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 8, 8)
        target = ctx.draw_int("motifs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("motifs", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
        target = ctx.draw_int("motifs", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(180):
        if placed >= target:
            break
        r = rng.randint(1, h - 2)
        c = rng.randint(1, w - 2)
        if not _clear(g, r, c):
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            g[r + dr][c + dc] = color
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_xs":
        # blank grid → no diagonal-X patterns to detect, rule is identity
        return g
    if name == "mixed_corner_colors":
        # 4 diagonal corners with mixed colors → predicate "all same color" fails
        for (r, c, col) in [(2, 2, 4), (2, 4, 6), (4, 2, 4), (4, 4, 4)]: g[r][c] = col
        return g
    if name == "center_filled":
        # center already non-zero → predicate "center is 0" fails, rule does nothing
        for (r, c) in [(2, 2), (2, 4), (4, 2), (4, 4)]: g[r][c] = 4
        g[3][3] = 8   # center already filled
        return g
    return g
