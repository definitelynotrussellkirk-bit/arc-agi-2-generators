"""Generator for 21b:m141 — select legend object and rotate clockwise.

Rule: a single legend cell at (0,0) names a target color. Among the
multi-cell shapes, the one matching that color gets cropped and
rotated 90° clockwise. Output is the rotated shape.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_matching_shape, symmetric_shape.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0cb23f5660c9"
VERSION = "1.1.0"
TASK_ID = "0cb23f5660c9"
SUMMARY = "Legend cell (0,0) names a color; that-colored shape gets rotated CW."

INVARIANTS = [
    "background is 0",
    "legend cell at (0,0) is a non-bg color C",
    "exactly 3 multi-cell shapes elsewhere; one is color C",
    "the C-shape's CW rotation differs from itself (so output isn't degenerate)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_matching_shape", "symmetric_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "legend_with_shapes",
                       "valid": "legend_with_shapes"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 0)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _place(g, rng, shape, color):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(40):
        r0 = rng.randint(1, h - sh); c0 = rng.randint(1, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 16)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 3)
    legend_color = palette[0]
    g[0][0] = legend_color
    for color in palette:
        _place(g, rng, rng.choice(_SHAPES), color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # Shapes but (0,0) empty — rule's color-selector has no
        # input.
        for r, c in [(3, 3), (3, 4), (3, 5), (4, 4)]: g[r][c] = 4
        for r, c in [(7, 8), (8, 8), (8, 9)]: g[r][c] = 6
        return g
    if name == "no_matching_shape":
        # Legend names a color absent from body shapes — rule's
        # selector finds nothing.
        g[0][0] = 7
        for r, c in [(3, 3), (3, 4), (4, 3)]: g[r][c] = 4
        for r, c in [(7, 8), (8, 8), (8, 9)]: g[r][c] = 6
        return g
    if name == "symmetric_shape":
        # The selected shape is rotation-invariant — rule's CW
        # rotation produces the same shape; rule's effect invisible.
        g[0][0] = 4
        for r in range(3, 5):
            for c in range(3, 5): g[r][c] = 4
        for r, c in [(7, 8), (8, 8), (8, 9)]: g[r][c] = 6
        return g
    return g
