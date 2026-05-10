"""Generator for arc_puzzle_bank_twentythird21:M156 — recolor shapes by size-rank to top-left legend.

Rule: top-left has a legend of 3 colors at row 0 cols 0-2. Body has
3 connected shapes with distinct sizes in distinct non-legend colors.
Output recolors each shape: rank-i (size ASC) becomes legend[i].
Top-left legend stays in output.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: tied_sizes (two shapes share a size → rank-by-size is
ambiguous, tie-break decides), single_shape (only one body shape →
2 of 3 legend colors are unused, output partial), no_legend (row 0
empty → rule's recolor map is undefined, all shapes become 0/error).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "28119d6d0e10"
VERSION = "1.1.0"
TASK_ID = "28119d6d0e10"
SUMMARY = "Top-left 3-color legend + 3 distinct-size shapes in distinct other colors."

INVARIANTS = [
    "background is 0",
    "row 0 cols 0-2 hold 3 distinct legend colors",
    "exactly 3 connected shapes below row 0, each in a distinct non-legend color",
    "all 3 shapes have distinct cell counts",
    "shapes don't touch each other or row 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_sizes", "single_shape", "no_legend")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "6", "valid": "6..6"},
    "position_bias":  {"type": "str", "default": "legend_plus_three_shapes",
                       "valid": "legend_plus_three_shapes"},
    "n_distinct_colors": {"type": "int", "default": "6", "valid": "6..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_BY_SIZE = {
    1: [[(0, 0)]],
    3: [[(0, 0), (1, 0), (1, 1)], [(0, 0), (0, 1), (0, 2)]],
    4: [[(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 0), (0, 1), (1, 0), (2, 0)]],
    6: [[(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]],
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 11, 14)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    legend = list(random_palette(rng, 3))
    for i, c in enumerate(legend):
        g[0][i] = c
    shape_palette = list(random_palette(rng, 3, exclude=set(legend)))
    sizes = rng.sample(list(_BY_SIZE.keys()), 3)
    placed: list[tuple[int, int, int, int]] = [(0, 0, 0, 2)]
    for size, color in zip(sizes, shape_palette):
        shape = rng.choice(_BY_SIZE[size])
        sh = max(c[0] for c in shape) + 1
        sw = max(c[1] for c in shape) + 1
        for _ in range(80):
            r0 = rng.randint(2, h - sh)
            c0 = rng.randint(0, w - sw)
            bb = (r0 - 1, c0 - 1, r0 + sh, c0 + sw)
            if any(bbox_overlaps(bb, p) for p in placed): continue
            paint_at(g, r0, c0, shape, color)
            placed.append((r0, c0, r0 + sh - 1, c0 + sw - 1))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "tied_sizes":
        # Two shapes share size 4 — rank-by-size is ambiguous;
        # tie-break decides which legend color each gets.
        for i, c in enumerate([2, 4, 6]):
            g[0][i] = c
        for dr, dc in _BY_SIZE[3][0]:
            g[3 + dr][1 + dc] = 7
        for dr, dc in _BY_SIZE[4][0]:
            g[3 + dr][5 + dc] = 8
        for dr, dc in _BY_SIZE[4][1]:
            g[5 + dr][8 + dc] = 9
        return g
    if name == "single_shape":
        # Only one body shape — 2 of 3 legend colors are unused;
        # output partial.
        for i, c in enumerate([2, 4, 6]):
            g[0][i] = c
        for dr, dc in _BY_SIZE[4][0]:
            g[3 + dr][4 + dc] = 7
        return g
    if name == "no_legend":
        # Row 0 empty — rule's recolor map is undefined; outputs
        # become 0 (or undefined behavior).
        for dr, dc in _BY_SIZE[3][0]:
            g[3 + dr][1 + dc] = 7
        for dr, dc in _BY_SIZE[4][0]:
            g[3 + dr][5 + dc] = 8
        for dr, dc in _BY_SIZE[6][0]:
            g[2 + dr][8 + dc] = 9
        return g
    return g
