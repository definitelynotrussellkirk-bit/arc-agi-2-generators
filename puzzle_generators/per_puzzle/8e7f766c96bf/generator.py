"""Generator for arc_additional_puzzle_bank_volume23:E161 — fill 4x4 blue squares with red.

Rule: side-4 hollow blue squares have their interiors filled red.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_squares,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_squares, solid_squares, interiors_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect_outline, full_grid

GENERATOR_ID = "8e7f766c96bf"
VERSION = "1.1.0"
TASK_ID = "8e7f766c96bf"
SUMMARY = "Side-4 hollow blue squares have their interiors filled red."

INVARIANTS = [
    "background is 0",
    "selected blue objects are exact 4x4 hollow square frames",
    "interior cells of selected frames start empty",
    "frames are separated by background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_squares", "solid_squares", "interiors_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "6..22"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "6..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_squares":      {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "spaced_4x4_blue_squares",
                       "valid": "spaced_4x4_blue_squares"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
        n_squares = ctx.draw_int("n_squares", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 13, 14)
        n_squares = ctx.draw_int("n_squares", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 10, 14)
        n_squares = ctx.draw_int("n_squares", 1, 3)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    anchors: list[tuple[int, int]] = []
    for _ in range(200):
        if len(anchors) >= n_squares:
            break
        r = rng.randint(0, h - 4)
        c = rng.randint(0, w - 4)
        if any(abs(r - rr) < 5 and abs(c - cc) < 5 for rr, cc in anchors):
            continue
        draw_rect_outline(g, r, c, 4, 4, 1)
        anchors.append((r, c))
    if not anchors:
        draw_rect_outline(g, 1, 1, 4, 4, 1)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "no_squares":
        # blank → no squares to fill
        return g
    if name == "solid_squares":
        # solid 4x4 blue squares (no hollow center) → no interior to fill
        for r in range(4):
            for c in range(4): g[1 + r][1 + c] = 1
        return g
    if name == "interiors_already_filled":
        # 4x4 blue ring with interior already non-bg → fill precondition fails
        draw_rect_outline(g, 1, 1, 4, 4, 1)
        for r in range(2, 4):
            for c in range(2, 4): g[r][c] = 6
        return g
    return g
