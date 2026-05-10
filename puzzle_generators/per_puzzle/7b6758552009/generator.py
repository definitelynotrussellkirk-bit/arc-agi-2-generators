"""Generator for arc_puzzle_bank_seventh_21_bundle:easy_49_palette_row_left_to_right.

Rule: separated components are summarized as a one-row left-to-right palette.

Combinatorial axes (8): grid_h, grid_w, palette_kind, components,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_components, single_component, components_touching.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7b6758552009"
VERSION = "1.1.0"
TASK_ID = "7b6758552009"

SUMMARY = "Separated components are summarized as a one-row left-to-right palette."

INVARIANTS = [
    "background is 0",
    "components are 4-connected same-color blobs",
    "components are separated by background",
    "output order is by each component's leftmost column then top row",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "single_component", "components_touching")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..16"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "6..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "components":     {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_components",
                       "valid": "spaced_components"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 10, 11)
        target = ctx.draw_int("components", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 13, 14)
        target = ctx.draw_int("components", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 10, 14)
        target = ctx.draw_int("components", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shapes = [
        [(0, 0)],
        [(0, 0), (0, 1)],
        [(0, 0), (1, 0)],
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (0, 1), (1, 0), (1, 1)],
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
    h, w = 7, 12
    g = full_grid(h, w, 0)
    if name == "no_components":
        # blank → no palette to extract
        return g
    if name == "single_component":
        # one component → single-color output, weakly tests sort order
        for (r, c) in [(2, 3), (2, 4), (3, 3)]: g[r][c] = 4
        return g
    if name == "components_touching":
        # adjacent same-color cells fuse into one component, breaking expected count
        g[2][2] = 4; g[2][3] = 4; g[3][3] = 4  # 4-component
        g[3][7] = 3; g[3][8] = 3; g[4][8] = 3
        return g
    return g
