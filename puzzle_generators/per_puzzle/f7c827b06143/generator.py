"""Generator for arc_additional_puzzles_21_set6:E37 — Fill 2x2 windows with 3 same.

Rule: iterate; whenever a 2x2 window has exactly 3 same non-zero and 1
zero, fill the zero with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shapes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_l, full_2x2, length_2_l.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f7c827b06143"
VERSION = "1.1.0"
TASK_ID = "f7c827b06143"
SUMMARY = "2-3 L-shaped 3-cell groups of distinct colors, well separated."

INVARIANTS = [
    "2-3 L-shapes (3 cells of the same color forming an L)",
    "each L's missing 4th cell is 0 (the corner to fill)",
    "shapes are well-separated (≥2 cells apart)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_l", "full_2x2", "length_2_l")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shapes":       {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "separated_l_triominoes",
                       "valid": "separated_l_triominoes"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

LSHAPES = [
    [(0, 0), (0, 1), (1, 0)],   # L-tl
    [(0, 0), (0, 1), (1, 1)],   # L-tr
    [(0, 1), (1, 0), (1, 1)],   # L-bl
    [(0, 0), (1, 0), (1, 1)],   # L-br
]


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
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_shapes = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_shapes)
    placed = []
    for color in palette:
        for _ in range(40):
            shape = rng.choice(LSHAPES)
            r0 = rng.randint(0, h - 2); c0 = rng.randint(0, w - 2)
            if any(abs(r0 - pr) < 4 and abs(c0 - pc) < 4 for pr, pc in placed):
                continue
            for dr, dc in shape:
                g[r0 + dr][c0 + dc] = color
            placed.append((r0, c0))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_l":
        # blank → no L-shapes to complete
        return g
    if name == "full_2x2":
        # 2x2 already complete → no missing 4th to fill
        for dr in range(2):
            for dc in range(2):
                g[2 + dr][2 + dc] = 4
        return g
    if name == "length_2_l":
        # 2-cell groups → not 3-of-4, rule won't fire
        for r, c in [(1, 1), (1, 2)]: g[r][c] = 4
        for r, c in [(5, 5), (6, 5)]: g[r][c] = 6
        return g
    return g
