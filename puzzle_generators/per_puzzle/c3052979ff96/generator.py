"""Generator for arc_additional_puzzle_bank_volume13:M86 — Rotate 8-shape around 9-pivot by code, paint as 2.

Rule: take the 8-shape; pivot at the unique 9-cell. Code cell ∈ {1..4}
selects rotation (1=identity, 2=cw, 3=180, 4=ccw). Each cell of the
8-shape rotated around the pivot is painted color 2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, code_value,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pivot, no_shape, no_code.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "c3052979ff96"
VERSION = "1.1.0"
TASK_ID = "c3052979ff96"
SUMMARY = "8-blob, single 9-pivot adjacent, code cell ∈ 1..4, plus distractor decoration."

INVARIANTS = [
    "exactly 1 cell of color 9 (pivot)",
    "exactly 1 cell with value in {1,2,3,4} (rotation code)",
    "≥3 cells of color 8 (rotated shape)",
    "rotated cells fit in grid",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pivot", "no_shape", "no_code")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "code_value":     {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "9pivot_8shape_code",
                       "valid": "9pivot_8shape_code"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    pr, pc = h // 2, w // 2
    g[pr][pc] = 9
    shapes = [
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (1, 1)],
        [(0, 0), (1, -1), (1, 0)],
    ]
    s = rng.choice(shapes)
    paint_at(g, pr, pc + 1, s, 8)
    code_r = rng.choice([0, h - 1])
    code_c = rng.randint(0, w - 1)
    g[code_r][code_c] = rng.randint(1, 4)
    decor_r = rng.choice([1, h - 2])
    decor_c = rng.randint(1, w - 2)
    if g[decor_r][decor_c] == 0:
        g[decor_r][decor_c] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "no_pivot":
        # 8-shape + code but no 9-pivot → no rotation center defined
        paint_at(g, 5, 6, [(0, 0), (0, 1), (1, 0)], 8)
        g[0][3] = 2
        return g
    if name == "no_shape":
        # 9-pivot + code but no 8-shape → nothing to rotate
        g[5][5] = 9
        g[0][3] = 2
        return g
    if name == "no_code":
        # 9-pivot + 8-shape but no code → no rotation dispatch
        g[5][5] = 9
        paint_at(g, 5, 6, [(0, 0), (0, 1), (1, 0)], 8)
        return g
    return g
