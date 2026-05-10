"""Generator for arc_puzzle_bank_twelfth_21_bundle:easy_82_draw_object_bounding_boxes.

Rule: each monochrome object keeps its cells and gains its bounding-box border.

Combinatorial axes (8): grid_h, grid_w, palette_kind, objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects, single_cell_objects, solid_rect_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "20d2c3da584a"
VERSION = "1.1.0"
TASK_ID = "20d2c3da584a"

SUMMARY = "Each monochrome object keeps its cells and gains its bounding-box border."

INVARIANTS = [
    "background is 0",
    "each component is monochrome and connected",
    "components have nontrivial bounding boxes",
    "component bounding boxes are separated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "single_cell_objects", "solid_rect_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "5..22"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "5..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "objects":        {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_l_shapes",
                       "valid": "spaced_l_shapes"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, cells):
    h, w = len(g), len(g[0])
    for r, c in cells:
        if not (0 <= r < h and 0 <= c < w):
            return False
        for rr in range(max(0, r - 1), min(h, r + 2)):
            for cc in range(max(0, c - 1), min(w, c + 2)):
                if g[rr][cc] != 0:
                    return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("objects", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
        target = ctx.draw_int("objects", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 9, 14)
        target = ctx.draw_int("objects", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shapes = [
        [(0, 0), (1, 0), (2, 0), (2, 1)],
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 1), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ]
    placed = 0
    for _ in range(160):
        if placed >= target:
            break
        shape = rng.choice(shapes)
        r0 = rng.randint(0, h - 3)
        c0 = rng.randint(0, w - 3)
        cells = [(r0 + dr, c0 + dc) for dr, dc in shape]
        if _free(g, cells):
            color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
            for r, c in cells:
                g[r][c] = color
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # blank → no objects, rule has no bboxes to draw
        return g
    if name == "single_cell_objects":
        # 1x1 objects → bbox = single cell, rule is identity
        g[1][2] = 4
        g[5][7] = 6
        g[7][3] = 3
        return g
    if name == "solid_rect_objects":
        # solid 3x3 rectangles → bbox border = object border, rule is identity
        for r in range(3):
            for c in range(3): g[1 + r][1 + c] = 4
        for r in range(3):
            for c in range(3): g[5 + r][6 + c] = 6
        return g
    return g
