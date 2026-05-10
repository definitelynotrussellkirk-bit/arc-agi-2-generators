"""Generator for arc_puzzle_bank_21_set15:S15_M7 — match source or its mirror.

Rule: candidate shapes are reported as matches when they equal the
source or its horizontal mirror.

Combinatorial axes (8): grid_h, grid_w, palette_kind, include_fourth,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_source, no_match, all_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "26f02d922ca0"
VERSION = "1.1.0"
TASK_ID = "26f02d922ca0"

SUMMARY = "Candidate shapes are reported as matches when they equal the source or its horizontal mirror."

INVARIANTS = [
    "background is 0",
    "there is exactly one color-2 source object",
    "candidate objects use colors 3 through 6 and are ordered by top-left position",
    "at least one candidate matches the source or its horizontal mirror and at least one does not",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_source", "no_match", "all_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "rng 16..19", "valid": "14..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "include_fourth": {"type": "bool", "default": "rng", "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "source_with_candidates",
                       "valid": "source_with_candidates"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

SOURCE = [(0, 0), (1, 0), (1, 1), (2, 1)]
MIRROR = [(0, 1), (1, 1), (1, 0), (2, 0)]
ODD_A = [(0, 0), (0, 1), (1, 1)]
ODD_B = [(0, 1), (1, 0), (1, 1), (1, 2)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 16, 17)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 18, 19)
    else:
        h = ctx.draw_int("grid_h", 12, 15)
        w = ctx.draw_int("grid_w", 16, 19)
    include_fourth = ctx.draw_choice("include_fourth", [False, True])
    g = full_grid(h, w, 0)

    paint_at(g, 1, 1, SOURCE, 2)
    candidates = [(3, 1, 6, SOURCE), (4, 1, 11, ODD_A), (5, h - 5, 6, MIRROR)]
    if include_fourth:
        candidates.append((6, h - 4, w - 5, ODD_B))
    for color, r, c, shape in candidates:
        paint_at(g, r, c, shape, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 17
    g = full_grid(h, w, 0)
    if name == "no_source":
        # candidates exist but no color-2 source → no template to match against
        paint_at(g, 1, 6, SOURCE, 3)
        paint_at(g, 5, 11, ODD_A, 4)
        paint_at(g, h - 5, 6, MIRROR, 5)
        return g
    if name == "no_match":
        # source + only odd candidates that DON'T match → all rejected
        paint_at(g, 1, 1, SOURCE, 2)
        paint_at(g, 5, 6, ODD_A, 3)
        paint_at(g, h - 5, 11, ODD_B, 4)
        return g
    if name == "all_match":
        # every candidate is the source or its mirror → no rejected distractor
        paint_at(g, 1, 1, SOURCE, 2)
        paint_at(g, 5, 6, SOURCE, 3)
        paint_at(g, 5, 11, MIRROR, 4)
        paint_at(g, h - 5, 11, SOURCE, 5)
        return g
    return g
