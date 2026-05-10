"""Generator for arc_additional_puzzles_21_set4:H22 — Pack recolored copies of mask.

Rule: row 0 has color palette. Below, a 1-shape defines the mask.
Output: copies of mask in each palette color, packed side-by-side.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_palette,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_palette, no_mask, mask_uses_palette_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "865e48425b05"
VERSION = "1.1.0"
TASK_ID = "865e48425b05"
SUMMARY = "Top row with 2-3 palette colors at distinct cols + 1-shape (3-4 cells) below."

INVARIANTS = [
    "row 0: 2-3 distinct non-zero non-1 colors",
    "below row 0: a 1-shape with 3-5 cells (3x3 bbox max)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_palette", "no_mask", "mask_uses_palette_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..10"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_palette":      {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "row0_palette_plus_mask",
                       "valid": "row0_palette_plus_mask"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

SHAPES = [
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], rng.randint(2, 3))
    cols = sorted(rng.sample(range(w), len(palette)))
    for c, color in zip(cols, palette):
        g[0][c] = color
    shape = rng.choice(SHAPES)
    sh = max(r for r, c in shape) + 1
    sw = max(c for r, c in shape) + 1
    r0 = rng.randint(2, h - sh - 1); c0 = rng.randint(0, w - sw)
    for dr, dc in shape:
        g[r0 + dr][c0 + dc] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_palette":
        # mask alone, no palette → no colors to recolor copies into
        for dr, dc in SHAPES[0]:
            g[3 + dr][2 + dc] = 1
        return g
    if name == "no_mask":
        # palette alone, no 1-shape mask → nothing to copy
        for c, color in zip([1, 4, 7], [4, 6, 7]):
            g[0][c] = color
        return g
    if name == "mask_uses_palette_color":
        # mask drawn with a palette color (not 1) → "1-shape" precondition fails
        for c, color in zip([1, 4, 7], [4, 6, 7]):
            g[0][c] = color
        for dr, dc in SHAPES[0]:
            g[3 + dr][2 + dc] = 4  # uses palette color, not 1
        return g
    return g
