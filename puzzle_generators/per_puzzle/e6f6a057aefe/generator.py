"""Generator for arc_puzzle_bank_tenth_21_bundle:hard_67_select_ranked_component_scale_and_place.

The value at (0,0) chooses the size-ranked object. A color-9 marker gives the
paste location for a 2x upscaled crop of that object.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rank,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rank, no_marker, no_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e6f6a057aefe"
VERSION = "1.1.0"
TASK_ID = "e6f6a057aefe"
SUMMARY = "Select a size-ranked object, upscale it by 2, and paste at the 9 marker."

INVARIANTS = [
    "cell (0,0) is a rank from 1 to 3",
    "there is one color-9 marker away from the source objects",
    "objects have distinct sizes and are sorted ascending by size",
    "the selected object's 2x crop fits at the marker location",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rank", "no_marker", "no_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12..12"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rank":           {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "rank_plus_marker_plus_objects",
                       "valid": "rank_plus_marker_plus_objects"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_OBJECTS = [
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1), (2, 1)],
]
_POSITIONS = [(2, 1), (5, 1), (2, 5)]


def _paint(g, top, left, cells, color):
    for dr, dc in cells:
        g[top + dr][left + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        rank = ctx.draw_int("rank", 1, 1)
    elif difficulty == "hard":
        rank = ctx.draw_int("rank", 2, 3)
    else:
        rank = ctx.draw_int("rank", 1, 3)
    colors = rng.sample([2, 3, 4, 5, 6, 7, 8], 3)
    g = full_grid(12, 14, 0)
    g[0][0] = rank
    g[6 + rng.randint(0, 1)][8 + rng.randint(0, 1)] = 9
    for cells, pos, color in zip(_OBJECTS, _POSITIONS, colors):
        _paint(g, pos[0], pos[1], cells, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 14, 0)
    if name == "no_rank":
        # marker + objects but no rank at (0,0) → no selection signal
        g[7][9] = 9
        for cells, pos, color in zip(_OBJECTS, _POSITIONS, [4, 6, 7]):
            _paint(g, pos[0], pos[1], cells, color)
        return g
    if name == "no_marker":
        # rank + objects but no 9-marker → no paste location
        g[0][0] = 2
        for cells, pos, color in zip(_OBJECTS, _POSITIONS, [4, 6, 7]):
            _paint(g, pos[0], pos[1], cells, color)
        return g
    if name == "no_objects":
        # rank + marker but no source objects → nothing to scale
        g[0][0] = 2
        g[7][9] = 9
        return g
    return g
