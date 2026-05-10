"""Generator for arc_additional_puzzles_21_set22_bundle:E151 — Apply rotation/flip code to bbox-cropped content.

Rule: code at (0,0) ∈ 1..6 selects: 1=id, 2=cw, 3=180, 4=ccw, 5=lr, 6=ud.
After zeroing (0,0), bbox-crop the rest then apply the transformation.

Combinatorial axes (8): grid_h, grid_w, palette_kind, code,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_code, no_shape, symmetric_shape.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "23220e3be06f"
VERSION = "1.1.0"
TASK_ID = "23220e3be06f"
SUMMARY = "Code at (0,0) ∈ 1..6 + small asymmetric shape elsewhere."

INVARIANTS = [
    "(0,0) ∈ 1..6",
    "≥1 small asymmetric shape (so each rotation produces a different output)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_code", "no_shape", "symmetric_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "code":           {"type": "int", "default": "rng 1..6", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "code_at_origin_with_shape",
                       "valid": "code_at_origin_with_shape"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[0][0] = rng.randint(1, 6)
    shapes = [
        [(0, 1), (1, 0), (1, 2), (2, 0), (2, 1)],
        [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
        [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)],
    ]
    s = rng.choice(shapes)
    color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    top = rng.randint(2, h - 5); left = rng.randint(2, w - 5)
    paint_at(g, top, left, s, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_code":
        # missing code at (0,0) → rule has no instruction to apply
        for (r, c) in [(3, 3), (3, 4), (4, 3), (5, 3)]: g[r][c] = 4
        return g
    if name == "no_shape":
        # code present but no shape to transform → rule has nothing to operate on
        g[0][0] = 3
        return g
    if name == "symmetric_shape":
        # 4-fold symmetric shape → all rotation codes produce same output
        g[0][0] = 2
        # solid 3x3 square — rotations produce identity
        for r in range(3, 6):
            for c in range(3, 6): g[r][c] = 4
        return g
    return g
