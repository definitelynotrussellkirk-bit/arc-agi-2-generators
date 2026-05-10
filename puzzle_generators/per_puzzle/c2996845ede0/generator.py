"""Generator for arc_puzzle_bank_21_set11_s:S11_M5 — Mirror largest shape.

Rule: take the largest object. Normalize. Mirror horizontally.
Union = original + mirror. Output cropped to bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_small,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_shapes, equal_size, single_shape.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c2996845ede0"
VERSION = "1.1.0"
TASK_ID = "c2996845ede0"
SUMMARY = "1 large asymmetric L-shape + 1 smaller distractor of different color."

INVARIANTS = [
    "exactly 2 objects of distinct colors",
    "one object is strictly larger (the target)",
    "objects are well-separated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_shapes", "equal_size", "single_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_small":        {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "big_left_small_right",
                       "valid": "big_left_small_right"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


SHAPES = [
    [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0), (2, 1)],   # 6-cells, asymmetric
    [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)],
    [(0, 0), (1, 0), (1, 1), (2, 0), (2, 1), (2, 2)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 9, 10)
        n_small_lo, n_small_hi = 2, 2
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 11, 12)
        n_small_lo, n_small_hi = 3, 3
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 9, 12)
        n_small_lo, n_small_hi = 2, 3
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    big_color, small_color = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 2)
    shape = rng.choice(SHAPES)
    sh = max(r for r, c in shape) + 1
    sw = max(c for r, c in shape) + 1
    # Place big in left half
    r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w // 2 - sw)
    for dr, dc in shape:
        g[r0 + dr][c0 + dc] = big_color
    # Place small (2-3 cells) in right half
    n_small = rng.randint(n_small_lo, n_small_hi)
    placed = 0
    for _ in range(40):
        if placed >= n_small:
            break
        r = rng.randint(0, h - 1); c = rng.randint(w // 2 + 1, w - 1)
        if g[r][c] == 0:
            g[r][c] = small_color
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 11
    g = full_grid(h, w, 0)
    if name == "no_shapes":
        # blank → no objects, no "largest" defined
        return g
    if name == "equal_size":
        # both objects same size → "largest" is ambiguous
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[1 + dr][1 + dc] = 4
            g[3 + dr][7 + dc] = 6
        return g
    if name == "single_shape":
        # only one shape, no distractor → no contrast for "largest" selection
        for dr, dc in SHAPES[0]:
            g[1 + dr][1 + dc] = 4
        return g
    return g
