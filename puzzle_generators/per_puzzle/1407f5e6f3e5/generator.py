"""Generator for arc_puzzle_bank_sixteenth_21_bundle:easy_111_fill_component_bounding_boxes.

Combinatorial axes (8): grid_h, grid_w, palette_kind, components,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_solid, single_component, no_components.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1407f5e6f3e5"
VERSION = "1.1.0"
TASK_ID = "1407f5e6f3e5"
SUMMARY = "Sparse L-shaped components expand to their solid bounding boxes."

INVARIANTS = [
    "background is 0",
    "each component is one color and 4-connected",
    "components are separated by background",
    "each component's bounding box contains at least one hole",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_solid", "single_component", "no_components")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..20"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "5..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "components":     {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r0, c0, shape):
    h, w = len(g), len(g[0])
    for dr, dc in shape:
        r, c = r0 + dr, c0 + dc
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
        target = ctx.draw_int("components", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        target = ctx.draw_int("components", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 13)
        target = ctx.draw_int("components", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shapes = [
        [(0, 0), (1, 0), (2, 0), (2, 1)],
        [(0, 0), (0, 1), (1, 0), (2, 0)],
        [(0, 0), (0, 1), (0, 2), (1, 0)],
        [(0, 2), (1, 2), (2, 2), (2, 1)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
    ]
    placed = 0
    for _ in range(500):
        if placed >= target:
            break
        shape = rng.choice(shapes)
        max_r = max(r for r, _ in shape)
        max_c = max(c for _, c in shape)
        r0 = rng.randint(0, h - max_r - 1)
        c0 = rng.randint(0, w - max_c - 1)
        if not _free(g, r0, c0, shape):
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "all_solid":
        # all components already solid rectangles → bbox-fill = identity
        for r in range(2, 4):
            for c in range(2, 4):
                g[r][c] = 4
        for r in range(6, 8):
            for c in range(7, 10):
                g[r][c] = 6
        return g
    if name == "single_component":
        # one partial-bbox component → no comparison, rule still applies trivially
        for r, c in [(3, 3), (4, 3), (5, 3), (5, 4)]:
            g[r][c] = 5
        return g
    if name == "no_components":
        # empty grid → no objects to bbox-fill
        return g
    return g
