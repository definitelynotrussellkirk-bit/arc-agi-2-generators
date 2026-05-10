"""Generator for arc_puzzle_bank_sixth_21_bundle:easy_42_component_colors_by_top_order.

Rule: separated components are summarized by their colors from top to bottom.

Combinatorial axes (8): grid_h, grid_w, palette_kind, components,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_components, all_same_color, single_component.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "22398bb29643"
VERSION = "1.1.0"
TASK_ID = "22398bb29643"

SUMMARY = "Separated components are summarized by their colors from top to bottom."

INVARIANTS = [
    "background is 0",
    "components are separated by background",
    "component order is by bbox top row then left column",
    "each component contributes exactly one output color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "all_same_color", "single_component")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "5..22"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "5..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "components":     {"type": "int", "default": "rng 4..6", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_components",
                       "valid": "scattered_components"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("components", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 18)
        w = ctx.draw_int("grid_w", 12, 18)
        target = ctx.draw_int("components", 6, 9)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 12)
        target = ctx.draw_int("components", 4, 6)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shapes = [[(0, 0)], [(0, 0), (0, 1)], [(0, 0), (1, 0)], [(0, 0), (0, 1), (1, 0)]]
    placed = 0
    for _ in range(600):
        if placed >= target:
            break
        shape = rng.choice(shapes)
        r0 = rng.randint(0, h - max(r for r, _ in shape) - 1)
        c0 = rng.randint(0, w - max(c for _, c in shape) - 1)
        ok = True
        for dr, dc in shape:
            r, c = r0 + dr, c0 + dc
            for rr in range(max(0, r - 1), min(h, r + 2)):
                for cc in range(max(0, c - 1), min(w, c + 2)):
                    if g[rr][cc] != 0:
                        ok = False
        if not ok:
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_components":
        # Empty grid — rule has no colors to list.
        return g
    if name == "all_same_color":
        # All components share one color — the rule's per-component
        # color list collapses to N copies of one color.
        g[1][1] = 4; g[3][6] = 4; g[7][2] = 4; g[8][8] = 4
        return g
    if name == "single_component":
        # Just one component — the order-by-top reduces to a single
        # color, removing the multi-component evidence of the rule.
        g[3][4] = 5; g[3][5] = 5
        return g
    return g
