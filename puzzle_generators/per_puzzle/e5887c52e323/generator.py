"""Generator for arc_additional_puzzle_bank_volume16:E106.

The elbow cell of each red L-triomino is recolored yellow.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_l_shapes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_l, full_squares, length_4_l.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e5887c52e323"
VERSION = "1.1.0"
TASK_ID = "e5887c52e323"
SUMMARY = "The elbow cell of each red L-triomino is recolored yellow."

INVARIANTS = [
    "background is 0",
    "target red components are exact 3-cell L shapes",
    "L shapes are separated so each remains one component",
    "all four missing-corner orientations may occur",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_l", "full_squares", "length_4_l")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "4..18"},
    "grid_w":         {"type": "int", "default": "rng 7..12", "valid": "4..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_l_shapes":     {"type": "int", "default": "rng 2..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "separated_l_triominoes",
                       "valid": "separated_l_triominoes"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        n_l_shapes = ctx.draw_int("n_l_shapes", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 10, 12)
        n_l_shapes = ctx.draw_int("n_l_shapes", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 7, 12)
        n_l_shapes = ctx.draw_int("n_l_shapes", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    corners = [(0, 0), (0, 1), (1, 0), (1, 1)]
    anchors: list[tuple[int, int]] = []
    for _ in range(220):
        if len(anchors) >= n_l_shapes:
            break
        r = rng.randint(0, h - 2)
        c = rng.randint(0, w - 2)
        if any(abs(r - rr) < 3 and abs(c - cc) < 3 for rr, cc in anchors):
            continue
        missing = rng.choice(corners)
        for dr, dc in corners:
            if (dr, dc) != missing:
                g[r + dr][c + dc] = 2
        anchors.append((r, c))
    if not anchors:
        g[1][1] = 2
        g[1][2] = 2
        g[2][1] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_l":
        # blank → no L-triominoes, no elbows to recolor
        return g
    if name == "full_squares":
        # 2x2 fully filled → no elbow (rule's "L-triomino" precondition fails)
        for dr in range(2):
            for dc in range(2):
                g[1 + dr][1 + dc] = 2
        return g
    if name == "length_4_l":
        # 4-cell L → not a 3-cell L-triomino, rule won't fire
        for r, c in [(1, 1), (1, 2), (2, 1), (3, 1)]:
            g[r][c] = 2
        return g
    return g
