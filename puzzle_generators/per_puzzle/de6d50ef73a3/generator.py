"""Generator for arc_puzzle_bank_tenth_21_bundle:easy_67_move_cropped_object_to_top_left.

Rule: a nonzero object is tightly cropped and pasted at the top-left of
the original-size canvas.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape_choice,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: object_at_top_left, multi_object, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "de6d50ef73a3"
VERSION = "1.1.0"
TASK_ID = "de6d50ef73a3"
SUMMARY = "A nonzero object is tightly cropped and pasted at the top-left."

INVARIANTS = [
    "background is 0",
    "all nonzero cells form one compact object",
    "object starts away from the top-left corner",
    "output keeps the original canvas size",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("object_at_top_left", "multi_object", "single_cell")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..18"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "5..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_choice":   {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "single_offset_object",
                       "valid": "single_offset_object"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 13)
    rng = ctx.draw_rng("layout")
    shape = rng.choice([
        [(0, 0), (0, 1), (1, 0), (2, 0)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
        [(0, 1), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
    ])
    r0 = rng.randint(1, h - max(r for r, _ in shape) - 1)
    c0 = rng.randint(1, w - max(c for _, c in shape) - 1)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    g = full_grid(h, w, 0)
    for dr, dc in shape:
        g[r0 + dr][c0 + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "object_at_top_left":
        # object already at (0,0) → rule has no movement (input == output)
        g[0][0] = 4; g[0][1] = 4; g[1][0] = 4; g[2][0] = 4
        return g
    if name == "multi_object":
        # multiple disconnected objects → "the object" is ambiguous
        g[1][3] = 4; g[1][4] = 4; g[2][3] = 4
        g[5][7] = 6; g[5][8] = 6; g[6][8] = 6
        return g
    if name == "single_cell":
        # single-cell object → cropped bbox is 1x1, "moves" to (0,0) trivially
        g[3][5] = 4
        return g
    return g
