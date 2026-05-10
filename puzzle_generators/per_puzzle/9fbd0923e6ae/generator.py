"""Generator for arc_additional_puzzles_21_set8:M50 — Mirror target across 5-axis.

Rule: target color is g[0][0]. 5-axis is a full-height or full-width
line. Mirror target-cells across the axis.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_targets, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_axis, no_targets, no_distractor.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9fbd0923e6ae"
VERSION = "1.1.0"
TASK_ID = "9fbd0923e6ae"
SUMMARY = "Target color at (0,0); 5-axis (col); 3-5 target cells on left side; 1-2 distractors on right."

INVARIANTS = [
    "g[0][0] is the target color (non-zero, non-5)",
    "exactly one full-height column of 5s (the axis)",
    "≥3 target cells on the LEFT of the axis (including (0,0))",
    "≥1 distractor cell of a different color on the RIGHT of the axis",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_axis", "no_targets", "no_distractor")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_targets":      {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "palette_size":   {"type": "str", "default": "2 (target+distractor)", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "left_of_axis_targets",
                       "valid": "left_of_axis_targets"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        n_lo, n_hi = 3, 4
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
        n_lo, n_hi = 4, 6
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
        n_lo, n_hi = 3, 5
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    target = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    g[0][0] = target
    axis = w // 2
    for r in range(h):
        g[r][axis] = 5
    n_targets = rng.randint(n_lo, n_hi)
    placed = 1
    for _ in range(60):
        if placed >= n_targets:
            break
        r = rng.randint(0, h - 1); c = rng.randint(0, axis - 1)
        if g[r][c] == 0 and 0 <= 2 * axis - c < w:
            g[r][c] = target
            placed += 1
    distract = rng.choice([v for v in [1, 2, 3, 4, 6, 7, 8, 9] if v != target])
    for _ in range(20):
        r = rng.randint(0, h - 1); c = rng.randint(axis + 1, w - 1)
        if g[r][c] == 0:
            g[r][c] = distract
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_axis":
        # Target color present but no 5-axis — rule has no mirror line.
        g[0][0] = 4
        g[2][1] = 4; g[3][2] = 4
        g[5][6] = 6
        return g
    if name == "no_targets":
        # Axis present but no target cells on either side beyond (0,0)
        # being unset — rule has nothing to mirror.
        axis = w // 2
        for r in range(h):
            g[r][axis] = 5
        return g
    if name == "no_distractor":
        # Target only, no right-side distractor. The rule's mirror-only-target
        # behavior gets ambiguous because it would be the same as a copy rule.
        axis = w // 2
        target = 4
        g[0][0] = target
        for r in range(h):
            g[r][axis] = 5
        g[2][1] = target; g[3][2] = target
        return g
    return g
