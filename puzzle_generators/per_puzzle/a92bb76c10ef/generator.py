"""Generator for arc_additional_puzzle_bank_volume18:M123.

Rule: count objects of colors 2, 3, and 4, then emit grouped color
runs separated by zeros.

Combinatorial axes (8): grid_h, grid_w, palette_kind, count_spread,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_color, equal_counts, no_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a92bb76c10ef"
VERSION = "1.1.0"
TASK_ID = "a92bb76c10ef"
SUMMARY = "Count objects of colors 2, 3, and 4, then emit grouped color runs separated by zeros."

INVARIANTS = [
    "only colors 2, 3, and 4 matter",
    "same-color objects are separated so counts are visible",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_color", "equal_counts", "no_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "count_spread":   {"type": "str", "default": "varied", "valid": "varied"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread_slots",
                       "valid": "spread_slots"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        w = ctx.draw_int("grid_w", 10, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 10, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    counts = {2: rng.randint(1, 3), 3: rng.randint(1, 3), 4: rng.randint(1, 3)}
    slots = [(r, c) for r in range(1, h, 2) for c in range(1, w, 3)]
    rng.shuffle(slots)
    idx = 0
    for color in [2, 3, 4]:
        for _ in range(counts[color]):
            r, c = slots[idx]
            idx += 1
            g[r][c] = color
            if rng.random() < 0.35 and c + 1 < w:
                g[r][c + 1] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "missing_color":
        # one of {2,3,4} has count 0 → its run in the output is empty
        slots = [(1, 1), (3, 4), (5, 8)]
        for (r, c), color in zip(slots, [2, 4, 4]):
            g[r][c] = color
        return g
    if name == "equal_counts":
        # all three counts equal → output run-lengths are identical, no rank signal
        for (r, c), color in [((1, 1), 2), ((1, 5), 2),
                              ((3, 1), 3), ((3, 5), 3),
                              ((5, 1), 4), ((5, 5), 4)]:
            g[r][c] = color
        return g
    if name == "no_objects":
        # empty grid → all counts zero, output collapses to zeros
        return g
    return g
