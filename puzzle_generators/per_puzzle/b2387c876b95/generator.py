"""Generator for arc_additional_puzzle_bank_volume11:M77.

A red shape is reflected across a complete gray divider row or column.

Combinatorial axes (8): grid_h, grid_w, palette_kind, orientation,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_shape, shape_on_divider.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b2387c876b95"
VERSION = "1.1.0"
TASK_ID = "b2387c876b95"
SUMMARY = "A red shape is reflected across a complete gray divider row or column."

INVARIANTS = [
    "background is 0",
    "there is exactly one full gray divider line",
    "the red source shape lies on one side of the divider",
    "the reflected destination cells are in bounds and initially blank",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_shape", "shape_on_divider")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "6..24"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "6..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "orientation":    {"type": "str", "default": "rng vertical|horizontal",
                       "valid": "vertical|horizontal"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "divider_plus_one_side_shape",
                       "valid": "divider_plus_one_side_shape"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    vertical = rng.choice([True, False])
    local = [(0, 0), (0, 1), (1, 0), (2, 0)]
    if vertical:
        d = rng.randint(3, w - 4)
        for r in range(h):
            g[r][d] = 5
        c_min = max(0, 2 * d - (w - 1))
        c = rng.randint(c_min, d - 3)
        r = rng.randint(1, h - 4)
        for dr, dc in local:
            g[r + dr][c + dc] = 2
    else:
        d = rng.randint(3, h - 4)
        for c in range(w):
            g[d][c] = 5
        r_min = max(0, 2 * d - (h - 1))
        r = rng.randint(r_min, d - 3)
        c = rng.randint(1, w - 4)
        for dr, dc in local:
            g[r + dr][c + dc] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # red shape without divider → no axis to reflect across
        for dr, dc in [(0, 0), (0, 1), (1, 0), (2, 0)]:
            g[2 + dr][1 + dc] = 2
        return g
    if name == "no_shape":
        # divider alone → nothing to reflect
        for r in range(h):
            g[r][4] = 5
        return g
    if name == "shape_on_divider":
        # red shape sits on the divider → "one side" precondition fails
        for r in range(h):
            g[r][4] = 5
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][3 + dc] = 2  # crosses divider at col 4
        return g
    return g
