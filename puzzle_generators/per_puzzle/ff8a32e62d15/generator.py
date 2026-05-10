"""Generator for arc_puzzle_bank_sixth_21_bundle:easy_37_replace_components_by_bboxes.

Rule: each component replaced by a cyan bbox-border outline.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_components, only_singletons, only_2x2.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ff8a32e62d15"
VERSION = "1.1.0"
TASK_ID = "ff8a32e62d15"

SUMMARY = "Separated components are replaced by cyan bounding-box borders."

INVARIANTS = [
    "background is 0",
    "components are 4-connected",
    "components are separated by at least one background cell",
    "output ignores original colors and uses 8 for bbox borders",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "only_singletons", "only_2x2")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..20"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..20"},
    "components":     {"type": "int", "default": "rng 3..5", "valid": "1..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_components",
                       "valid": "scattered_components"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..9"},
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
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("components", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 16)
        w = ctx.draw_int("grid_w", 11, 16)
        target = ctx.draw_int("components", 5, 8)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
        target = ctx.draw_int("components", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shapes = [
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (1, 0), (2, 0), (2, 1)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 1), (1, 0), (1, 1), (1, 2)],
    ]
    placed = 0
    for _ in range(500):
        if placed >= target:
            break
        shape = rng.choice(shapes)
        r0 = rng.randint(0, h - max(r for r, _ in shape) - 1)
        c0 = rng.randint(0, w - max(c for _, c in shape) - 1)
        if not _free(g, r0, c0, shape):
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_components":
        # Empty grid — rule has no components to bbox.
        return g
    if name == "only_singletons":
        # All 1x1 components — rule's bbox-border for a 1-cell
        # component is the cell itself; replacing color → 8 makes
        # the rule a recolor with no shape change.
        g[2][2] = 4; g[2][7] = 6; g[6][3] = 7; g[7][8] = 3
        return g
    if name == "only_2x2":
        # All 2x2 solid components — rule's bbox-border has no
        # interior; rule's "border replaces component" does not
        # introduce any zero cells.
        for r in range(2, 4):
            for c in range(2, 4): g[r][c] = 4
        for r in range(6, 8):
            for c in range(7, 9): g[r][c] = 6
        return g
    return g
