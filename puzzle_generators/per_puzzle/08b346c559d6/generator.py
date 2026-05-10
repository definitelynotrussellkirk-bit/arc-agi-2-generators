"""Generator for arc_puzzle_bank_21_set9_e:easy_i07.

Rule: copy upper half into lower half by vertical mirroring.

Combinatorial axes (8): grid_h, grid_w, palette_kind, top_marks,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_top, top_already_mirrors_bottom, odd_height.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "08b346c559d6"
VERSION = "1.1.0"
TASK_ID = "08b346c559d6"
SUMMARY = "Copy the upper half into the lower half by vertical mirroring."

INVARIANTS = [
    "background is 0",
    "height is even",
    "upper half is the source pattern",
    "lower half may contain distractors that are overwritten",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_top", "top_already_mirrors_bottom", "odd_height")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng even 6..8", "valid": "4..14 even"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "top_marks":      {"type": "int", "default": "rng 3..6", "valid": "1..20"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "top_half", "valid": "top_half"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 6, 7)
        marks = ctx.draw_int("top_marks", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        marks = ctx.draw_int("top_marks", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 6, 9)
        marks = ctx.draw_int("top_marks", 3, 6)
    if h % 2:
        h += 1
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    half = h // 2
    top_cells = [(r, c) for r in range(half) for c in range(w)]
    for r, c in rng.sample(top_cells, min(marks, len(top_cells))):
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    for r in range(half, h):
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        if rng.random() < 0.75:
            g[r] = [color for _ in range(w)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 7
    g = full_grid(h, w, 0)
    if name == "empty_top":
        # top half empty → mirror copy is all zeros, no information transmitted
        for c in range(w):
            g[3][c] = 4
            g[5][c] = 4
        return g
    if name == "top_already_mirrors_bottom":
        # top and bottom already match → rule is identity, output = input
        for r, c in [(0, 1), (1, 3)]:
            g[r][c] = 5
        for r, c in [(5, 1), (4, 3)]:
            g[r][c] = 5
        return g
    if name == "odd_height":
        # odd-height grid breaks "even h" invariant, midline is ambiguous
        odd = full_grid(7, w, 0)
        for r, c, v in [(0, 1, 4), (1, 3, 5), (2, 5, 6)]:
            odd[r][c] = v
        return odd
    return g
