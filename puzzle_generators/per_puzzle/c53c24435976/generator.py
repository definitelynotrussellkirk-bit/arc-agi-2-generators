"""Generator for arc_additional_puzzles_21_set12_bundle:E81 — Apply rotation/flip code to bbox-cropped content.

Rule: code at (0,0) ∈ 1..4 selects: 1=cw, 2=180, 3=lr, 4=ud (else
ud). After ignoring (0,0), bbox-crop the rest then apply.

Combinatorial axes (8): grid_h, grid_w, palette_kind, code,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_code, code_out_of_range, symmetric_shape.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "c53c24435976"
VERSION = "1.1.0"
TASK_ID = "c53c24435976"
SUMMARY = "Code at (0,0) ∈ 1..4 + asymmetric shape elsewhere."

INVARIANTS = [
    "(0,0) ∈ 1..4",
    "asymmetric shape (so each transform produces a different output)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_code", "code_out_of_range", "symmetric_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "code":           {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "code_at_origin_with_asym_shape",
                       "valid": "code_at_origin_with_asym_shape"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        w = ctx.draw_int("grid_w", 8, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[0][0] = rng.randint(1, 4)
    shapes = [
        [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],
        [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0), (2, 1), (1, 2)],
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
        # (0,0) is 0 → no transform code, rule has no operation defined
        s = [(0, 0), (1, 0), (1, 1), (2, 1)]
        paint_at(g, 3, 3, s, 4)
        return g
    if name == "code_out_of_range":
        # code = 5 (outside 1..4) → falls through to ud default (rule docs say "else ud")
        g[0][0] = 5
        s = [(0, 0), (1, 0), (1, 1), (2, 1)]
        paint_at(g, 3, 3, s, 4)
        return g
    if name == "symmetric_shape":
        # symmetric shape (4-fold) → all 4 transforms produce the same output (no signal)
        g[0][0] = 1
        s = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]   # plus (4-fold sym)
        paint_at(g, 3, 3, s, 4)
        return g
    return g
