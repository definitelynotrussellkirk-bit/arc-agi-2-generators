"""Generator for arc_additional_puzzle_bank_volume10:M64.

Rule: pairs of same-colored corner markers expand into rectangle perimeters.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, single_marker, collinear_markers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9e0cd377fa63"
VERSION = "1.1.0"
TASK_ID = "9e0cd377fa63"
SUMMARY = "Pairs of same-colored corner markers expand into rectangle perimeters."

INVARIANTS = [
    "background is 0",
    "each active color appears exactly twice",
    "same-colored cells are opposite corners of an axis-aligned rectangle",
    "implied rectangles are separated to avoid color conflicts",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_marker", "collinear_markers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..15", "valid": "6..24"},
    "grid_w":         {"type": "int", "default": "rng 10..15", "valid": "6..24"},
    "n_pairs":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "scattered_corner_pairs",
                       "valid": "scattered_corner_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h = len(g)
    w = len(g[0])
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0:
                return False
    return True


def _separate(rect, others):
    r1, c1, r2, c2 = rect
    for a1, b1, a2, b2 in others:
        if not (r2 + 1 < a1 or a2 + 1 < r1 or c2 + 1 < b1 or b2 + 1 < c1):
            return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
        n_pairs = ctx.draw_int("n_pairs", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 15, 21)
        w = ctx.draw_int("grid_w", 15, 21)
        n_pairs = ctx.draw_int("n_pairs", 3, 5)
    else:
        h = ctx.draw_int("grid_h", 10, 15)
        w = ctx.draw_int("grid_w", 10, 15)
        n_pairs = ctx.draw_int("n_pairs", 2, 3)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    colors = list(range(1, 10))
    rng.shuffle(colors)
    placed = 0
    rects: list[tuple[int, int, int, int]] = []
    for color in colors:
        if placed >= n_pairs:
            break
        for _ in range(100):
            r1 = rng.randint(0, h - 4)
            c1 = rng.randint(0, w - 4)
            r2 = rng.randint(r1 + 2, min(h - 1, r1 + 5))
            c2 = rng.randint(c1 + 2, min(w - 1, c1 + 5))
            rect = (r1, c1, r2, c2)
            if _free(g, r1, c1, r2, c2) and _separate(rect, rects):
                g[r1][c1] = color
                g[r2][c2] = color
                rects.append(rect)
                placed += 1
                break
    if placed == 0:
        g[1][1] = 1
        g[4][5] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Empty grid — rule has no corner pairs to expand.
        return g
    if name == "single_marker":
        # Color appears once — rule's "two corners → rectangle"
        # precondition fails.
        g[3][3] = 4
        return g
    if name == "collinear_markers":
        # Two same-color markers on the same row (collinear) —
        # rule's "non-degenerate rectangle" condition fails;
        # rectangle has zero height.
        g[3][2] = 4; g[3][7] = 4
        return g
    return g
