"""Generator for next_b:m12 — reflect left objects across center axis.

Rule: all non-bg cells live in the left half. Output is the input plus
the LR-mirror of those cells in the right half, painted in color 7.

Combinatorial axes (8): grid_h, half_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_left, right_half_filled, on_center_axis.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8eeb98656c43"
VERSION = "1.1.0"
TASK_ID = "8eeb98656c43"
SUMMARY = "2-4 small color-2 shapes in the left half of the grid."

INVARIANTS = [
    "background is 0",
    "grid width is odd; center column is empty",
    "all non-bg cells live in cols 0..(w//2 - 1) and use color 2",
    "their LR mirror would land entirely in cols (w//2+1)..(w-1)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_left", "right_half_filled", "on_center_axis")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "half_w":         {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "left_half",
                       "valid": "left_half"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (0, 1)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        half = ctx.draw_int("half_w", 4, 5)
        n_objects = ctx.draw_int("n_objects", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        half = ctx.draw_int("half_w", 5, 6)
        n_objects = ctx.draw_int("n_objects", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        half = ctx.draw_int("half_w", 4, 6)
        n_objects = ctx.draw_int("n_objects", 2, 4)
    rng = ctx.draw_rng("layout")
    w = half * 2 + 1
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    for _ in range(n_objects):
        for _ in range(40):
            shape = rng.choice(_SHAPES)
            sh = max(r for r, _ in shape) + 1
            sw = max(c for _, c in shape) + 1
            r0 = rng.randint(0, h - sh)
            c0 = rng.randint(0, half - sw)
            cells = [(r0 + dr, c0 + dc) for dr, dc in shape]
            bad = any(p in used for p in cells)
            if bad: continue
            for r, c in cells: g[r][c] = 2
            for r, c in cells:
                for rr in range(max(0, r - 1), min(h, r + 2)):
                    for cc in range(max(0, c - 1), min(w, c + 2)):
                        used.add((rr, cc))
            break
    return g


def _draw_from_degenerate(name, rng):
    h = 9
    half = 5
    w = half * 2 + 1   # 11
    g = full_grid(h, w, 0)
    if name == "empty_left":
        # blank left half → mirror has nothing to paint, output equals input
        return g
    if name == "right_half_filled":
        # cells live on the right half (predicate violated) → mirror would land in left,
        # contradicting the rule's "left → right" assumption
        g[2][7] = 2; g[2][8] = 2
        g[5][9] = 2; g[6][9] = 2
        return g
    if name == "on_center_axis":
        # cells on the center column (col w//2) → mirror lands on themselves; no expansion
        cc = w // 2
        g[2][cc] = 2; g[4][cc] = 2; g[6][cc] = 2
        return g
    return g
