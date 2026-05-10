"""Generator for arc_puzzle_bank_21_set12_s:S12_H4 — quadrant-cross packs into 6x6 grid.

Input has a mode-color cross (one row + one col uniform with a
"central" color cc) dividing the grid into 4 quadrants. Each quadrant
has one small colored shape. Rule outputs a 6x6 grid with each
quadrant's shape placed in its matching 3x3 sub-grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_cross (no full row/col of mode color → rule's quadrant
divider is undefined), missing_quadrant_shape (one of 4 quadrants
has no shape → rule's 6x6 packing has an empty slot), shapes_too_large
(quadrant shape's bbox exceeds 3x3 → rule's "place in 3x3 sub-grid"
truncates).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c4e70c48d698"
VERSION = "1.1.0"
TASK_ID = "c4e70c48d698"
SUMMARY = "Mode-color cross + 4 quadrant shapes; rule outputs 6x6 quadrant grid."

INVARIANTS = [
    "one mode-color row (>= w/2 of cc) + one mode-color col (>= h/2 of cc)",
    "exactly 4 non-bg, non-cc shapes, one per quadrant",
    "each shape's bbox fits in 3x3",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cross", "missing_quadrant_shape", "shapes_too_large")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "grid_w":            {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 5..5", "valid": "5..5"},
    "position_bias":     {"type": "str", "default": "cross_plus_4_quadrant_shapes",
                          "valid": "cross_plus_4_quadrant_shapes"},
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
    h, w = 13, 13
    g = full_grid(h, w, 0)
    if name == "no_cross":
        # No full row/col of mode color — rule's quadrant divider undefined.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (0, 1)]:
            g[2 + dr][9 + dc] = 6
        for dr, dc in [(0, 0), (1, 0)]:
            g[8 + dr][2 + dc] = 7
        for dr, dc in [(0, 0), (1, 1)]:
            g[8 + dr][9 + dc] = 8
        return g
    if name == "missing_quadrant_shape":
        # Cross present but one quadrant has no shape — 6x6 packing
        # has an empty slot.
        for c in range(w): g[6][c] = 5
        for r in range(h): g[r][6] = 5
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (1, 0)]:
            g[2 + dr][9 + dc] = 6
        # 3rd quadrant skipped
        for dr, dc in [(0, 0), (1, 1)]:
            g[9 + dr][9 + dc] = 8
        return g
    if name == "shapes_too_large":
        # Quadrant shape exceeds 3x3 — rule truncates.
        for c in range(w): g[6][c] = 5
        for r in range(h): g[r][6] = 5
        # 4x4 shape in top-left
        for dr in range(4):
            for dc in range(4):
                g[1 + dr][1 + dc] = 4
        for dr, dc in [(0, 0), (1, 0)]:
            g[2 + dr][9 + dc] = 6
        for dr, dc in [(0, 0), (0, 1)]:
            g[8 + dr][2 + dc] = 7
        for dr, dc in [(0, 0), (1, 1)]:
            g[9 + dr][9 + dc] = 8
        return g
    return g
