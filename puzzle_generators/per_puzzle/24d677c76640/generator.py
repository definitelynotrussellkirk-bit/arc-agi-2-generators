"""Generator for arc_puzzle_bank_21_set10_s:S10_E4 — Move shape's bbox-corner to anchor.

Rule: anchor is the 1-cell. Shape (non-0, non-1 cells) moves so its
bbox top-left aligns with the anchor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape_id,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, no_shape, anchor_inside_shape.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "24d677c76640"
VERSION = "1.1.0"
TASK_ID = "24d677c76640"
SUMMARY = "Anchor cell (color 1) + small connected shape of one non-1 color."

INVARIANTS = [
    "exactly one 1-cell (anchor)",
    "exactly one connected shape of cells in a single non-1 color",
    "anchor is below-and-right of the shape so the moved shape stays in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "no_shape", "anchor_inside_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_id":       {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "shape_upper_left_anchor_below_right",
                       "valid": "shape_upper_left_anchor_below_right"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

SHAPES = [
    [(0, 0), (1, 0), (1, 1)],         # L
    [(0, 0), (0, 1), (1, 0)],         # corner
    [(0, 0), (0, 1), (1, 1)],         # corner-right
    [(0, 0), (0, 1), (1, 1), (1, 2)],  # zigzag
    [(0, 0), (1, 0), (2, 0)],         # vbar
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 9)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    shape = rng.choice(SHAPES)
    color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    sh = max(r for r, c in shape) + 1
    sw = max(c for r, c in shape) + 1
    # Place shape in upper-left half
    r0 = rng.randint(0, max(0, h // 2 - sh))
    c0 = rng.randint(0, max(0, w // 2 - sw))
    for dr, dc in shape:
        g[r0 + dr][c0 + dc] = color
    # Anchor below-and-right
    for _ in range(40):
        ar = rng.randint(r0 + sh, h - sh)
        ac = rng.randint(c0 + sw, w - sw)
        if g[ar][ac] == 0:
            g[ar][ac] = 1
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # shape but no 1-anchor → no destination, no move
        for dr, dc in SHAPES[0]: g[1 + dr][1 + dc] = 4
        return g
    if name == "no_shape":
        # anchor only → nothing to move
        g[5][6] = 1
        return g
    if name == "anchor_inside_shape":
        # anchor overlaps the shape → ambiguous source/dest
        for dr, dc in SHAPES[0]: g[1 + dr][1 + dc] = 4
        g[1][1] = 1  # overwrite a shape cell
        return g
    return g
