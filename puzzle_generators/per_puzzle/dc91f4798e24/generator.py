"""Generator for arc_additional_puzzle_bank_volume16:M110.

Rule: count components of colors 1, 2, and 3 and emit a three-row
histogram.

Combinatorial axes (8): grid_h/w, palette_kind, n_components,
palette_size, position_bias, n_distinct_colors, count_balance, texture.
Degenerates: equal_counts, missing_color, no_components.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dc91f4798e24"
VERSION = "1.1.0"
TASK_ID = "dc91f4798e24"
SUMMARY = "Count components of colors 1, 2, and 3 and emit a three-row histogram."

INVARIANTS = [
    "colors 1, 2, and 3 appear as separated components",
    "at least two rows have different counts",
]

PALETTE_KINDS = ("default", "sparse", "dense", "varied")
DEGENERATE_TEXTURES = ("equal_counts", "missing_color", "no_components")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_components":   {"type": "str", "default": "varied", "valid": "varied"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "count_balance":  {"type": "str", "default": "unbalanced",
                       "valid": "unbalanced"},
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
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 10, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    counts = {1: rng.randint(1, 3), 2: rng.randint(2, 4), 3: rng.randint(1, 3)}
    slots = [(r, c) for r in range(1, h, 2) for c in range(1, w, 3)]
    rng.shuffle(slots)
    idx = 0
    for color in [1, 2, 3]:
        for _ in range(counts[color]):
            r, c = slots[idx]
            idx += 1
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "equal_counts":
        # all three colors have same count → all rows identical (no signal)
        slots = [(1, 1), (3, 1), (1, 5), (3, 5), (1, 9), (3, 9)]
        for i, color in enumerate([1, 2, 3]):
            r1, c1 = slots[i * 2]
            r2, c2 = slots[i * 2 + 1]
            g[r1][c1] = color
            g[r2][c2] = color
        return g
    if name == "missing_color":
        # color 2 is absent → histogram has zero row in the middle
        g[1][1] = 1; g[3][1] = 1
        g[1][9] = 3; g[5][9] = 3
        return g
    if name == "no_components":
        # empty grid — all three counts zero
        return g
    return g
