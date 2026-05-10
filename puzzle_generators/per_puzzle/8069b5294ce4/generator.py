"""Generator for arc_puzzle_bank_21_set12_s:S12_H7 — input has a mode-color cross
(one row + one col uniform with a "central" color cc) dividing the
grid into 4 quadrants. Each quadrant has one small colored shape.
Rule outputs a 6x6 grid with each quadrant's shape placed in its
matching 3x3 sub-grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_cross (no full mode-color row+col → rule's quadrant
splitter has no axes); missing_quadrant_shape (one of 4 quadrants
empty → rule's 6x6 packer has nothing for that slot); cross_at_edge
(cross row/col is on grid edge → 4 quadrants degenerate to 2 or
fewer regions).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8069b5294ce4"
VERSION = "1.1.0"
TASK_ID = "8069b5294ce4"
SUMMARY = "Mode-color cross + 4 quadrant shapes; rule outputs 6x6 quadrant grid."

INVARIANTS = [
    "one mode-color row (>= w/2 of cc) + one mode-color col (>= h/2 of cc)",
    "exactly 4 non-bg, non-cc shapes, one per quadrant",
    "each shape's bbox fits in 3x3",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cross", "missing_quadrant_shape", "cross_at_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "grid_w":            {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 5..5", "valid": "5..5"},
    "position_bias":     {"type": "str", "default": "cross_with_quadrant_shapes",
                          "valid": "cross_with_quadrant_shapes"},
    "n_distinct_colors": {"type": "int", "default": "rng 5..5", "valid": "5..5"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 11, 15)
        w = ctx.draw_int("grid_w", 11, 15)
    rng = ctx.draw_rng("placement")
    palette = ctx.draw_distinct_colors("palette", n=5, exclude={0})
    cc = palette[0]
    shape_palette = palette[1:]

    g = full_grid(h, w, 0)
    cr = rng.randint(h // 3, 2 * h // 3)
    cl = rng.randint(w // 3, 2 * w // 3)
    for c in range(w):
        g[cr][c] = cc
    for r in range(h):
        g[r][cl] = cc

    quadrants = [
        (0, cr - 1, 0, cl - 1),
        (0, cr - 1, cl + 1, w - 1),
        (cr + 1, h - 1, 0, cl - 1),
        (cr + 1, h - 1, cl + 1, w - 1),
    ]
    for i, (rmin, rmax, cmin, cmax) in enumerate(quadrants):
        if rmax - rmin < 2 or cmax - cmin < 2:
            return [[0]]
        sh = rng.randint(2, min(3, rmax - rmin))
        sw = rng.randint(2, min(3, cmax - cmin))
        rr = rng.randint(rmin, rmax - sh + 1)
        rcc = rng.randint(cmin, cmax - sw + 1)
        for dr in range(sh):
            for dc in range(sw):
                if rng.random() < 0.6:
                    g[rr + dr][rcc + dc] = shape_palette[i]
        g[rr][rcc] = shape_palette[i]
        g[rr + sh - 1][rcc + sw - 1] = shape_palette[i]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_cross":
        # No mode-color row+col — rule's quadrant splitter has no axes.
        for dr in range(2):
            for dc in range(2):
                g[1 + dr][1 + dc] = 1
                g[1 + dr][9 + dc] = 2
                g[9 + dr][1 + dc] = 3
                g[9 + dr][9 + dc] = 4
        return g
    if name == "missing_quadrant_shape":
        # Cross present but bottom-right quadrant has no shape.
        for c in range(w):
            g[5][c] = 8
        for r in range(h):
            g[r][5] = 8
        for dr in range(2):
            for dc in range(2):
                g[1 + dr][1 + dc] = 1
                g[1 + dr][8 + dc] = 2
                g[8 + dr][1 + dc] = 3
        return g
    if name == "cross_at_edge":
        # Cross on grid edge — 4 quadrants degenerate.
        for c in range(w):
            g[0][c] = 8
        for r in range(h):
            g[r][0] = 8
        for dr in range(2):
            for dc in range(2):
                g[3 + dr][3 + dc] = 1
                g[3 + dr][8 + dc] = 2
                g[8 + dr][3 + dc] = 3
                g[8 + dr][8 + dc] = 4
        return g
    return g
