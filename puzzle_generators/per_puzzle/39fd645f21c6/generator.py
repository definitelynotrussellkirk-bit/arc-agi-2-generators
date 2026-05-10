"""Generator for arc_puzzle_bank_21_set13_s:S13_M2 — blue seed selects feature-matching object.

Rule: a blue seed object's area, hole count, and symmetry class select
matching objects.

Combinatorial axes (8): grid_h, grid_w, palette_kind, seed_shape,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seed, no_match, multiple_matches.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "39fd645f21c6"
VERSION = "1.1.0"
TASK_ID = "39fd645f21c6"

SUMMARY = "A blue seed object's area, hole count, and symmetry class select matching objects."

INVARIANTS = [
    "background is 0",
    "there is exactly one blue seed object",
    "one non-blue object shares the seed's feature triple",
    "other objects differ by area, holes, or symmetry class",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seed", "no_match", "multiple_matches")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 13..16", "valid": "11..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "seed_shape":     {"type": "str", "default": "rng l|t", "valid": "l|t"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "blue_seed_with_distractors",
                       "valid": "blue_seed_with_distractors"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

L_3 = [(0, 0), (1, 0), (1, 1)]
T_DOWN = [(0, 0), (0, 1), (0, 2), (1, 1)]
PLUS_5 = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
RING_8 = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 15, 16)
    else:
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 13, 16)
    seed_shape = ctx.draw_choice("seed_shape", ["l", "t"])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)

    shape = L_3 if seed_shape == "l" else T_DOWN
    r0 = rng.randint(1, 2)
    c0 = rng.randint(1, 2)
    paint_at(g, r0, c0, shape, 1)
    paint_at(g, r0, c0 + 6, shape, 4)
    paint_at(g, h - 4, 1, PLUS_5, 6)
    paint_at(g, h - 4, w - 4, RING_8, 7)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 14
    g = full_grid(h, w, 0)
    if name == "no_seed":
        # no blue object → no seed feature triple to match
        paint_at(g, 1, 1, L_3, 4)
        paint_at(g, h - 4, 1, PLUS_5, 6)
        paint_at(g, h - 4, w - 4, RING_8, 7)
        return g
    if name == "no_match":
        # blue seed exists but no other object shares its feature triple
        paint_at(g, 1, 1, L_3, 1)
        paint_at(g, h - 4, 1, PLUS_5, 6)
        paint_at(g, h - 4, w - 4, RING_8, 7)
        return g
    if name == "multiple_matches":
        # multiple non-blue objects match the seed → ambiguous selection
        paint_at(g, 1, 1, L_3, 1)
        paint_at(g, 1, 7, L_3, 4)   # match #1
        paint_at(g, h - 4, 1, L_3, 6)   # match #2 (same shape!)
        return g
    return g
