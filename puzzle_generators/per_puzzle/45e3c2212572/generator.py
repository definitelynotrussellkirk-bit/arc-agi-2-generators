"""Generator for puzzle a61ba2ce.

Rule: find 3-cell L-tromino objects. Each orientation maps to one of 4
quadrants of a 4x4 output, based on which of the (0,0)/(0,1)/(1,0)
positions the shape contains.

Combinatorial axes (8): grid_h/w, n_trominoes, palette_kind,
position_bias, padding, anchor_corner, asymmetry_force, include_decoy.
Degenerates: missing_orientation, all_same_orientation, single_tromino.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.place import place_no_overlap
from puzzle_generators.helpers.shape import L_TROMINOES

GENERATOR_ID = "45e3c2212572"
VERSION = "1.1.0"
TASK_ID = "45e3c2212572"
SUMMARY = "4 distinct L-trominos (one of each orientation); rule outputs 4x4."

INVARIANTS = [
    "background is 0",
    "exactly 4 connected 3-cell objects",
    "each is an L-tromino (one of 4 orientations)",
    "all 4 orientations present (one of each)",
    "each object has a unique non-bg color",
    "objects don't touch (4-conn)",
]

POSITION_BIASES = ("spread", "corners", "row_aligned", "diagonal",
                   "clustered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("missing_orientation", "all_same_orientation",
                       "single_tromino")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..16", "valid": "9..20"},
    "grid_w":         {"type": "int", "default": "rng 11..16", "valid": "9..20"},
    "n_trominoes":    {"type": "int", "default": "4", "valid": "4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "padding":        {"type": "int", "default": "1", "valid": "1..3"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 9, 11
    elif difficulty == "hard":
        h_lo, h_hi = 14, 20
    else:
        h_lo, h_hi = 11, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    padding = max(1, min(3, int(overrides.get("padding", 1))))
    palette = _build_palette(palette_kind, 4, rng)
    g = full_grid(h, w, 0)
    shapes = list(L_TROMINOES)
    rng.shuffle(shapes)
    for i, shape in enumerate(shapes):
        place_no_overlap(rng, g, shape, palette[i],
                         padding=padding, max_tries=80)
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        return random_palette(rng, n)
    rng.shuffle(pool)
    while len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
    return pool[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    palette = random_palette(rng, 4)
    if name == "missing_orientation":
        # Only 3 of 4 orientations present
        shapes = list(L_TROMINOES)[:3]
        rng.shuffle(shapes)
        for i, shape in enumerate(shapes):
            place_no_overlap(rng, g, shape, palette[i],
                             padding=1, max_tries=80)
        return g
    if name == "all_same_orientation":
        shape = list(L_TROMINOES)[0]
        for i in range(4):
            place_no_overlap(rng, g, shape, palette[i],
                             padding=1, max_tries=80)
        return g
    if name == "single_tromino":
        shape = list(L_TROMINOES)[0]
        place_no_overlap(rng, g, shape, palette[0],
                         padding=1, max_tries=80)
        return g
    return g
