"""Generator for arc_puzzle_bank_21_set7_s:S7_E4.

Rule: a sparse connected color-6 component is replaced by its solid
bounding box.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_component, multiple_components, already_solid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f9cd85012aa8"
VERSION = "1.1.0"
TASK_ID = "f9cd85012aa8"
SUMMARY = "A sparse connected color-6 component is replaced by its solid bounding box."

INVARIANTS = [
    "background is 0",
    "there is exactly one connected color-6 component",
    "the component's bounding box contains holes or missing cells",
    "output fills the full bounding box with 6",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_component", "multiple_components", "already_solid")
HELPFUL_TEXTURES = PALETTE_KINDS

_SHAPES = [
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)],
]

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape":          {"type": "choice", "default": "rng connected sparse bbox",
                       "valid": "small connected stencils"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "interior_sparse",
                       "valid": "interior_sparse"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shape = rng.choice(_SHAPES)
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    r0 = rng.randint(0, h - sh)
    c0 = rng.randint(0, w - sw)
    for dr, dc in shape:
        g[r0 + dr][c0 + dc] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_component":
        # empty grid → no 6-component to fill bbox of
        return g
    if name == "multiple_components":
        # 2 disjoint 6-components → which bbox to fill is ambiguous
        for dr, dc in [(0, 0), (1, 0), (1, 1)]: g[2 + dr][2 + dc] = 6
        for dr, dc in [(0, 0), (0, 1), (1, 0)]: g[5 + dr][6 + dc] = 6
        return g
    if name == "already_solid":
        # component already fills its bbox solidly → bbox-fill is identity
        for r in range(2, 5):
            for c in range(2, 5): g[r][c] = 6
        return g
    return g
