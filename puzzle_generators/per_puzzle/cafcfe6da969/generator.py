"""Generator for arc_additional_puzzle_bank_volume11:E71.

Red T-tetrominoes are replaced by filled green bounding rectangles.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_t_shapes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_t_shapes, wrong_shape, t_at_border.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cafcfe6da969"
VERSION = "1.1.0"
TASK_ID = "cafcfe6da969"
SUMMARY = "Red T-tetrominoes are replaced by filled green bounding rectangles."

INVARIANTS = [
    "background is 0",
    "target red components are exact T-tetrominoes",
    "T shapes can appear in any of four orientations",
    "target components are separated so they remain distinct",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_t_shapes", "wrong_shape", "t_at_border")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_t_shapes":     {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "red_t_tetrominoes",
                       "valid": "red_t_tetrominoes"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


T_SHAPES = [
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(1, 0), (1, 1), (1, 2), (0, 1)],
    [(0, 0), (1, 0), (2, 0), (1, 1)],
    [(0, 1), (1, 1), (2, 1), (1, 0)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_t_shapes = ctx.draw_int("n_t_shapes", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
        n_t_shapes = ctx.draw_int("n_t_shapes", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
        n_t_shapes = ctx.draw_int("n_t_shapes", 2, 4)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    anchors: list[tuple[int, int]] = []
    for _ in range(220):
        if len(anchors) >= n_t_shapes:
            break
        shape = rng.choice(T_SHAPES)
        sh = max(r for r, _ in shape) + 1
        sw = max(c for _, c in shape) + 1
        r = rng.randint(0, h - sh)
        c = rng.randint(0, w - sw)
        if any(abs(r - rr) < 4 and abs(c - cc) < 4 for rr, cc in anchors):
            continue
        for dr, dc in shape:
            g[r + dr][c + dc] = 2
        anchors.append((r, c))
    if not anchors:
        for dr, dc in T_SHAPES[0]:
            g[1 + dr][1 + dc] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_t_shapes":
        # blank → no T-tetrominoes to replace
        return g
    if name == "wrong_shape":
        # red components are not T (e.g., L-shape, square) → rule precondition fails
        # L-tetromino:
        for dr, dc in [(0, 0), (1, 0), (2, 0), (2, 1)]: g[1 + dr][1 + dc] = 2
        # square:
        for dr in range(2):
            for dc in range(2): g[5 + dr][6 + dc] = 2
        return g
    if name == "t_at_border":
        # T-shape touches border such that bbox-fill would extend OOB? actually bbox fits
        # but we test edge case: T with cells exactly at row 0 / col 0
        for dr, dc in T_SHAPES[0]: g[0 + dr][0 + dc] = 2
        return g
    return g
