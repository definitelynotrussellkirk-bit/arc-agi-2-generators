"""Generator for arc_puzzle_bank_21_set4:S4_E4 — fill 3x3 ring centers with cyan.

Rule: every gray 3x3 ring receives a cyan center cell.

Combinatorial axes (8): grid_h, grid_w, palette_kind, ring_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rings, all_distractors, ring_with_filled_center.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.place import place_no_overlap
from puzzle_generators.helpers.shape import RING_3X3

GENERATOR_ID = "cc90240d0045"
VERSION = "1.1.0"
TASK_ID = "cc90240d0045"
SUMMARY = "Every gray 3x3 ring receives a cyan center cell."

INVARIANTS = [
    "background is 0",
    "all complete rings are gray 3x3 hollow squares",
    "ring centers are empty in the input",
    "optional gray distractors are not complete 3x3 rings",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rings", "all_distractors", "ring_with_filled_center")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "ring_count":     {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "spaced_3x3_rings",
                       "valid": "spaced_3x3_rings"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_DISTRACTORS = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        count = ctx.draw_int("ring_count", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        count = ctx.draw_int("ring_count", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 11)
        count = ctx.draw_int("ring_count", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for _ in range(count):
        if place_no_overlap(rng, g, RING_3X3, 5, padding=1, max_tries=400) is None:
            raise ValueError("could not place ring")
    if rng.random() < 0.7:
        place_no_overlap(rng, g, rng.choice(_DISTRACTORS), 5, padding=1, max_tries=200)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_rings":
        # blank → no rings to fill
        return g
    if name == "all_distractors":
        # only non-ring gray shapes → no rings to fill
        for (dr, dc) in [(0, 0), (0, 1), (1, 0), (1, 1)]: g[1 + dr][1 + dc] = 5  # 2x2 block
        for (dr, dc) in [(0, 0), (0, 1), (0, 2)]: g[5 + dr][3 + dc] = 5  # bar
        return g
    if name == "ring_with_filled_center":
        # ring with a non-zero center → "center is empty" precondition fails
        for (dr, dc) in RING_3X3: g[1 + dr][1 + dc] = 5
        g[2][2] = 4   # center already filled
        return g
    return g
