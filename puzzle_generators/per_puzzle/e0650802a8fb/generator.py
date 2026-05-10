"""Generator for arc_puzzle_bank_eleventh_21_bundle:easy_71_fill_diagonal_between_matching_endpoints.

Rule: each color appearing exactly twice on a perfect diagonal fills
its diagonal span between endpoints.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, pairs, texture.
Degenerates: no_pairs, axis_aligned, single_endpoint.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e0650802a8fb"
VERSION = "1.1.0"
TASK_ID = "e0650802a8fb"

SUMMARY = "Place same-color endpoint pairs on clean diagonals to be filled."

INVARIANTS = [
    "background is 0",
    "each active color appears exactly twice",
    "same-color cells are endpoints of one perfect diagonal",
    "diagonal spans do not overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "axis_aligned", "single_endpoint")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "pairs":          {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "= pairs", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "scattered_diagonal_pairs",
                       "valid": "scattered_diagonal_pairs"},
    "n_distinct_colors": {"type": "int", "default": "= pairs", "valid": "1..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _diag_cells(r0, c0, r1, c1):
    dr = 1 if r1 > r0 else -1
    dc = 1 if c1 > c0 else -1
    return [(r0 + dr * k, c0 + dc * k) for k in range(abs(r1 - r0) + 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("pairs", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 10, 14)
        target = ctx.draw_int("pairs", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("pairs", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], k=target)
    placed = 0
    for _ in range(400):
        if placed >= target:
            break
        length = rng.randint(2, min(5, h - 1, w - 1))
        r0 = rng.randint(0, h - length - 1)
        c0 = rng.randint(0, w - length - 1)
        if rng.randrange(2):
            a, b = (r0, c0), (r0 + length, c0 + length)
        else:
            a, b = (r0, c0 + length), (r0 + length, c0)
        cells = _diag_cells(*a, *b)
        if any(cell in reserved for cell in cells):
            continue
        color = colors[placed]
        g[a[0]][a[1]] = color
        g[b[0]][b[1]] = color
        reserved.update(cells)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Empty grid — rule has no diagonal pairs to fill.
        return g
    if name == "axis_aligned":
        # Pair shares row or column rather than a diagonal — rule's
        # diagonal-only filter excludes them.
        g[3][2] = 4; g[3][7] = 4
        return g
    if name == "single_endpoint":
        # Color appears only once — rule's "exactly two endpoints"
        # check excludes it.
        g[2][2] = 4
        return g
    return g
