"""Generator for 0bb8deee.

Rule: mode-color cross + 4 quadrant shapes; rule outputs 6x6 quadrant
grid.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
shape_density.
Degenerates: no_cross, no_shapes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "24ef0b5ae2e1"
VERSION = "1.1.0"
TASK_ID = "24ef0b5ae2e1"
SUMMARY = "Mode-color cross + 4 quadrant shapes assembled to 6x6 quadrant grid."

INVARIANTS = [
    "one mode-color row and one mode-color col form the cross",
    "exactly four non-bg non-cc shapes one per quadrant",
    "each shape's bbox fits in 3x3",
    "shape colors are distinct from each other and from cc",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_cross", "no_shapes", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "grid_w":         {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "5", "valid": "5"},
    "shape_density":  {"type": "float", "default": "0.6", "valid": "0.5..0.8"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 11, 12
    elif difficulty == "hard":
        h_lo, h_hi = 14, 17
    else:
        h_lo, h_hi = 11, 15
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
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
    g = full_grid(13, 13, 0)
    if name == "no_cross":
        g[3][3] = 2
        return g
    if name == "no_shapes":
        for c in range(13):
            g[6][c] = 5
        for r in range(13):
            g[r][6] = 5
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 5
        return g
    return g
